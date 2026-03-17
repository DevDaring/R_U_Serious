"""
Admin Routes - Admin-only functionality
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
import io

from app.api.dependencies import get_current_admin_user
from app.database.csv_handler import CSVHandler
from app.models.tournament import TournamentCreate
from app.models.user import User
from app.utils.helpers import generate_unique_id

router = APIRouter()


@router.post("/tournaments/create", status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Create a new tournament (admin only)

    Args:
        tournament_data: Tournament configuration
        current_user: Authenticated admin user

    Returns:
        Created tournament data
    """
    csv_handler = CSVHandler()

    try:
        # Generate tournament ID
        tournament_id = generate_unique_id("TRN")

        # Create tournament record
        tournament = {
            "tournament_id": tournament_id,
            "name": tournament_data.name,
            "topic": tournament_data.topic,
            "difficulty_level": tournament_data.difficulty_level,
            "start_datetime": tournament_data.start_datetime.isoformat(),
            "end_datetime": tournament_data.end_datetime.isoformat(),
            "duration_minutes": tournament_data.duration_minutes,
            "max_participants": tournament_data.max_participants,
            "team_size_min": tournament_data.team_size_min,
            "team_size_max": tournament_data.team_size_max,
            "entry_type": tournament_data.entry_type,
            "status": tournament_data.status or "upcoming",
            "prize_1st": tournament_data.prize_1st or "",
            "prize_2nd": tournament_data.prize_2nd or "",
            "prize_3rd": tournament_data.prize_3rd or "",
            "created_by": current_user["user_id"],
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("tournaments", tournament)

        return {
            "message": "Tournament created successfully",
            "tournament": tournament
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating tournament: {str(e)}"
        )


@router.post("/questions/upload", status_code=status.HTTP_201_CREATED)
async def upload_questions(
    file: UploadFile = File(...),
    question_type: str = Form(...),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Upload questions from CSV file (admin only)

    Args:
        file: CSV file with questions
        question_type: Type of questions (mcq/descriptive)
        current_user: Authenticated admin user

    Returns:
        Upload summary
    """
    csv_handler = CSVHandler()

    try:
        # Read uploaded CSV file
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        uploaded_count = 0
        errors = []

        if question_type == "mcq":
            # Validate required columns
            required_columns = [
                "topic", "difficulty_level", "question_text",
                "option_a", "option_b", "option_c", "option_d",
                "correct_answer", "explanation"
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required columns: {', '.join(missing_columns)}"
                )

            # Process each row
            for idx, row in df.iterrows():
                try:
                    question_id = generate_unique_id("Q")
                    question_data = {
                        "question_id": question_id,
                        "topic": str(row["topic"]),
                        "difficulty_level": int(row["difficulty_level"] if row["difficulty_level"] is not None else 5),
                        "question_text": str(row["question_text"]),
                        "option_a": str(row["option_a"]),
                        "option_b": str(row["option_b"]),
                        "option_c": str(row["option_c"]),
                        "option_d": str(row["option_d"]),
                        "correct_answer": str(row["correct_answer"]).upper(),
                        "explanation": str(row["explanation"]),
                        "created_by": current_user["user_id"],
                        "is_ai_generated": False,
                        "created_at": datetime.now().isoformat()
                    }

                    csv_handler.create("questions_mcq", question_data)
                    uploaded_count += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")

        elif question_type == "descriptive":
            # Validate required columns
            required_columns = [
                "topic", "difficulty_level", "question_text",
                "model_answer", "keywords", "max_score"
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required columns: {', '.join(missing_columns)}"
                )

            # Process each row
            for idx, row in df.iterrows():
                try:
                    question_id = generate_unique_id("DQ")
                    question_data = {
                        "question_id": question_id,
                        "topic": str(row["topic"]),
                        "difficulty_level": int(row["difficulty_level"] if row["difficulty_level"] is not None else 5),
                        "question_text": str(row["question_text"]),
                        "model_answer": str(row["model_answer"]),
                        "keywords": str(row["keywords"]),  # Comma-separated
                        "max_score": int(row["max_score"] if row["max_score"] is not None else 10),
                        "created_by": current_user["user_id"],
                        "is_ai_generated": False,
                        "created_at": datetime.now().isoformat()
                    }

                    csv_handler.create("questions_descriptive", question_data)
                    uploaded_count += 1

                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid question_type. Must be 'mcq' or 'descriptive'"
            )

        return {
            "message": f"Successfully uploaded {uploaded_count} questions",
            "uploaded_count": uploaded_count,
            "total_rows": len(df),
            "errors": errors if errors else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading questions: {str(e)}"
        )


@router.get("/users", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_all_users(
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Get all users (admin only)

    Args:
        limit: Maximum number of users to return
        offset: Number of users to skip
        current_user: Authenticated admin user

    Returns:
        List of users
    """
    csv_handler = CSVHandler()

    try:
        # Get all users
        all_users = csv_handler.read_all("users")

        # Remove password hashes
        users_data = [
            {k: v for k, v in user.items() if k != "password_hash"}
            for user in all_users
        ]

        # Apply pagination
        paginated_users = users_data[offset:offset + limit]

        return paginated_users

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )

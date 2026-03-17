"""
Quiz Routes - MCQ and descriptive questions
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.models.quiz import (
    MCQQuestionDisplay,
    MCQAnswerSubmit,
    MCQAnswerResult,
    DescriptiveQuestionDisplay,
    DescriptiveAnswerSubmit,
    DescriptiveAnswerResult
)
from app.services.question_generator import QuestionGenerator
from app.services.answer_evaluator import AnswerEvaluator
from app.utils.helpers import generate_unique_id

router = APIRouter()


@router.get("/session/{session_id}/mcq", response_model=list[MCQQuestionDisplay], status_code=status.HTTP_200_OK)
async def get_mcq_questions(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get MCQ questions for a learning session

    Args:
        session_id: Session identifier
        current_user: Authenticated user

    Returns:
        List of MCQ questions without answers
    """
    csv_handler = CSVHandler()
    question_generator = QuestionGenerator()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Get learning content for context
        history = csv_handler.read_all("learning_history")
        session_history = [h for h in history if h.get("session_id") == session_id]
        content_context = f"Topic: {session['topic']}"

        # Generate MCQ questions
        num_questions = min(3, session["total_cycles"])
        questions = await question_generator.generate_mcq_questions(
            topic=session["topic"],
            difficulty_level=session["difficulty_level"],
            content_context=content_context,
            num_questions=num_questions
        )

        # Format for display (without correct answers)
        display_questions = []
        for q in questions:
            display_questions.append({
                "question_id": q["question_id"],
                "question_text": q["question_text"],
                "options": {
                    "A": q["option_a"],
                    "B": q["option_b"],
                    "C": q["option_c"],
                    "D": q["option_d"]
                },
                "image_url": q.get("image_url")
            })

        return display_questions

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching MCQ questions: {str(e)}"
        )


@router.post("/session/{session_id}/mcq/answer", response_model=MCQAnswerResult, status_code=status.HTTP_200_OK)
async def submit_mcq_answer(
    session_id: str,
    answer_data: MCQAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit and evaluate MCQ answer

    Args:
        session_id: Session identifier
        answer_data: User's answer
        current_user: Authenticated user

    Returns:
        Answer evaluation result
    """
    csv_handler = CSVHandler()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Get question
        question = csv_handler.read_by_id("questions_mcq", answer_data.question_id, "question_id")
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        # Evaluate answer
        is_correct = answer_data.selected_answer == question["correct_answer"]
        points_earned = 10 if is_correct else 2  # Full points if correct, partial for attempt

        # Save score
        score_data = {
            "score_id": generate_unique_id("SCR"),
            "user_id": current_user["user_id"],
            "session_id": session_id,
            "question_id": answer_data.question_id,
            "question_type": "mcq",
            "user_answer": answer_data.selected_answer,
            "is_correct": str(is_correct).lower(),
            "points_earned": points_earned,
            "time_taken_seconds": 30,  # Default, should be tracked by frontend
            "evaluated_at": datetime.now().isoformat()
        }
        csv_handler.create("scores", score_data)

        # Update session score
        session["score"] = int(session.get("score", 0) or 0) + points_earned
        csv_handler.update("sessions", session_id, session, "session_id")

        return {
            "question_id": answer_data.question_id,
            "selected_answer": answer_data.selected_answer,
            "correct_answer": question["correct_answer"],
            "is_correct": is_correct,
            "explanation": question["explanation"],
            "points_earned": points_earned,
            "time_taken_seconds": 30
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting MCQ answer: {str(e)}"
        )


@router.get("/session/{session_id}/descriptive", response_model=list[DescriptiveQuestionDisplay], status_code=status.HTTP_200_OK)
async def get_descriptive_questions(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get descriptive questions for a learning session

    Args:
        session_id: Session identifier
        current_user: Authenticated user

    Returns:
        List of descriptive questions
    """
    csv_handler = CSVHandler()
    question_generator = QuestionGenerator()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Get learning content for context
        content_context = f"Topic: {session['topic']}"

        # Generate descriptive questions
        num_questions = min(3, session["total_cycles"])
        questions = await question_generator.generate_descriptive_questions(
            topic=session["topic"],
            difficulty_level=session["difficulty_level"],
            content_context=content_context,
            num_questions=num_questions
        )

        # Format for display
        display_questions = []
        for q in questions:
            display_questions.append({
                "question_id": q["question_id"],
                "question_text": q["question_text"],
                "max_score": q["max_score"]
            })

        return display_questions

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching descriptive questions: {str(e)}"
        )


@router.post("/session/{session_id}/descriptive/answer", response_model=DescriptiveAnswerResult, status_code=status.HTTP_200_OK)
async def submit_descriptive_answer(
    session_id: str,
    answer_data: DescriptiveAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit and evaluate descriptive answer using AI

    Args:
        session_id: Session identifier
        answer_data: User's answer
        current_user: Authenticated user

    Returns:
        Answer evaluation with feedback
    """
    csv_handler = CSVHandler()
    answer_evaluator = AnswerEvaluator()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Get question
        question = csv_handler.read_by_id("questions_descriptive", answer_data.question_id, "question_id")
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        # Evaluate answer using AI
        evaluation = await answer_evaluator.evaluate_answer(
            question=question["question_text"],
            model_answer=question["model_answer"],
            user_answer=answer_data.answer_text,
            keywords=question["keywords"].split(",") if isinstance(question["keywords"], str) else question["keywords"],
            max_score=int(question.get("max_score", 10) or 10)
        )

        # Save score
        score_data = {
            "score_id": generate_unique_id("SCR"),
            "user_id": current_user["user_id"],
            "session_id": session_id,
            "question_id": answer_data.question_id,
            "question_type": "descriptive",
            "user_answer": answer_data.answer_text,
            "is_correct": str(evaluation["score"] >= int(question.get("max_score", 10) or 10) * 0.6).lower(),
            "points_earned": evaluation["score"],
            "time_taken_seconds": 60,  # Default, should be tracked by frontend
            "evaluated_at": datetime.now().isoformat()
        }
        csv_handler.create("scores", score_data)

        # Update session score
        session["score"] = int(session.get("score", 0) or 0) + evaluation["score"]
        csv_handler.update("sessions", session_id, session, "session_id")

        return {
            "question_id": answer_data.question_id,
            "user_answer": answer_data.answer_text,
            "score": evaluation["score"],
            "max_score": evaluation["max_score"],
            "feedback": evaluation["feedback"],
            "points_earned": evaluation["score"],
            "time_taken_seconds": 60
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting descriptive answer: {str(e)}"
        )

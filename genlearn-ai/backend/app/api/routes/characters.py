"""
Character Routes - Create and manage story characters
"""

import logging
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import Optional

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.database.file_handler import FileHandler

logger = logging.getLogger(__name__)
router = APIRouter()
csv_handler = CSVHandler()
file_handler = FileHandler()

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.get("/list")
async def list_characters(current_user: dict = Depends(get_current_user)):
    """List all characters for the current user"""
    try:
        df = csv_handler.read("characters")
        if df.empty:
            return []
        user_chars = df[df["user_id"] == current_user["user_id"]]
        characters = []
        for _, row in user_chars.iterrows():
            characters.append({
                "character_id": row["character_id"],
                "user_id": row["user_id"],
                "name": row["name"],
                "image_url": f"/media/{row['image_path']}" if row.get("image_path") else "",
                "creation_method": row.get("creation_method", "upload"),
                "description": row.get("description", ""),
            })
        return characters
    except Exception as e:
        logger.error(f"Error listing characters: {e}")
        return []


@router.post("/create")
async def create_character(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(""),
    current_user: dict = Depends(get_current_user),
):
    """Create a character from an uploaded image"""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")

    file_data = await file.read()
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    char_id = f"CHR{uuid.uuid4().hex[:8].upper()}"
    filename = file_handler.generate_filename(file.filename or "character.png", f"character_{char_id}")
    success, relative_path = file_handler.save_file(file_data, filename, "characters")

    if not success:
        raise HTTPException(status_code=500, detail="Failed to save image")

    record = {
        "character_id": char_id,
        "user_id": current_user["user_id"],
        "name": name[:100],
        "image_path": relative_path,
        "creation_method": "upload",
        "description": description[:500],
        "created_at": datetime.now().isoformat(),
    }
    csv_handler.create("characters", record)

    return {
        "character_id": char_id,
        "name": name[:100],
        "image_url": f"/media/{relative_path}",
        "creation_method": "upload",
        "description": description[:500],
    }


@router.post("/upload")
async def upload_character(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(""),
    style: str = Form("cartoon"),
    custom_prompt: str = Form(""),
    current_user: dict = Depends(get_current_user),
):
    """Create a character from uploaded image (with style metadata)"""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")

    file_data = await file.read()
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    char_id = f"CHR{uuid.uuid4().hex[:8].upper()}"
    filename = file_handler.generate_filename(file.filename or "character.png", f"character_{char_id}")
    success, relative_path = file_handler.save_file(file_data, filename, "characters")

    if not success:
        raise HTTPException(status_code=500, detail="Failed to save image")

    record = {
        "character_id": char_id,
        "user_id": current_user["user_id"],
        "name": name[:100],
        "image_path": relative_path,
        "creation_method": "upload",
        "description": description[:500],
        "created_at": datetime.now().isoformat(),
    }
    csv_handler.create("characters", record)

    return {
        "character_id": char_id,
        "name": name[:100],
        "image_url": f"/media/{relative_path}",
        "creation_method": "upload",
        "description": description[:500],
    }


@router.delete("/{character_id}")
async def delete_character(
    character_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a character"""
    df = csv_handler.read("characters")
    if df.empty:
        raise HTTPException(status_code=404, detail="Character not found")

    mask = (df["character_id"] == character_id) & (df["user_id"] == current_user["user_id"])
    if not mask.any():
        raise HTTPException(status_code=404, detail="Character not found")

    # Delete the image file
    row = df[mask].iloc[0]
    if row.get("image_path"):
        file_handler.delete_file(row["image_path"])

    df = df[~mask]
    csv_handler.write(df, "characters")

    return {"message": "Character deleted"}

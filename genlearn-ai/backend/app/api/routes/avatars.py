"""
Avatar Routes - List and manage user avatars
"""

import logging
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler

logger = logging.getLogger(__name__)
router = APIRouter()
csv_handler = CSVHandler()


@router.get("/list")
async def list_avatars(current_user: dict = Depends(get_current_user)):
    """List all avatars for the current user"""
    try:
        df = csv_handler.read("avatars")
        if df.empty:
            return []
        user_avatars = df[df["user_id"] == current_user["user_id"]]
        avatars = []
        for _, row in user_avatars.iterrows():
            avatars.append({
                "avatar_id": row["avatar_id"],
                "name": row["name"],
                "image_url": f"/media/{row['image_path']}" if row.get("image_path") else "",
                "creation_method": row.get("creation_method", "upload"),
                "style": row.get("style", "cartoon"),
            })
        return avatars
    except Exception as e:
        logger.error(f"Error listing avatars: {e}")
        return []

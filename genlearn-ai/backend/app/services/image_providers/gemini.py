"""
Gemini / Imagen Image Provider (fallback)
Uses Google's Imagen 4.0 model via the Generative Language API for image generation.
"""

import os
import base64
import logging
import httpx
from app.services.image_providers.base import BaseImageProvider, ImageGenerationRequest

logger = logging.getLogger(__name__)

API_BASE = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "imagen-4.0-generate-001"


class GeminiImageProvider(BaseImageProvider):
    """Image provider using Google Imagen 4.0 via Generative Language API."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set — gemini image provider will fail")
        self.timeout = 90.0

    async def _call_imagen(self, prompt: str) -> bytes:
        """Call Imagen 4.0 predict endpoint and return image bytes."""
        url = f"{API_BASE}/models/{MODEL}:predict?key={self.api_key}"
        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1},
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
            resp.raise_for_status()
            data = resp.json()

            predictions = data.get("predictions", [])
            if not predictions:
                raise ValueError("No predictions returned from Imagen")

            b64 = predictions[0].get("bytesBase64Encoded", "")
            if not b64:
                raise ValueError("No image data in Imagen response")

            image_bytes = base64.b64decode(b64)
            logger.info(f"Imagen image generated: {len(image_bytes)} bytes")
            return image_bytes

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        style_hint = (
            "cartoon style, vibrant colors, child-friendly illustration, "
            if request.style == "cartoon"
            else "photorealistic, detailed, cinematic lighting, "
        )
        full_prompt = f"{style_hint}{request.prompt}"
        try:
            return await self._call_imagen(full_prompt)
        except Exception as e:
            logger.error(f"Gemini/Imagen generate_image failed: {e}")
            raise

    async def generate_avatar(
        self, source_image: bytes, style: str = "cartoon", custom_prompt: str = ""
    ) -> bytes:
        prompt = custom_prompt or f"A {style} avatar character portrait, colorful, friendly, expressive face"
        try:
            return await self._call_imagen(prompt)
        except Exception as e:
            logger.error(f"Gemini/Imagen generate_avatar failed: {e}")
            raise

    async def stylize_character(
        self, source_image: bytes, style: str = "cartoon"
    ) -> bytes:
        prompt = f"A {style} character full body illustration, vibrant colors, detailed, suitable for children's educational content"
        try:
            return await self._call_imagen(prompt)
        except Exception as e:
            logger.error(f"Gemini/Imagen stylize_character failed: {e}")
            raise

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            result = await self._call_imagen("a small red dot")
            return len(result) > 100
        except Exception:
            return False


GeminiProvider = GeminiImageProvider

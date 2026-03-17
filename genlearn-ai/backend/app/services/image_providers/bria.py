"""
Bria.ai FIBO v2 Image Provider
Uses the bria.ai hosted FIBO API for image generation.
The /v2/image/generate endpoint internally uses Gemini 2.5 Flash VLM bridge
to convert text prompts into structured JSON before generating images.

API docs: https://docs.bria.ai/image-generation/endpoints/image-generate
"""

import os
import logging
import httpx
from app.services.image_providers.base import BaseImageProvider, ImageGenerationRequest

logger = logging.getLogger(__name__)

BASE_URL = "https://engine.prod.bria-api.com/v2"


class BriaImageProvider(BaseImageProvider):
    """Image provider using Bria.ai FIBO v2 API."""

    def __init__(self):
        self.api_key = os.getenv("BRIA_API_KEY", "")
        if not self.api_key:
            logger.warning("BRIA_API_KEY not set — bria provider will fail on requests")
        self.timeout = 120.0

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "api_token": self.api_key,
        }

    def _aspect_ratio(self, width: int, height: int) -> str:
        ratio = width / height
        mapping = [
            (16 / 9, "16:9"),
            (9 / 16, "9:16"),
            (4 / 3, "4:3"),
            (3 / 4, "3:4"),
            (3 / 2, "3:2"),
            (2 / 3, "2:3"),
            (5 / 4, "5:4"),
            (4 / 5, "4:5"),
        ]
        best = min(mapping, key=lambda x: abs(x[0] - ratio))
        if abs(best[0] - ratio) < 0.15:
            return best[1]
        return "1:1"

    async def _call_generate(self, prompt: str, aspect_ratio: str = "16:9") -> bytes:
        """Call bria.ai /v2/image/generate with sync=true."""
        payload = {
            "prompt": prompt,
            "sync": True,
            "aspect_ratio": aspect_ratio,
            "model_version": "FIBO",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{BASE_URL}/image/generate",
                headers=self._get_headers(),
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

            image_url = data.get("result", {}).get("image_url")
            if not image_url:
                raise ValueError("No image_url in bria response")

            logger.info(f"Bria FIBO image generated, downloading from CloudFront")
            img_resp = await client.get(image_url, timeout=60.0)
            img_resp.raise_for_status()

            if len(img_resp.content) < 100:
                raise ValueError("Downloaded image too small")

            logger.info(f"Bria image downloaded: {len(img_resp.content)} bytes")
            return img_resp.content

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        style_hint = (
            "cartoon style, vibrant colors, child-friendly illustration, "
            if request.style == "cartoon"
            else "photorealistic, detailed, cinematic lighting, "
        )
        full_prompt = f"{style_hint}{request.prompt}"
        aspect = self._aspect_ratio(request.width, request.height)

        try:
            return await self._call_generate(full_prompt, aspect)
        except Exception as e:
            logger.error(f"Bria generate_image failed: {e}")
            raise

    async def generate_avatar(
        self, source_image: bytes, style: str = "cartoon", custom_prompt: str = ""
    ) -> bytes:
        prompt = custom_prompt or f"A {style} avatar character portrait, colorful, friendly, expressive face"
        try:
            return await self._call_generate(prompt, "1:1")
        except Exception as e:
            logger.error(f"Bria generate_avatar failed: {e}")
            raise

    async def stylize_character(
        self, source_image: bytes, style: str = "cartoon"
    ) -> bytes:
        prompt = f"A {style} character full body illustration, vibrant colors, detailed, suitable for children's educational content"
        try:
            return await self._call_generate(prompt, "3:4")
        except Exception as e:
            logger.error(f"Bria stylize_character failed: {e}")
            raise

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            return await self._call_generate("a small red dot", "1:1") is not None
        except Exception:
            return False


BriaProvider = BriaImageProvider

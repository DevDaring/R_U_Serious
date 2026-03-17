"""
Pollinations.ai Image Provider
Free image generation API - no API key required for basic usage.
https://pollinations.ai/
"""

import httpx
import logging
from urllib.parse import quote
from app.services.image_providers.base import BaseImageProvider, ImageGenerationRequest

logger = logging.getLogger(__name__)

BASE_URL = "https://gen.pollinations.ai"


class PollinationsImageProvider(BaseImageProvider):
    """Image provider using Pollinations.ai free API."""

    def __init__(self):
        self.timeout = 60.0

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        style_suffix = (
            ", cartoon style, vibrant colors, illustrated"
            if request.style == "cartoon"
            else ", photorealistic, high detail, cinematic lighting"
        )
        full_prompt = request.prompt + style_suffix
        encoded_prompt = quote(full_prompt, safe="")

        url = (
            f"{BASE_URL}/image/{encoded_prompt}"
            f"?model=flux&width={request.width}&height={request.height}"
            f"&enhance=true&nologo=true"
        )

        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                if len(resp.content) > 100:
                    logger.info(f"Pollinations image generated: {len(resp.content)} bytes")
                    return resp.content
                logger.warning("Pollinations returned too-small response")
                return b""
        except Exception as e:
            logger.error(f"Pollinations image generation failed: {e}")
            return b""

    async def generate_avatar(
        self, source_image: bytes, style: str = "cartoon", custom_prompt: str = ""
    ) -> bytes:
        prompt = custom_prompt or f"A {style} avatar character portrait, colorful, friendly"
        request = ImageGenerationRequest(prompt=prompt, style=style, width=512, height=512)
        return await self.generate_image(request)

    async def stylize_character(
        self, source_image: bytes, style: str = "cartoon"
    ) -> bytes:
        prompt = f"A {style} character full body illustration, vibrant, detailed"
        request = ImageGenerationRequest(prompt=prompt, style=style, width=512, height=768)
        return await self.generate_image(request)

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                resp = await client.get(f"{BASE_URL}/image/health%20check%20test?width=64&height=64&nologo=true")
                return resp.status_code == 200
        except Exception:
            return False


PollinationsProvider = PollinationsImageProvider

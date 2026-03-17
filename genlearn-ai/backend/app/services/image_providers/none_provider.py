"""
None/Disabled Image Provider

Placeholder provider that returns empty bytes - used when image generation
is disabled via IMAGE_PROVIDER=none
"""

from .base import BaseImageProvider, ImageGenerationRequest


class NoneImageProvider(BaseImageProvider):
    """Disabled image provider - returns empty image bytes."""

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        """Return empty bytes (image generation disabled)."""
        return b""

    async def generate_avatar(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = ""
    ) -> bytes:
        """Return empty bytes (image generation disabled)."""
        return b""

    async def stylize_character(
        self,
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """Return empty bytes (image generation disabled)."""
        return b""

    async def health_check(self) -> bool:
        """Always healthy since it's intentionally disabled."""
        return True

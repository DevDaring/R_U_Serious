"""
Provider Factory - SINGLE POINT OF CONFIGURATION FOR ALL API PROVIDERS

To switch providers, change the corresponding environment variable:
- AI_PROVIDER: digitalocean, openai, anthropic
- IMAGE_PROVIDER: bria, gemini, fibo, stability, none
- IMAGE_FALLBACK_PROVIDER: gemini (auto-fallback when primary fails)
- VOICE_TTS_PROVIDER: azure, none (none = disable voice features)
- VOICE_STT_PROVIDER: azure, none (none = disable voice features)

No other code changes required!
"""

import os
import logging
from typing import Optional
from app.services.ai_providers.base import BaseAIProvider
from app.services.ai_providers.digitalocean import DigitalOceanAIProvider
from app.services.ai_providers.openai import OpenAIProvider
from app.services.ai_providers.anthropic import AnthropicProvider
from app.services.image_providers.base import BaseImageProvider, ImageGenerationRequest
from app.services.image_providers.fibo import FiboProvider
from app.services.image_providers.stability import StabilityProvider
from app.services.image_providers.none_provider import NoneImageProvider
from app.services.image_providers.pollinations import PollinationsProvider
from app.services.image_providers.bria import BriaProvider
from app.services.image_providers.gemini import GeminiProvider
from app.services.voice_providers.base import BaseTTSProvider, BaseSTTProvider
from app.services.voice_providers.azure_voice import AzureTTSProvider, AzureSTTProvider
from app.services.voice_providers.none_provider import NoneTTSProvider, NoneSTTProvider

logger = logging.getLogger(__name__)


class FallbackImageProvider(BaseImageProvider):
    """Wraps a primary image provider with automatic fallback to a secondary."""

    def __init__(self, primary: BaseImageProvider, fallback: BaseImageProvider):
        self.primary = primary
        self.fallback = fallback
        self.primary_name = primary.__class__.__name__
        self.fallback_name = fallback.__class__.__name__

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        try:
            return await self.primary.generate_image(request)
        except Exception as e:
            logger.warning(f"{self.primary_name} generate_image failed ({e}), falling back to {self.fallback_name}")
            return await self.fallback.generate_image(request)

    async def generate_avatar(self, source_image: bytes, style: str = "cartoon", custom_prompt: str = "") -> bytes:
        try:
            return await self.primary.generate_avatar(source_image, style, custom_prompt)
        except Exception as e:
            logger.warning(f"{self.primary_name} generate_avatar failed ({e}), falling back to {self.fallback_name}")
            return await self.fallback.generate_avatar(source_image, style, custom_prompt)

    async def stylize_character(self, source_image: bytes, style: str = "cartoon") -> bytes:
        try:
            return await self.primary.stylize_character(source_image, style)
        except Exception as e:
            logger.warning(f"{self.primary_name} stylize_character failed ({e}), falling back to {self.fallback_name}")
            return await self.fallback.stylize_character(source_image, style)

    async def health_check(self) -> bool:
        primary_ok = False
        try:
            primary_ok = await self.primary.health_check()
        except Exception:
            pass
        if primary_ok:
            return True
        try:
            return await self.fallback.health_check()
        except Exception:
            return False


class ProviderFactory:
    """
    Factory class to instantiate the correct provider based on configuration.

    USAGE:
        from app.services.provider_factory import ProviderFactory

        ai = ProviderFactory.get_ai_provider()
        image = ProviderFactory.get_image_provider()
        tts = ProviderFactory.get_tts_provider()
        stt = ProviderFactory.get_stt_provider()
    """

    # ============================================================
    # AI PROVIDERS (for content generation, question creation, etc.)
    # ============================================================

    _ai_providers = {
        "digitalocean": DigitalOceanAIProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }

    @classmethod
    def get_ai_provider(cls, provider_name: Optional[str] = None) -> BaseAIProvider:
        """
        Get AI provider instance.

        Args:
            provider_name: Override provider (optional).
                          If None, uses AI_PROVIDER env var.

        Returns:
            Configured AI provider instance
        """
        name = provider_name or os.getenv("AI_PROVIDER", "digitalocean")
        provider_class = cls._ai_providers.get(name.lower())

        if not provider_class:
            raise ValueError(
                f"Unknown AI provider: {name}. "
                f"Available: {list(cls._ai_providers.keys())}"
            )

        return provider_class()

    # ============================================================
    # IMAGE PROVIDERS (for image generation)
    # ============================================================

    _image_providers = {
        "bria": BriaProvider,
        "gemini": GeminiProvider,
        "fibo": FiboProvider,
        "stability": StabilityProvider,
        "pollinations": PollinationsProvider,
        "none": NoneImageProvider,
    }

    @classmethod
    def get_image_provider(cls, provider_name: Optional[str] = None) -> BaseImageProvider:
        """
        Get Image provider instance with automatic fallback.

        If IMAGE_FALLBACK_PROVIDER is set (e.g. "gemini"), the returned provider
        will automatically try the fallback when the primary fails.

        Args:
            provider_name: Override provider (optional).
                          If None, uses IMAGE_PROVIDER env var.

        Returns:
            Configured Image provider instance (with fallback wrapper if configured)
        """
        name = provider_name or os.getenv("IMAGE_PROVIDER", "fibo")
        provider_class = cls._image_providers.get(name.lower())

        if not provider_class:
            raise ValueError(
                f"Unknown Image provider: {name}. "
                f"Available: {list(cls._image_providers.keys())}"
            )

        primary = provider_class()

        # Check for fallback provider
        fallback_name = os.getenv("IMAGE_FALLBACK_PROVIDER", "").strip().lower()
        if fallback_name and fallback_name != name.lower():
            fallback_class = cls._image_providers.get(fallback_name)
            if fallback_class:
                fallback = fallback_class()
                logger.info(f"Image provider: {name} -> fallback: {fallback_name}")
                return FallbackImageProvider(primary, fallback)
            else:
                logger.warning(f"Unknown fallback provider '{fallback_name}', using primary only")

        return primary

    # ============================================================
    # TEXT-TO-SPEECH PROVIDERS
    # ============================================================

    _tts_providers = {
        "azure": AzureTTSProvider,
        "none": NoneTTSProvider,
    }

    @classmethod
    def get_tts_provider(cls, provider_name: Optional[str] = None) -> BaseTTSProvider:
        """
        Get Text-to-Speech provider instance.

        Args:
            provider_name: Override provider (optional).
                          If None, uses VOICE_TTS_PROVIDER env var.

        Returns:
            Configured TTS provider instance
        """
        name = provider_name or os.getenv("VOICE_TTS_PROVIDER", "none")
        provider_class = cls._tts_providers.get(name.lower())

        if not provider_class:
            raise ValueError(
                f"Unknown TTS provider: {name}. "
                f"Available: {list(cls._tts_providers.keys())}"
            )

        return provider_class()

    # ============================================================
    # SPEECH-TO-TEXT PROVIDERS
    # ============================================================

    _stt_providers = {
        "azure": AzureSTTProvider,
        "none": NoneSTTProvider,
    }

    @classmethod
    def get_stt_provider(cls, provider_name: Optional[str] = None) -> BaseSTTProvider:
        """
        Get Speech-to-Text provider instance.

        Args:
            provider_name: Override provider (optional).
                          If None, uses VOICE_STT_PROVIDER env var.

        Returns:
            Configured STT provider instance
        """
        name = provider_name or os.getenv("VOICE_STT_PROVIDER", "none")
        provider_class = cls._stt_providers.get(name.lower())

        if not provider_class:
            raise ValueError(
                f"Unknown STT provider: {name}. "
                f"Available: {list(cls._stt_providers.keys())}"
            )

        return provider_class()

    # ============================================================
    # CONVENIENCE METHOD - GET ALL PROVIDERS
    # ============================================================

    @classmethod
    def get_all_providers(cls) -> dict:
        """
        Get all provider instances at once.

        Returns:
            Dictionary with all provider instances
        """
        return {
            "ai": cls.get_ai_provider(),
            "image": cls.get_image_provider(),
            "tts": cls.get_tts_provider(),
            "stt": cls.get_stt_provider(),
        }

    # ============================================================
    # PROVIDER HEALTH CHECK
    # ============================================================

    @classmethod
    async def check_all_providers(cls) -> dict:
        """
        Check health/connectivity of all configured providers.

        Returns:
            Dictionary with provider status
        """
        providers = cls.get_all_providers()
        status = {}

        for name, provider in providers.items():
            try:
                is_healthy = await provider.health_check()
                status[name] = {
                    "provider": provider.__class__.__name__,
                    "status": "healthy" if is_healthy else "unhealthy"
                }
            except Exception as e:
                status[name] = {
                    "provider": provider.__class__.__name__,
                    "status": "error",
                    "error": str(e)
                }

        return status

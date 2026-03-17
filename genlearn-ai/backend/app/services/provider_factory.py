"""
Provider Factory - SINGLE POINT OF CONFIGURATION FOR ALL API PROVIDERS

To switch providers, change the corresponding environment variable:
- AI_PROVIDER: digitalocean, openai, anthropic
- IMAGE_PROVIDER: fibo, stability, none (none = disable image features)
- VOICE_TTS_PROVIDER: azure, none (none = disable voice features)
- VOICE_STT_PROVIDER: azure, none (none = disable voice features)

No other code changes required!
"""

import os
from typing import Optional
from app.services.ai_providers.base import BaseAIProvider
from app.services.ai_providers.digitalocean import DigitalOceanAIProvider
from app.services.ai_providers.openai import OpenAIProvider
from app.services.ai_providers.anthropic import AnthropicProvider
from app.services.image_providers.base import BaseImageProvider
from app.services.image_providers.fibo import FiboProvider
from app.services.image_providers.stability import StabilityProvider
from app.services.image_providers.none_provider import NoneImageProvider
from app.services.image_providers.pollinations import PollinationsProvider
from app.services.voice_providers.base import BaseTTSProvider, BaseSTTProvider
from app.services.voice_providers.azure_voice import AzureTTSProvider, AzureSTTProvider
from app.services.voice_providers.none_provider import NoneTTSProvider, NoneSTTProvider


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
        "fibo": FiboProvider,
        "stability": StabilityProvider,
        "pollinations": PollinationsProvider,
        "none": NoneImageProvider,
    }

    @classmethod
    def get_image_provider(cls, provider_name: Optional[str] = None) -> BaseImageProvider:
        """
        Get Image provider instance.

        Args:
            provider_name: Override provider (optional).
                          If None, uses IMAGE_PROVIDER env var.

        Returns:
            Configured Image provider instance
        """
        name = provider_name or os.getenv("IMAGE_PROVIDER", "fibo")
        provider_class = cls._image_providers.get(name.lower())

        if not provider_class:
            raise ValueError(
                f"Unknown Image provider: {name}. "
                f"Available: {list(cls._image_providers.keys())}"
            )

        return provider_class()

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

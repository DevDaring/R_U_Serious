"""
Voice Providers Module

This module contains all voice provider implementations for text-to-speech
and speech-to-text functionality.
"""

from .base import (
    BaseTTSProvider,
    BaseSTTProvider
)
from .azure_voice import AzureTTSProvider, AzureSTTProvider

__all__ = [
    "BaseTTSProvider",
    "BaseSTTProvider",
    "AzureTTSProvider",
    "AzureSTTProvider",
]

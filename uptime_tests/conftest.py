"""
Shared test fixtures and helpers.
"""

import ssl

import certifi
import pytest


@pytest.fixture
def ssl_context() -> ssl.SSLContext:
    """
    Create an SSL context so that urllib.request can find HTTPS certificates.
    """
    return ssl.create_default_context(cafile=certifi.where())

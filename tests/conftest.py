import pytest
import os
from unittest.mock import patch
from typing import Generator


@pytest.fixture(autouse=True)
def mock_env() -> Generator[None, None, None]:
    """Mock environment variables for testing.
    
    Yields:
        Generator that provides the mocked environment.
    """
    with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
        yield
import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_env():
    with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
        yield
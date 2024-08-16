"""Top level test suite for needle_haystack."""

import re
import sys
from importlib import reload
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import needle_haystack


class TestInit:
    @patch("importlib.metadata.version", side_effect=PackageNotFoundError)
    def test_version_not_found(self, mock_version):
        """Test `__version__` when the package is not found."""
        if "needle_haystack" in sys.modules:
            del sys.modules["needle_haystack"]
        import needle_haystack

        reload(needle_haystack)
        assert needle_haystack.__version__ == "unknown"

    @patch("importlib.metadata.version")
    def test_version_found(self, mock_version):
        """Test `__version__` when the package is found."""
        mock_version.return_value = "0.1.0"
        if "needle_haystack" in sys.modules:
            del sys.modules["needle_haystack"]
        import needle_haystack

        reload(needle_haystack)
        assert needle_haystack.__version__ == "0.1.0"

    def test_version(self):
        """Test the actual `__version__` value is valid."""
        assert (
            re.match(r"^\d+\.\d+\.\d+$", needle_haystack.__version__)
            or needle_haystack.__version__ == "unknown"
        )

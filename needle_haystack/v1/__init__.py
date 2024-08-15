"""
This module provides NeedleClient class for interacting with Needle API.
"""

from typing import Optional, Dict
import os

from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace

from needle_haystack.utils import make_needle_search_url
from needle_haystack.v1.models import NeedleConfig, NeedleBaseClient
from needle_haystack.v1.collections import NeedleCollections



NEEDLE_DEFAULT_URL = "https://needle-ai.com"


@component
class NeedleClient(NeedleBaseClient):
    """
    A client for interacting with the Needle API.

    This class provides a high-level interface for interacting with the Needle API,
    including managing collections and performing searches.

    Initialize the client with an API key and an optional URL.
    If no API key is provided, the client will use the `NEEDLE_API_KEY` environment variable.
    If no URL is provided, the client will use the default Needle API URL, that is https://needle-ai.com.

    Attributes:
        collections (NeedleCollections): A client for managing collections within the Needle API.
    """

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("NEEDLE_API_KEY"),
        url: Optional[str] = NEEDLE_DEFAULT_URL,
        _search_url: Optional[str] = None,
    ):
        if not _search_url:
            _search_url = make_needle_search_url(url)

        config = NeedleConfig(api_key.resolve_value(), url, search_url=_search_url)
        headers = {"x-api-key": config.api_key}
        super().__init__(config, headers)

        # sub clients
        self.collections = NeedleCollections(config, headers)

    def to_dict(self) -> Dict[str, any]:
        """Serializes the component to a dictionary."""
        return default_to_dict(
            self,
            api_key=self.config.api_key,
            url=self.config.url,
            _search_url=self.config.search_url,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "NeedleClient":
        """Deserializes the component from a dictionary."""
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    def run(self):
        """
        A placeholder run method required for Haystack components.
        This method can be empty if no specific operation is required.
        """
        pass
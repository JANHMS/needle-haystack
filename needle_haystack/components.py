from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace
from typing import Any, Dict, Optional
from needle.v1 import NeedleClient
from needle.v1.models import FileToAdd

@component
class HaystackNeedleCreateCollection:
    """A Haystack-compatible wrapper for creating Needle API collections."""

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("NEEDLE_API_KEY"),
        url: Optional[str] = "https://needle-ai.com",
    ):
        self.client = NeedleClient(api_key.resolve_value(), url)

    @component.output_types(collection_id=str)
    def run(self, name: str) -> Dict[str, str]:
        """Create a new collection in the Needle API."""
        collection = self.client.collections.create(name=name)
        return {"collection_id": collection.id}

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self,
            api_key=self.client.config.api_key,
            url=self.client.config.url,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HaystackNeedleCreateCollection":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

@component
class HaystackNeedleAddFiles:
    """A Haystack-compatible wrapper for adding files to Needle API collections."""

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("NEEDLE_API_KEY"),
        url: Optional[str] = "https://needle-ai.com",
    ):
        self.client = NeedleClient(api_key.resolve_value(), url)

    @component.output_types(file_ids=Dict[str, str])
    def run(self, collection_id: str, file_urls: Dict[str, str]) -> Dict[str, str]:
        """Add files to a collection in the Needle API."""
        files_to_add = [FileToAdd(name=name, url=url) for name, url in file_urls.items()]
        file_statuses = self.client.collections.files.add(collection_id=collection_id, files=files_to_add)

        # Polling for file indexing status
        import time
        while not all(file.status == "indexed" for file in self.client.collections.files.list(collection_id)):
            time.sleep(5)

        return {"file_ids": {file.name: file.id for file in file_statuses}}

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self,
            api_key=self.client.config.api_key,
            url=self.client.config.url,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HaystackNeedleAddFiles":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

@component
class HaystackNeedleSearch:
    """A Haystack-compatible wrapper for performing searches using the Needle API."""

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("NEEDLE_API_KEY"),
        url: Optional[str] = "https://needle-ai.com",
    ):
        self.client = NeedleClient(api_key.resolve_value(), url)

    @component.output_types(results=Dict[str, Any])
    def run(self, collection_id: str, text: str) -> Dict[str, Any]:
        """Perform a search using the Needle API."""
        results = self.client.collections.search(collection_id=collection_id, text=text)
        return {"results": results}

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self,
            api_key=self.client.config.api_key,
            url=self.client.config.url,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HaystackNeedleSearch":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

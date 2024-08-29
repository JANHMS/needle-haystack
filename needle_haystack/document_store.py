"""
Needle Document Store for Haystack
"""

from typing import Any, Dict, List, Optional

from haystack import Document, default_to_dict, default_from_dict
from haystack.document_stores.types import DuplicatePolicy

from needle.v1 import NeedleClient


class NeedleDocumentStore:
    """Document store corresponds to Collections in Needle."""

    def __init__(
        self,
        collection_id: str,
    ):
        self.client = NeedleClient()
        self.collection_id = collection_id
        self.name = self.client.collections.get(collection_id).name

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes this store to a dictionary.
        """
        return default_to_dict(self, collection_id=self.collection_id)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NeedleDocumentStore":
        """
        Deserializes the store from a dictionary.
        """
        return default_from_dict(cls, data)

    def count_documents(self) -> int:
        """
        Returns the number of documents stored.
        """
        stats = self.client.collections.get_stats(collection_id=self.collection_id)
        return stats.chunks_count

    def filter_documents(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        NeedleDocumentStore does not support filtering. This document store can be used only in combination with NeedleEmbeddingRetriever.
        """
        raise NotImplementedError(
            "NeedleDocumentStore does not support filtering. This document store can be used only in combination with NeedleEmbeddingRetriever."
        )

    def write_documents(
        self, documents: List[Document], policy: DuplicatePolicy = DuplicatePolicy.NONE
    ) -> int:
        """
        NeedleDocumentStore does not support writing documents directly.
        Please add files to your collection either via web UI at https://needle-ai.com or via NeedleClient from `needle-python` package.
        """
        raise NotImplementedError(
            "NeedleDocumentStore does not support writing documents directly. Please add files to your collection either via web UI at https://needle-ai.com or via NeedleClient from `needle-python` package."
        )

    def delete_documents(self, document_ids: List[str]) -> None:
        """
        NeedleDocumentStore does not support deleting documents directly.
        Please remove files from your collection either via web UI at https://needle-ai.com or via NeedleClient from `needle-python` package.
        """
        raise NotImplementedError(
            "NeedleDocumentStore does not support deleting documents directly. Please remove files from your collection either via web UI at https://needle-ai.com or via NeedleClient from `needle-python` package."
        )

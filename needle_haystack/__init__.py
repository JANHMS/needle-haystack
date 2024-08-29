"""Needle Haystack integration."""

from importlib.metadata import PackageNotFoundError, version

from needle_haystack.document_store import NeedleDocumentStore
from needle_haystack.needle_embedding_retriever import NeedleEmbeddingRetriever

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["NeedleDocumentStore", "NeedleEmbeddingRetriever"]

"""Needle Haystack integration."""

from importlib.metadata import PackageNotFoundError, version

from .components import NeedleDocumentStore, NeedleRetriever

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["NeedleDocumentStore", "NeedleRetriever"]
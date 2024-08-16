"""Needle Haystack integration."""

from importlib.metadata import PackageNotFoundError, version

from .components import HaystackNeedleCreateCollection, HaystackNeedleAddFiles, HaystackNeedleSearch

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["HaystackNeedleCreateCollection", "HaystackNeedleAddFiles", "HaystackNeedleSearch"]
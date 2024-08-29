from typing import Any, Dict, List, Optional

from haystack import component, Document, default_to_dict, default_from_dict

from needle_haystack.document_store import NeedleDocumentStore


@component
class NeedleEmbeddingRetriever:
    """A Haystack-compatible retriever that interfaces with Needle API collections."""

    def __init__(
        self,
        document_store: NeedleDocumentStore,
    ):
        self.document_store = document_store

    @component.output_types(documents=List[Document])
    def run(
        self,
        text: str,
        max_distance: Optional[float] = None,
        top_k: Optional[int] = None,
    ) -> Dict[str, List[Document]]:
        """
        Retrieves documents from NeedleDocumentStore, based on their dense embeddings.

        Args:
            text (str): The query text.

        Returns:
            Dict[str, List[Document]]: A dictionary containing the retrieved documents.
        """
        results = self.document_store.client.collections.search(
            collection_id=self.document_store.collection_id,
            text=text,
            max_distance=max_distance,
            top_k=top_k,
        )
        documents = [
            Document(content=r.content, meta={"file_id": r.file_id}) for r in results
        ]
        return {"documents": documents}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes this retriever to a dictionary.
        """
        return default_to_dict(self, document_store=self.document_store.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NeedleEmbeddingRetriever":
        """
        Deserializes the retriever from a dictionary.
        """
        document_store = NeedleDocumentStore.from_dict(
            data["init_parameters"]["document_store"]
        )
        data["init_parameters"]["document_store"] = document_store

        return default_from_dict(cls, data)

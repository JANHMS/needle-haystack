"""
This module provides NeedleCollections class for interacting with Needle API's collections endpoint.
"""

from typing import Optional, List, Dict

import requests
from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace

from needle_haystack.v1.models import (
    NeedleConfig,
    NeedleBaseClient,
    Collection,
    Error,
    SearchResult,
)
from needle_haystack.v1.collections.files import NeedleCollectionsFiles


@component
class NeedleCollections(NeedleBaseClient):
    """
    A client for interacting with the Needle API's collections endpoint.

    This class provides methods to create and manage collections within the Needle API.
    It uses a requests session to handle HTTP requests with a default timeout of 120 seconds.
    """

    def __init__(self, config: NeedleConfig, headers: Dict[str, str]):
        super().__init__(config, headers)

        self.endpoint = f"{config.url}/api/v1/collections"
        self.search_endpoint = f"{config.search_url}/api/v1/collections"

        # requests config
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.timeout = 120

        # sub clients
        self.files = NeedleCollectionsFiles(config, headers)

    @component.output_types(collection=Collection)
    def create(self, name: str, file_ids: Optional[List[str]] = None):
        """
        Creates a new collection with the specified name and file IDs.

        Args:
            name (str): The name of the collection.
            file_ids (Optional[List[str]]): A list of file IDs to include in the collection.

        Returns:
            Collection: The created collection object.

        Raises:
            Error: If the API request fails.
        """
        req_body = {"name": name, "file_ids": file_ids}
        resp = self.session.post(f"{self.endpoint}", json=req_body)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        c = body.get("result")
        return {"collection": Collection(**c)}

    @component.output_types(collection=Collection)
    def get(self, collection_id: str):
        """
        Retrieves a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Collection: The retrieved collection object.

        Raises:
            Error: If the API request fails.
        """
        resp = self.session.get(f"{self.endpoint}/{collection_id}")
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        c = body.get("result")
        return {"collection": Collection(**c)}

    @component.output_types(collections=List[Collection])
    def list(self):
        """
        Lists all collections.

        Returns:
            List[Collection]: A list of all collections.

        Raises:
            Error: If the API request fails.
        """
        resp = self.session.get(self.endpoint)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return {"collections": [Collection(**c) for c in body.get("result")]}

    @component.output_types(results=List[SearchResult])
    def search(self, collection_id: str, text: str):
        """
        Searches within a collection based on the provided parameters.

        Args:
            collection_id (str): The ID of the collection to search within.
            text (str): The search text.

        Returns:
            List[SearchResult]: The search results.

        Raises:
            Error: If the API request fails.
        """
        endpoint = f"{self.search_endpoint}/{collection_id}/search"
        req_body = {"text": text}
        resp = self.session.post(endpoint, headers=self.headers, json=req_body)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return {"results": [SearchResult(**c) for c in body.get("result")]}
    
    def run(self):
        """
        A placeholder run method required for Haystack components.
        This method can be empty if no specific operation is required.
        """
        pass

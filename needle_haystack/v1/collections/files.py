from dataclasses import asdict
from typing import List, Dict
import requests

from needle_haystack.v1 import NeedleBaseClient, NeedleConfig
from needle_haystack.v1.models import FileToAdd, Error, CollectionFile
from haystack import component

@component
class NeedleCollectionsFiles(NeedleBaseClient):
    """
    A client for interacting with the Needle API's collection files endpoint.

    This class provides methods to create and manage collection files within the Needle API.
    It uses a requests session to handle HTTP requests with a default timeout of 120 seconds.
    """

    def __init__(self, config: NeedleConfig, headers: Dict[str, str]):
        """
        Initialize the NeedleCollectionsFiles client.

        Args:
            config (NeedleConfig): Configuration object for the Needle API.
            headers (dict): A dictionary of headers to include in the requests.
        """
        super().__init__(config, headers)

        self.collections_endpoint = f"{config.url}/api/v1/collections"

        # requests config
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.timeout = 120

    @component.output_types(files=List[CollectionFile])
    def add(self, collection_id: str, files: List[FileToAdd]) -> List[CollectionFile]:
        """
        Adds files to a specified collection. Added files will be automatically indexed 
        and will be available for search within the collection.

        Args:
            collection_id (str): The ID of the collection to which files will be added.
            files (list[FileToAdd]): A list of FileToAdd objects representing the files to be added.

        Returns:
            list[CollectionFile]: A list of CollectionFile objects representing the added files.

        Raises:
            Error: If the API request fails.
        """
        endpoint = f"{self.collections_endpoint}/{collection_id}/files"
        req_body = {"files": [asdict(f) for f in files]}
        resp = self.session.post(endpoint, json=req_body)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return [CollectionFile(**cf) for cf in body.get("result")]

    @component.output_types(files=List[CollectionFile])
    def list(self, collection_id: str) -> List[CollectionFile]:
        """
        Lists all files in a specified collection.

        Args:
            collection_id (str): The ID of the collection whose files will be listed.

        Returns:
            list[CollectionFile]: A list of CollectionFile objects representing the files in the collection.

        Raises:
            Error: If the API request fails.
        """
        endpoint = f"{self.collections_endpoint}/{collection_id}/files"
        resp = self.session.get(endpoint)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return [CollectionFile(**cf) for cf in body.get("result")]

    def run(self):
        """
        A placeholder run method required for Haystack components.
        This method can be empty if no specific operation is required.
        """
        pass

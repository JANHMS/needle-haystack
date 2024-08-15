import pytest
from unittest.mock import MagicMock, patch
from needle_haystack.v1.collections import NeedleCollections
from needle_haystack.v1.models import NeedleConfig, Collection, Error
from needle_haystack.v1.collections.files import NeedleCollectionsFiles

@pytest.fixture
def mock_config():
    return NeedleConfig(api_key="test-api-key", url="https://needle-ai.com", search_url="https://needle-ai.com/search")

@pytest.fixture
def mock_headers():
    return {"x-api-key": "test-api-key"}

@pytest.fixture
def mock_collections():
    with patch("needle_haystack.v1.collections.NeedleCollections") as mock:
        yield mock

@pytest.fixture
def mock_files():
    with patch("needle_haystack.v1.collections.files.NeedleCollectionsFiles") as mock:
        yield mock

class TestNeedleCollections:

    @pytest.fixture
    def client(self, mock_collections, mock_config, mock_headers):
        return NeedleCollections(config=mock_config, headers=mock_headers)

    def test_create(self, client, mock_collections):
        # Mock the requests.Session.post method
        client.session.post = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": {"id": "123", "name": "Test Collection"}}))
        
        result = client.create(name="Test Collection", file_ids=["file1", "file2"])
        assert isinstance(result["collection"], Collection)
        assert result["collection"].id == "123"
        assert result["collection"].name == "Test Collection"

    def test_create_failure(self, client, mock_collections):
        # Mock the requests.Session.post method to simulate an error
        client.session.post = MagicMock(return_value=MagicMock(status_code=400, json=lambda: {"error": {"message": "Error creating collection"}}))
        
        with pytest.raises(Error):
            client.create(name="Test Collection", file_ids=["file1", "file2"])

    def test_get(self, client, mock_collections):
        # Mock the requests.Session.get method
        client.session.get = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": {"id": "123", "name": "Test Collection"}}))
        
        result = client.get(collection_id="123")
        assert isinstance(result["collection"], Collection)
        assert result["collection"].id == "123"
        assert result["collection"].name == "Test Collection"

    def test_list(self, client, mock_collections):
        # Mock the requests.Session.get method
        client.session.get = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": [{"id": "123", "name": "Test Collection"}]}))
        
        result = client.list()
        assert isinstance(result["collections"], list)
        assert len(result["collections"]) == 1
        assert isinstance(result["collections"][0], Collection)

    def test_search(self, client, mock_collections):
        # Mock the requests.Session.post method
        client.session.post = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": [{"id": "1", "content": "Search Result"}]}))
        
        result = client.search(collection_id="123", text="search text")
        assert isinstance(result["results"], list)
        assert len(result["results"]) == 1
        assert result["results"][0].id == "1"
        assert result["results"][0].content == "Search Result"

class TestNeedleCollectionsFiles:

    @pytest.fixture
    def client(self, mock_files, mock_config, mock_headers):
        return NeedleCollectionsFiles(config=mock_config, headers=mock_headers)

    def test_add(self, client, mock_files):
        # Mock the requests.Session.post method
        client.session.post = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": [{"id": "file1", "name": "File 1"}]}))
        
        files_to_add = [FileToAdd(id="file1", name="File 1")]
        result = client.add(collection_id="123", files=files_to_add)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CollectionFile)
        assert result[0].id == "file1"
        assert result[0].name == "File 1"

    def test_add_failure(self, client, mock_files):
        # Mock the requests.Session.post method to simulate an error
        client.session.post = MagicMock(return_value=MagicMock(status_code=400, json=lambda: {"error": {"message": "Error adding files"}}))
        
        files_to_add = [FileToAdd(id="file1", name="File 1")]
        with pytest.raises(Error):
            client.add(collection_id="123", files=files_to_add)

    def test_list(self, client, mock_files):
        # Mock the requests.Session.get method
        client.session.get = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {"result": [{"id": "file1", "name": "File 1"}]}))
        
        result = client.list(collection_id="123")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CollectionFile)
        assert result[0].id == "file1"
        assert result[0].name == "File 1"

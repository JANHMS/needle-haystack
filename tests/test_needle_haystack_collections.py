import pytest
from unittest.mock import MagicMock, patch
from needle_haystack.v1.collections import NeedleCollections
from needle_haystack.v1.models import NeedleConfig, Collection, Error, SearchResult
from needle_haystack.v1.collections.files import NeedleCollectionsFiles

# Mock NeedleCollectionsFiles component
class MockNeedleCollectionsFiles:
    def __init__(self, config, headers):
        pass

@pytest.fixture
def mock_config():
    return NeedleConfig(api_key="test-api-key", url="https://needle-ai.com", search_url="https://needle-ai.com/search")

@pytest.fixture
def mock_headers():
    return {"x-api-key": "test-api-key"}

@pytest.fixture
def client(mock_config, mock_headers):
    with patch("needle_haystack.v1.collections.NeedleCollectionsFiles", MockNeedleCollectionsFiles):
        return NeedleCollections(config=mock_config, headers=mock_headers)

class TestNeedleCollections:

    @pytest.fixture(autouse=True)
    def setup_method(self, client):
        # Mock the requests.Session methods on the client instance
        self.client = client
        self.client.session = MagicMock()

    def test_create(self):
        # Mock the requests.Session.post method
        self.client.session.post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"result": {"id": "123", "name": "Test Collection"}}
        )
        
        result = self.client.create(name="Test Collection", file_ids=["file1", "file2"])
        assert isinstance(result["collection"], Collection)
        assert result["collection"].id == "123"
        assert result["collection"].name == "Test Collection"

    def test_create_failure(self):
        # Mock the requests.Session.post method to simulate an error
        self.client.session.post.return_value = MagicMock(
            status_code=400,
            json=lambda: {"error": {"message": "Error creating collection"}}
        )
        
        with pytest.raises(Error):
            self.client.create(name="Test Collection", file_ids=["file1", "file2"])

    def test_get(self):
        # Mock the requests.Session.get method
        self.client.session.get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"result": {"id": "123", "name": "Test Collection"}}
        )
        
        result = self.client.get(collection_id="123")
        assert isinstance(result["collection"], Collection)
        assert result["collection"].id == "123"
        assert result["collection"].name == "Test Collection"

    def test_list(self):
        # Mock the requests.Session.get method
        self.client.session.get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"result": [{"id": "123", "name": "Test Collection"}]}
        )
        
        result = self.client.list()
        assert isinstance(result["collections"], list)
        assert len(result["collections"]) == 1
        assert isinstance(result["collections"][0], Collection)

    def test_search(self):
        # Mock the requests.Session.post method
        self.client.session.post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"result": [{"id": "1", "content": "Search Result"}]}
        )
        
        result = self.client.search(collection_id="123", text="search text")
        assert isinstance(result["results"], list)
        assert len(result["results"]) == 1
        assert result["results"][0].id == "1"
        assert result["results"][0].content == "Search Result"

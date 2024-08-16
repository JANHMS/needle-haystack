# Needle Haystack Integration

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI/CD   | [![Tests](https://github.com/JANHMS/needle-haystack/actions/workflows/test.yml/badge.svg)](https://github.com/JANHMS/needle-haystack/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/JANHMS/needle-haystack)](https://codecov.io/gh/JANHMS/needle-haystack) [![Tests](https://github.com/JANHMS/needle-haystack/actions/workflows/lint.yml/badge.svg)](https://github.com/JANHMS/needle-haystack/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/needle-haystack)](https://pypi.org/project/needle-haystack/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/needle-haystack?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/needle-haystack?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/JANHMS/needle-haystack?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                                 |

---

## Installation

This project resides in the Python Package Index (PyPI), so it can easily be installed with `pip`:

```console
pip install needle-haystack
```

## Usage

The Needle Haystack integration provides components for working with the Needle API. These components can be used to create collections, add files to collections, and perform searches.

### Configure your API keys

- Get your `NEEDLE_API_KEY` from [Developer settings](https://needle-ai.com/dashboard/settings/developer).

```
os.environ["NEEDLE_API_KEY"] = ""
```

- Get OpenAPI key from [OpenAI](https://platform.openai.com/)

```
os.environ["OPENAI_API_KEY"] = ""
```

### Create a Collection in Needle

```
from haystack import Pipeline
from needle_haystack import HaystackNeedleCreateCollection

# Initialize components
create_collection = HaystackNeedleCreateCollection()

# Define the pipeline
pipeline = Pipeline()
pipeline.add_component(name="create_collection", instance=create_collection)

# Define inputs for the pipeline
inputs = {
    "create_collection": {"name": "Tech Trends"}
}

# Run the pipeline
collection = pipeline.run(data=inputs)
collection
```

### Add Files to a Collection and Search

```
from haystack import Pipeline
from needle_haystack import HaystackNeedleAddFiles, HaystackNeedleSearch

# Initialize components
add_files = HaystackNeedleAddFiles()
search = HaystackNeedleSearch()

# Define the pipeline
pipeline_add_files_and_search = Pipeline()
pipeline_add_files_and_search.add_component(name="add_files", instance=add_files)
pipeline_add_files_and_search.add_component(name="search", instance=search)

# Define inputs for the pipeline
inputs = {
    "add_files": {
        "collection_id": collection['create_collection']['collection_id'],
        "file_urls": {
            "tech-radar-30.pdf": "https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2024/04/tr_technology_radar_vol_30_en.pdf"
        }
    },
    "search": {
        "collection_id": collection['create_collection']['collection_id'],
        "text": "What techniques moved into adopt in this volume of technology radar?"
    }
}

# Run Pipeline
results = pipeline_add_files_and_search.run(data=inputs)
results
```

### Complete Your RAG Pipeline

To compose a human-friendly answer, you can use an LLM provider of your choice. For demo purposes, this example uses OpenAI:

```
from openai import OpenAI

prompt = "What techniques moved into adopt in this volume of technology radar?"

system_messages = [{"role": "system", "content": r.content} for r in results["search"]["results"]]
user_message = {
    "role": "system",
    "content": f"""
        Only answer the question based on the provided results data.
        If there is no data in the provided data for the question, do not try to generate an answer.
        This is the question: {prompt}
""",
}

openai_client = OpenAI()
answer = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        *system_messages,
        user_message,
    ],
)

print(answer.choices[0].message.content)
# -> Retrieval-Augmented Generation (RAG)
```

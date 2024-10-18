# Robyn Reranking Service Setup Guide

This guide will walk you through the process of setting up and running the reranking service using Robyn's project creator CLI and attrs.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Step 1: Install Robyn

First, install Robyn globally:

```bash
pip install robyn
```

## Step 2: Create a new Robyn project

Use Robyn's project creator CLI to initialize your project:

```bash
robyn new reranking-service
cd reranking-service
```

This command creates a new directory with a basic Robyn project structure.

## Step 3: Set up a virtual environment

It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS and Linux:
source venv/bin/activate
```

## Step 4: Install additional required packages

Install attrs and your reranker package:

```bash
pip install attrs your-reranker-package
```

Replace `your-reranker-package` with the actual package name for your reranker implementation.

## Step 5: Modify the main.py file

Open the `main.py` file created by Robyn and replace its contents with our reranking service code:

```python
from robyn import Robyn, jsonify
from attrs import define, field
import attr
from typing import List
import json
import time
from your_reranker import CPUFriendlyReranker  # Replace with your actual reranker import

app = Robyn(__file__)

@define
class Document:
    id: str
    content: str

@define
class RerankRequest:
    query: str
    documents: List[Document]
    model: str = field(default="default_model")
    top_k: int = field(default=5)

@define
class RankedDocument:
    id: str
    score: float
    original_rank: int
    new_rank: int

@define
class RerankResponse:
    reranked_documents: List[RankedDocument]
    model_used: str
    processing_time: float

def validate_rerank_request(data):
    try:
        documents = [Document(**doc) for doc in data['documents']]
        return RerankRequest(
            query=data['query'],
            documents=documents,
            model=data.get('model', 'default_model'),
            top_k=data.get('top_k', 5)
        )
    except (KeyError, TypeError, attr.exceptions.BadArgument) as e:
        raise ValueError(f"Invalid request data: {str(e)}")

@app.post("/v1/rerank")
async def rerank(request):
    try:
        data = json.loads(request.body)
        rerank_request = validate_rerank_request(data)
        
        reranker = CPUFriendlyReranker(model_name=rerank_request.model)
        
        start_time = time.time()
        reranked = reranker.rerank(rerank_request.query, 
                                   [attr.asdict(doc) for doc in rerank_request.documents], 
                                   top_k=rerank_request.top_k)
        processing_time = time.time() - start_time
        
        response = RerankResponse(
            reranked_documents=[
                RankedDocument(
                    id=doc['id'],
                    score=doc['score'],
                    original_rank=i,
                    new_rank=j
                ) for j, (i, doc) in enumerate(reranked)
            ],
            model_used=rerank_request.model,
            processing_time=processing_time
        )
        
        return jsonify(attr.asdict(response)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.start(port=8000)
```

Make sure to replace `from your_reranker import CPUFriendlyReranker` with the actual import statement for your reranker implementation.

## Step 6: Configure the reranker

If your reranker requires any configuration (e.g., model paths, parameters), set these up according to your specific implementation.

## Step 7: Run the service

Start the reranking service:

```bash
python app.py
```

The service should now be running on `http://localhost:8000`.

## Step 8: Test the service

Test the service using curl or any HTTP client:

```bash
curl -X POST http://localhost:8000/v1/rerank \
-H "Content-Type: application/json" \
-d '{
  "query": "example search query",
  "documents": [
    {
      "id": "doc1",
      "content": "This is the content of document 1"
    },
    {
      "id": "doc2",
      "content": "This is the content of document 2"
    }
  ],
  "model": "default_model",
  "top_k": 2
}'
```

## Step 9: Integrate with your application

To use this reranking service in your ContentCreationAgent, make HTTP requests to the `/v1/rerank` endpoint:

```python
import requests

class ContentCreationAgent:
    def __init__(self, reranker_url):
        self.reranker_url = reranker_url

    async def rerank_documents(self, query, documents):
        response = requests.post(
            f"{self.reranker_url}/v1/rerank",
            json={
                "query": query,
                "documents": documents,
                "top_k": 5  # Adjust as needed
            }
        )
        response.raise_for_status()
        return response.json()["reranked_documents"]

    # Use this method in your generate_response method
```

## Troubleshooting

- If you encounter import errors, ensure all required packages are installed and your virtual environment is activated.
- If the service fails to start, check that port 8000 is not already in use.
- For reranker-specific issues, refer to the documentation of your reranker implementation.

## Next Steps

- Implement proper error handling and logging in the service.
- Add authentication if the service will be publicly accessible.
- Consider containerizing the service using Docker for easier deployment.

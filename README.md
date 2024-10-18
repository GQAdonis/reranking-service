# Reranking Service

This repository contains a CPU-friendly reranking service designed to improve search result relevance. The service uses a lightweight reranking model to efficiently reorder a list of documents based on their relevance to a given query.

## Purpose

The main purpose of this service is to provide a fast and efficient way to rerank search results or any list of documents. It's particularly useful in scenarios where:

1. You need to improve the relevance of search results without the computational overhead of more complex models.
2. You want to rerank documents on CPU, making it more accessible and cost-effective for various deployment environments.
3. You need a reranking solution that can be easily integrated into existing search pipelines or content recommendation systems.

## Key Features

- CPU-friendly reranking: Optimized for performance on CPU, making it suitable for a wide range of deployment scenarios.
- FastAPI integration: Uses FastAPI for creating a robust and efficient API service.
- Customizable model: Allows specifying different reranking models based on your needs.
- Flexible input/output: Accepts a query and a list of documents, returning reranked results with scores.

## Project Structure

- `app.py`: The main FastAPI application file containing the API endpoints.
- `cpu_friendly_reranker.py`: Implementation of the CPU-friendly reranking model.
- `rerank_types.py`: Pydantic models for request/response typing and validation.
- `requirements.txt`: List of Python dependencies for the project (generated from Poetry for compatibility).
- `pyproject.toml`: Project metadata and dependencies managed by Poetry.
- `Dockerfile`: Instructions for building a Docker container for the service.
- `.dockerignore`: Specifies files and directories to be excluded from the Docker build context.
- `.env`: Environment variables for the project (not tracked in version control).

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/reranking-service.git
   cd reranking-service
   ```

2. This project uses Poetry for dependency management. If you don't have Poetry installed, you can install it by following the instructions at https://python-poetry.org/docs/#installation

3. Install the project dependencies:
   ```
   poetry install
   ```

4. Activate the virtual environment:
   ```
   poetry shell
   ```

5. Set up environment variables:
   - Copy the `.env.example` file to `.env` (if it exists)
   - Update the `.env` file with your specific configuration

6. Run the FastAPI server:
   ```
   uvicorn app:app --reload
   ```

The service will be available at `http://localhost:8000`.

## API Usage

### Rerank Endpoint

**POST** `/v1/rerank`

Request body:
```json
{
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
  "top_k": 5
}
```

Response:
```json
{
  "reranked_documents": [
    {
      "id": "doc2",
      "score": 0.85,
      "original_rank": 1,
      "new_rank": 0
    },
    {
      "id": "doc1",
      "score": 0.75,
      "original_rank": 0,
      "new_rank": 1
    }
  ],
  "model_used": "default_model",
  "processing_time": 0.0123
}
```

## Docker Support

To build and run the service using Docker:

1. Build the Docker image:
   ```
   docker build -t reranking-service .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 reranking-service
   ```

## Contributing

Contributions to improve the reranking service are welcome. Please feel free to submit issues and pull requests.

## License

[Specify the license under which this project is released]

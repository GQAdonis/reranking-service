# CPU-Friendly Reranking Service

This repository contains a high-performance, CPU-friendly reranking service designed to improve search result relevance. The service uses a lightweight reranking model to efficiently reorder a list of documents based on their relevance to a given query.

## Purpose

The main purpose of this service is to provide a fast and efficient way to rerank search results or any list of documents. It's particularly useful in scenarios where:

1. You need to improve the relevance of search results without the computational overhead of more complex models.
2. You want to rerank documents on CPU, making it more accessible and cost-effective for various deployment environments.
3. You need a reranking solution that can be easily integrated into existing search pipelines or content recommendation systems.

## Key Features

- CPU-friendly reranking: Optimized for performance on CPU, making it suitable for a wide range of deployment scenarios.
- Robyn integration: Uses Robyn, a fast ASGI web framework with Rust integration capabilities, for creating a high-performance API service.
- attrs for data validation: Utilizes attrs for efficient and clean data class definitions and validation.
- Customizable model: Allows specifying different reranking models based on your needs.
- Flexible input/output: Accepts a query and a list of documents, returning reranked results with scores.

## Architectural Assessment

This reranking service is designed with a focus on high performance, CPU-friendly execution, and a balance between speed and accuracy:

1. **High Performance**: 
   - The service uses Robyn, a fast ASGI web framework that allows for Rust integration, providing excellent performance for web serving.
   - The reranker is initialized once at startup, reducing overhead for each request.
   - JSON parsing and response creation are optimized for speed.

2. **CPU-Friendly Execution**:
   - The `CPUFriendlyReranker` class (in `cpu_friendly_reranker.py`) is designed to work efficiently on CPU-only machines.
   - The default model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) is chosen for its balance of speed and accuracy, suitable for CPU execution.

3. **Balance of Speed and Accuracy**:
   - The choice of a MiniLM model provides a good trade-off between reranking quality and computational requirements.
   - The `top_k` parameter allows users to control the number of documents reranked, further balancing speed and accuracy needs.

4. **Scalability and Flexibility**:
   - Environment variables are used for configuration, allowing easy deployment across different environments.
   - The service includes a health check endpoint for monitoring in production environments.
   - The architecture allows for easy swapping of the underlying reranking model if needed.

5. **Error Handling and Logging**:
   - Comprehensive error handling and logging are implemented, aiding in debugging and monitoring.

This architecture ensures that the service can provide fast, accurate reranking even on machines with limited or no GPU capabilities, making it versatile for various deployment scenarios.

## Project Structure

- `app.py`: The main Robyn application file containing the API endpoints.
- `cpu_friendly_reranker.py`: Implementation of the CPU-friendly reranking model.
- `rerank_types.py`: attrs classes for request/response typing and validation.
- `requirements.txt`: List of Python dependencies for the project.
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

6. Run the Robyn server:
   ```
   python app.py
   ```

The service will be available at `http://localhost:8080` by default.

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
  "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "top_k": 5
}
```

Response:
```json
{
  "reranked_documents": [
    {
      "id": "doc2",
      "content": "This is the content of document 2",
      "score": 0.85,
      "original_rank": 1,
      "new_rank": 0
    },
    {
      "id": "doc1",
      "content": "This is the content of document 1",
      "score": 0.75,
      "original_rank": 0,
      "new_rank": 1
    }
  ],
  "model_used": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "processing_time": 0.0123
}
```

### Health Check Endpoint

**GET** `/health`

Response:
```json
{
  "status": "healthy"
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
   docker run -p 8080:8080 reranking-service
   ```

## Contributing

Contributions to improve the reranking service are welcome. Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

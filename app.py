from robyn import Robyn, jsonify, ALLOW_CORS, Response
import attr
from typing import Dict, Any
import json
import time
import os
import logging
from cpu_friendly_reranker import CPUFriendlyReranker

from dotenv import load_dotenv
load_dotenv()

from rerank_types import Document, RankedDocument, RerankRequest, RerankResponse

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

env = {
    'PORT': int(os.getenv('PORT', 8080)),
    'TRANSFORMER_MODEL': os.getenv('TRANSFORMER_MODEL', 'cross-encoder/ms-marco-MiniLM-L-6-v2'),
}

app = Robyn(__file__)
ALLOW_CORS(app, origins=["*"])

# Initialize the reranker once
reranker = CPUFriendlyReranker(model_name=env['TRANSFORMER_MODEL'])

def validate_rerank_request(data):
    try:
        documents = [Document(id=doc['id'], content=doc['content']) for doc in data['documents']]
        return RerankRequest(
            query=data['query'],
            documents=documents,
            model=data.get('model', env['TRANSFORMER_MODEL']),
            top_k=data.get('top_k', 5)
        )
    except (KeyError, TypeError, attr.exceptions.BadArgument) as e:
        raise ValueError(f"Invalid request data: {str(e)}")

def create_response(data: Any, status_code: int, headers: Dict[str, str] = None) -> Response:
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"
    return Response(status_code, headers, json.dumps(data))

@app.post("/v1/rerank")
async def rerank(request):
    try:
        data = json.loads(request.body)
        log.debug(f"Received request data: {data}")
        
        rerank_request = validate_rerank_request(data)
        log.debug(f"Validated rerank request: {rerank_request}")
        
        start_time = time.time()
        reranked = reranker.rerank(rerank_request.query, 
                                   rerank_request.documents,
                                   top_k=rerank_request.top_k)
        processing_time = time.time() - start_time
        
        log.debug(f"Reranked results: {reranked}")
        
        reranked_documents = [
            RankedDocument(
                id=doc.id,
                content=doc.content,
                score=doc.score,
                original_rank=i,
                new_rank=i
            ) for i, doc in enumerate(reranked)
        ]
        
        response = RerankResponse(
            reranked_documents=reranked_documents,
            model_used=rerank_request.model,
            processing_time=processing_time
        )
        
        log.debug(f"Final response: {attr.asdict(response)}")
        
        return create_response(attr.asdict(response), 200)
    except ValueError as e:
        log.error(f"ValueError: {str(e)}")
        return create_response({"error": str(e)}, 400)
    except Exception as e:
        log.exception("An error occurred during reranking")
        return create_response({"error": "Internal server error"}, 500)

@app.get("/health")
async def health_check(request):
    return create_response({"status": "healthy"}, 200)

if __name__ == "__main__":
    app.start(host="0.0.0.0", port=env['PORT'])
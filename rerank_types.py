from attrs import define, field
from typing import List

@define
class Document:
    id: str
    content: str
    score: float = field(default=0.0)

@define
class RankedDocument:
    id: str
    content: str
    score: float
    original_rank: int
    new_rank: int

@define
class RerankRequest:
    query: str
    documents: List[Document]
    model: str = field(default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    top_k: int = field(default=5)

@define
class RerankResponse:
    reranked_documents: List[RankedDocument]
    model_used: str
    processing_time: float
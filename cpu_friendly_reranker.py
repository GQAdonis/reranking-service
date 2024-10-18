from sentence_transformers import CrossEncoder
from typing import List
from rerank_types import Document
import os
from transformers import set_cache_dir

class CPUFriendlyReranker:
    def __init__(self, model_name: str):
        # Set the cache directory
        cache_dir = '/app/models'
        os.makedirs(cache_dir, exist_ok=True)
        set_cache_dir(cache_dir)
        
        # Initialize the model with the cache directory
        self.model = CrossEncoder(model_name, cache_folder=cache_dir)
    
    def rerank(self, query: str, documents: List[Document], top_k: int = 5) -> List[Document]:
        pairs = [[query, doc.content] for doc in documents]
        scores = self.model.predict(pairs)
        
        for doc, score in zip(documents, scores):
            doc.score = float(score)
        
        ranked_documents = sorted(documents, key=lambda x: x.score, reverse=True)
        return ranked_documents[:top_k]

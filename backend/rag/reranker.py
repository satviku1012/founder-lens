from typing import List
from langchain_core.documents import Document

class Reranker:
    def __init__(self):
        pass

    def rerank(self, query: str, documents: List[Document], top_k: int = 5) -> List[Document]:
        """
        A placeholder for a real re-ranker.
        In a production app, use Cohere or a Cross-Encoder model.
        For now, this simply trims to the top K chunks since Pinecone already gives us sorted context.
        """
        # A simple pass-through that slices the top_k.
        return documents[:top_k]
    
    def format_docs(self, docs: List[Document]) -> str:
        """Helper to format docs for printing or injecting."""
        return "\n\n".join(
            f"Source: {doc.metadata.get('title')} ({doc.metadata.get('url')})\n{doc.page_content}" 
            for doc in docs
        )

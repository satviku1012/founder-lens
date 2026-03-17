from typing import Dict, Any
from rag.retriever import Retriever
from rag.reranker import Reranker
from rag.agent import RAGAgent

class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.reranker = Reranker()
        self.agent = RAGAgent()

    def run_query_stream(self, question: str):
        """End-to-end RAG stream."""
        # 1. Retrieve
        retriever_chain = self.retriever.get_retriever(k=25)
        raw_docs = retriever_chain.invoke(question)

        # 2. Rerank
        top_docs = self.reranker.rerank(question, raw_docs, top_k=6)

        # 3. Collect Citations metadata to pass alongside stream
        citations = []
        for i, doc in enumerate(top_docs):
            if doc.metadata.get("url"):
                citations.append({
                    "id": i + 1,
                    "title": doc.metadata.get("title", "Source"),
                    "url": doc.metadata.get("url")
                })

        # 4. Agent Generator stream
        stream = self.agent.generate_answer(question, top_docs)
        return stream, citations

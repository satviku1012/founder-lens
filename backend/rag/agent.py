import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List
from langchain_core.documents import Document

class RAGAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            temperature=0.0,
            streaming=True
        )

    def generate_answer(self, query: str, context_docs: List[Document]):
        """Runs the LLM model to answer based on contexts."""
        # Extract context text and build citations
        context_text = "\n\n".join([
            f"[{i+1}] {doc.metadata.get('title', 'Unknown')} ({doc.metadata.get('url', '')})\n{doc.page_content}"
            for i, doc in enumerate(context_docs)
        ])

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert startup analyst. Answer the user's question about startup failures clearly and accurately " 
                       "using ONLY the provided postmortem documents. Cite your sources using the [number] format in your text."),
            ("user", "Context:\n{context}\n\nQuestion: {question}")
        ])

        chain = prompt | self.llm | StrOutputParser()
        
        # We can yield chunks for streaming, or return full generator
        return chain.stream({
            "context": context_text,
            "question": query
        })

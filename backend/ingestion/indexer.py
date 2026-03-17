import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from typing import List, Dict
import pinecone

class Indexer:
    def __init__(self):
        # Requires environment variables configured
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "startup-postmortems")
        
        # We rely on LangChain's wrapper, but check Pinecone is set up
        # The PINECONE_API_KEY environment variable is required
        
    def index_chunks(self, chunks: List[Dict[str, str]]):
        """Index chunk dictionaries into Pinecone."""
        if not chunks:
            return
            
        docs = [
            Document(page_content=c["text"], metadata={"url": c["url"], "title": c["title"]})
            for c in chunks
        ]
        
        print(f"Indexing {len(docs)} documents into Pinecone index '{self.index_name}'...")
        PineconeVectorStore.from_documents(
            docs, 
            self.embeddings, 
            index_name=self.index_name
        )
        print("Indexing complete.")

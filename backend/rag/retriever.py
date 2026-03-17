import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import AzureOpenAIEmbeddings

class Retriever:
    def __init__(self):
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "startup-postmortems")
        self.vector_store = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )

    def get_retriever(self, k: int = 20):
        """Returns the LangChain retriever."""
        # Retrieve top 20-30 chunks to pass to reranker
        return self.vector_store.as_retriever(search_kwargs={"k": k})

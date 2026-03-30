from dotenv import load_dotenv
load_dotenv()
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from rag.pipeline import RAGPipeline

app = FastAPI(title="Startup Postmortem RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

# Attempt to load pipeline if variables exist
pipeline = None
try:
    pipeline = RAGPipeline()
except Exception as e:
    print(f"Warning: RAG Pipeline not initialized: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query")
async def query_postmortems(req: QueryRequest):
    if pipeline is None:
        return {"error": "Pipeline not configured (missing environment variables)."}
        
    stream, citations_data = pipeline.run_query_stream(req.question)
    
    # Wait for the stream to finish and combine into one answer
    full_answer = "".join([chunk for chunk in stream])
            
    return {"answer": full_answer, "citations": citations_data}

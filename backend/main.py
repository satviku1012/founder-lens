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
    
    # We yield citations first as a JSON chunk, then stream the answer
    def event_stream():
        # First yield the citations
        citations_json = json.dumps({"type": "citations", "data": citations_data})
        yield f"data: {citations_json}\n\n"
        
        # Then stream the answer chunks
        for chunk in stream:
            chunk_json = json.dumps({"type": "chunk", "text": chunk})
            yield f"data: {chunk_json}\n\n"
            
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(event_stream(), media_type="text/event-stream")

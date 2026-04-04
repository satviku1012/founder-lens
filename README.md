# FounderLens

AI-powered Q&A with cited sources.

## Usage
```bash
curl -X POST "https://founder-lens-backend.victoriousstone-f6872aff.eastus.azurecontainerapps.io/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "YOUR QUESTION HERE"}'
```

Or test all endpoints in the browser:  
https://founder-lens-backend.victoriousstone-f6872aff.eastus.azurecontainerapps.io/docs

## Stack

- **Backend:** FastAPI
- **Agent:** LangChain
- **DB:** Pinecone
- **Deploy:** Azure

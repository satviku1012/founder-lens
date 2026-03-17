from typing import List, Dict

class TextChunker:
    def __init__(self, chunk_size=500, overlap=50):
        # Using word count for simplicity as requested, but standard Langchain splitters can be used too.
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, raw_text: str) -> str:
        """Basic text cleanup."""
        return " ".join(raw_text.split())

    def chunk_document(self, doc: Dict[str, str]) -> List[Dict[str, str]]:
        """Split document text into overlapping chunks of words."""
        clean = self.clean_text(doc["text"])
        words = clean.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            if not chunk_words:
                break
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "text": chunk_text,
                "url": doc["url"],
                "title": doc["title"]
            })
        return chunks

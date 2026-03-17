import os
from dotenv import load_dotenv

# Load env vars (for Pinecone / OpenAI keys) before anything else
load_dotenv()

from ingestion.scraper import PostmortemScraper
from ingestion.chunker import TextChunker
from ingestion.indexer import Indexer

# A sample list of startup postmortem URLs
# You can add or replace these with actual postmortem links.
STARTUP_POSTMORTEM_URLS = [
    "https://blossomstreetventures.medium.com/a-great-startup-post-mortem-074185c136b0",
    "https://www.cbinsights.com/research/startup-failure-post-mortem/"
]

def run_ingestion_pipeline():
    print("Initializing ingestion pipeline components...")
    try:
        scraper = PostmortemScraper()
        chunker = TextChunker(chunk_size=500, overlap=50)
        indexer = Indexer()
    except Exception as e:
        print(f"Error initializing components. Ensure all environment variables are set: {e}")
        return

    all_chunks = []

    print(f"Starting to process {len(STARTUP_POSTMORTEM_URLS)} URLs...")
    for idx, url in enumerate(STARTUP_POSTMORTEM_URLS, 1):
        print(f"\n[{idx}/{len(STARTUP_POSTMORTEM_URLS)}] Processing: {url}")
        
        # 1. Scrape
        print("  Scraping...")
        doc = scraper.scrape_url(url)
        if not doc["text"]:
            print("  Skipping (no content found or error fetching).")
            continue
            
        print(f"  Scraped successfully. Title: {doc['title']}")
        
        # 2. Chunk
        print("  Chunking...")
        chunks = chunker.chunk_document(doc)
        print(f"  Created {len(chunks)} chunks.")
        
        all_chunks.extend(chunks)

    # 3. Index
    if all_chunks:
        print(f"\nStarting indexing of {len(all_chunks)} total chunks...")
        try:
            indexer.index_chunks(all_chunks)
            print("Pipeline completed successfully!")
        except Exception as e:
            print(f"Error during indexing: {e}")
    else:
        print("\nNo chunks were created. Skipping indexing.")

if __name__ == "__main__":
    run_ingestion_pipeline()

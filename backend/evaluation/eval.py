import sys
import os

# Add the root project path to Python path so we can import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.rag.pipeline import RAGPipeline

def run_evaluation():
    """
    Test a set of questions to evaluate retrieval accuracy and generation quality.
    Note: Requires Pinecone index to be populated and endpoints configured.
    """
    test_questions = [
        "Why did Quibi fail?",
        "What are the most common reasons startups run out of cash?",
        "How does a lack of product-market fit lead to failure?"
    ]
    
    print("Initializing Pipeline...")
    try:
        pipeline = RAGPipeline()
    except Exception as e:
        print(f"Skipping evaluation (missing config or environment): {e}")
        return

    for q in test_questions:
        print(f"\n--- Question: {q} ---")
        try:
            stream, citations = pipeline.run_query_stream(q)
            
            print("Answer:", end=" ")
            for chunk in stream:
                print(chunk, end="")
            print("\n")
            
            print("Citations:")
            for cite in citations:
                print(f" - [{cite['id']}] {cite['title']} ({cite['url']})")
        except Exception as e:
            print(f"Error querying '{q}': {e}")

if __name__ == "__main__":
    run_evaluation()

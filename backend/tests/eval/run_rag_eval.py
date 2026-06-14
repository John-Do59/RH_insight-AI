import json
import os
import asyncio
from typing import List

# Import LLM and Embeddings for Evaluation
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.rag.vector_store import get_embeddings
from backend.app.services.chat_service import chat_service

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_precision,
    context_recall,
)

async def generate_rag_responses(dataset_items: List[dict]):
    """
    For each item in the dataset, run the RAG pipeline to get `answer` and `contexts`.
    """
    results = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }
    
    print(f"Generating answers for {len(dataset_items)} questions...")
    for i, item in enumerate(dataset_items):
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        # We process the question using our chat service
        # Since it streams, we collect all tokens
        response_tokens = []
        async for token in chat_service.process_question(question=question):
            response_tokens.append(token)
            
        answer = "".join(response_tokens)
        
        # For evaluation purposes, we should ideally extract the retrieved contexts
        # from the state. Since chat_service doesn't expose the context directly in the stream,
        # we will manually call the vector store to simulate the context retrieval
        # for the sake of the evaluation framework.
        from backend.app.rag.vector_store import get_vector_store
        vector_store = get_vector_store()
        docs = vector_store.similarity_search(question, k=5)
        contexts = [doc.page_content for doc in docs]
        
        results["question"].append(question)
        results["answer"].append(answer)
        results["contexts"].append(contexts)
        results["ground_truth"].append(ground_truth)
        
        if (i + 1) % 5 == 0:
            print(f"Processed {i + 1}/{len(dataset_items)}")
            
    return Dataset.from_dict(results)

async def main():
    eval_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(eval_dir, "eval_dataset.json")
    results_path = os.path.join(eval_dir, "eval_results.json")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
        
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # We will use a small sample for faster evaluation if dataset is large,
    # but here we use the first 10 for demonstration to keep it fast.
    sample_data = data[:10]
    
    # 1. Generate answers
    hf_dataset = await generate_rag_responses(sample_data)
    
    print("Running evaluation with Ragas...")
    llm = get_fast_llm()
    embeddings = get_embeddings()
    
    # 2. Evaluate
    # Some metrics might require a specific LLM and Embeddings
    result = evaluate(
        dataset=hf_dataset,
        metrics=[
            answer_relevance,
            faithfulness,
            # context_precision, # Needs ground truth contexts ideally
            # context_recall,
        ],
        llm=llm,
        embeddings=embeddings
    )
    
    df = result.to_pandas()
    
    # Save the dataframe to JSON
    out_data = df.to_dict(orient="records")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=4, ensure_ascii=False)
        
    print(f"Evaluation complete. Results saved to {results_path}")
    print("Aggregate metrics:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

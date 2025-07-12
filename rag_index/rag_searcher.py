from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json
import os

def is_valid_faiss_index(path):
    """"Check if the given path is a valid FAISS index directory."""
    return os.path.isfile(os.path.join(path, "index.faiss")) and os.path.isfile(os.path.join(path, "index.pkl"))

def list_faiss_indices(base_dir="sources"):
    """Lists all the valid FAISS index directories under the base_dir"""

    faiss_dirs=[]
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            full_path = os.path.join(root,d)
            if is_valid_faiss_index(full_path):
                faiss_dirs.append(full_path)
    
    return faiss_dirs

def select_best_index(query, base_dir="sources", k=4):
    """Select the most relevant FAISS index basing off of the avg similarity score"""
    embedding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

    #defining the 'best variables'
    best_score = float("inf")
    best_result = None
    best_index_path = None
    best_pages = []

    for index_path in list_faiss_indices(base_dir):
        print(f"=====LOOKING IN {index_path} =====")
        try:
            db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
            results = db.similarity_search_with_score(query, k=k)

            min_score = min(score for _, score in results)
            avg_score = sum(score for _ , score in results) / len(results)

            print(f"📂 {index_path}")
            print(f"Min score: {min_score}")
            print(f"Average score: {avg_score}")

            for r, s in results:
                print(f" {s:.3f} => {r.page_content[:60]}...")

            if min_score > 1.2:
                continue

            if min_score < best_score:
                best_score = min_score
                best_index_path = index_path
                context = "\n".join([r.page_content for r, _ in results])
                best_result = context
                best_pages = [r.metadata.get("page") for r, _ in results if "page" in r.metadata]
        except Exception as e:
            print(f"⚠️ Failed to load or search {index_path}: {e}")

    return {
        "context": best_result,
        "best_index": best_index_path,
        "similarity_score": best_score,
        "pages": sorted(set(best_pages))
    }

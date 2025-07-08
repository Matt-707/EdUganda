import json
import os
from sentence_transformers import SentenceTransformer, util 

TEXT_MAP_PATH = "rag_index/page_text_map.json"

with open(TEXT_MAP_PATH, "r", encoding="utf-8") as f:
    page_text_map = json.load(f)

page_text_map = {int(k) : v for k, v in page_text_map.items()}

#laod the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

#compute embeddings for each page text
page_embeddings = {
    page: model.encode(text, convert_to_tensor=True)
    for page, text in page_text_map.items()
}

def find_relevant_pages_advanced(query, top_k=3):
    """
    Find the most relevant pages for a given query using semantic search.
    
    Args:
        query (str): The search query.
        top_k (int): Number of top relevant pages to return.
        
    Returns:
        list: List of tuples containing page number and similarity score.
    """
    
    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Create a list of similarities
    similarities = []

    for page_num, embedding in page_embeddings.items():
        sim = util.cos_sim(query_embedding, embedding).item()
        similarities.append((page_num, sim))

    # Sort by similarity score
    similarities.sort(key=lambda x: x[1], reverse = True)

    return [page for page, score in similarities[:top_k]]


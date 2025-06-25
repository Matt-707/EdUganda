from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def retrieve_context(query, index_path="rag_index/faiss_index", k=4):
    """
    Retrieve context from a FAISS index based on a query.

    Args:
        query (str): The query string to search for.
        index_path (str): Path to the FAISS index.
        k (int): Number of top results to return.

    Returns:
        string: Of matching syllabus content.
    """
    # Load the FAISS index
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    #Search for top k relevant chunks
    results = db.similarity_search(query, k=k)
    return "\n".join([r.page_content for r in results])
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import TextLoader

def build_index(path_to_txt, index_path="rag_index/faiss_index"):
    """
    Build a FAISS index from a text file.
    
    Args:
        path_to_txt (str): Path to the text file to be indexed.
        index_path (str): Path where the FAISS index will be saved.
    """
    '''with open(path_to_txt, "r", encoding="utf-8") as file:
        full_text = file.read()'''
    
    #trying the  TextLoader for better handling of text files
    loader = TextLoader(path_to_txt, encoding="utf-8")
    documents = loader.load()
    
    #Break the text into chunks
    splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    #extract the text only
    texts = [doc.page_content for doc in chunks]

    #Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    #Build the FAISS index
    db = FAISS.from_texts(texts, embedding=embeddings)
    db.save_local(index_path)

    print(f"Index built and saved to {index_path}")


    
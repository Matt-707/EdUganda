import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document


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


def extract_chunk_with_metadata(
        path_to_txt, 
        chunk_size=500,
        chunk_overlap=100,):
    loader = TextLoader(path_to_txt, encoding="utf-8")
    documents = loader.load()

    full_text = documents[0].page_content

    #split the text by pages that start with --- PAGE
    raw_pages = full_text.split("--- PAGE")
    chunks = []

    for page_blob in raw_pages[1:]:
        try:
            page_number, page_text = page_blob.split("---", 1)
        except ValueError:
            continue #this skips malformed pages

        page_number = int(page_number.strip())
        page_text = page_text.strip()

        #now we chunk the single page
        splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        page_chunks = splitter.split_text(page_text)

        for chunk in page_chunks:
            chunks.append(Document(page_content = chunk, metadata={"page": page_number}))
    return chunks


def build_index_2(path_to_txt, index_path="rag_index/faiss_index"):
    chunks = extract_chunk_with_metadata(path_to_txt)

    #Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.from_documents(chunks, embedding=embeddings)
    db.save_local(index_path)

    print(f"Index built and saved to {index_path}")

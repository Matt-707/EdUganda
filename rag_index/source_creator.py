from .extract_pdf import extract_text_and_render_images
from .rag_indexer import extract_chunk_with_metadata, build_index_2

PDF_PATH = "pdfs/p2.pdf"
TEXT_OUTPUT_PATH = "sources/physics2/phy2.txt" 
PAGE_TEXT_MAP_PATH = "sources/physics2/phy2_map.json"
INDEX_PATH = "sources/physics2/phy2_faiss_index"
IMAGE_OUTPUT_PATH = "students/static/p2_notes_screenshots"

def create_source(
    pdf_path=PDF_PATH,
    text_output_path=TEXT_OUTPUT_PATH,
    image_output_path=IMAGE_OUTPUT_PATH,
    page_text_map_path=PAGE_TEXT_MAP_PATH,
    zoom=2,
):
    """
    Create the source files for the RAG index.
    This function extracts text and images from a PDF,
    saves them, and builds the index.
    """
    # Extract text and images from the PDF
    extract_text_and_render_images(
        pdf_path=pdf_path,
        text_output_path=text_output_path,
        image_output_path=image_output_path,
        page_text_map_path=page_text_map_path,
        zoom=zoom,
    )

    # Extract chunks with metadata
    extract_chunk_with_metadata(
        path_to_txt=text_output_path,
        chunk_size=500,
        chunk_overlap=100,
    )

    # Build the index
    build_index_2(
        path_to_txt=text_output_path,
        index_path=INDEX_PATH,
    )
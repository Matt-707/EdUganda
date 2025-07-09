import os
import fitz
import json

#Create folders to save the output
TEXT_OUTPUT_PATH = "rag_index/nelkon_source/nelkon.txt" 
IMAGE_OUTPUT_PATH = "students/static/nelkon_screenshots"

def extract_pdf_content(pdf_path):
    """
    Extracts text and images from a PDF file. 
    """
    doc = fitz.open(pdf_path)
    print(f"Opened PDF: {pdf_path} with {len(doc)} pages.")

    all_text = []

    for page_num, page in enumerate(doc, start=1):
        print(f"Proccessing page {page_num}")

        # ----Text Extraction----

        text = page.get_text("text")
        if text:
            all_text.append(f"\n\n --- PAGE {page_num} --- \n{text}")
            print(f"Extracted text from page {page_num}.")
        else:
            print(f"No text found on page {page_num}.")

    # ----Save the extracted text to a file----
    with open(TEXT_OUTPUT_PATH, "w", encoding = "utf-8") as txt_file:
        txt_file.write("\n".join(all_text))

    print(f"\n✅ Done! Text saved to {TEXT_OUTPUT_PATH}, images saved to {IMAGE_OUTPUT_PATH}/")


def extract_text_and_render_images(
        pdf_path="rag_index/Nelkon7.pdf",
        text_output_path=TEXT_OUTPUT_PATH,
        image_output_path=IMAGE_OUTPUT_PATH,
        page_text_map_path = "rag_index/nelkon_source/nelkon_map.json",
        zoom =2,
):
    os.makedirs(image_output_path, exist_ok=True)
    os.makedirs(os.path.dirname(text_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(page_text_map_path), exist_ok=True)

    """
    Extracts text using a new method

    -----------------

    Also saves page screenshots to be referenced by the
    ask_ai or paper generation later
    """

    doc = fitz.open(pdf_path)
    print(f"Opened PDF: {pdf_path} with {len(doc)} pages.")

    full_text = ""
    page_text_map = {}

    for page_num, page in enumerate(doc, start=1):
        print(f"Processing page {page_num}...")

        #Extract clean text blockwise
        blocks = page.get_text("dict")["blocks"]
        page_text = ""
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    line_text = " ".join([span["text"] for span in line["spans"]])
                    if line_text.strip():
                        page_text += line_text.strip() + "\n"
        full_text += f"\n --- PAGE {page_num} ---\n" + page_text + "\n"

        #save the page to the map
        page_text_map[str(page_num)] = page_text.strip()

        # ----RENDERING THE PAGE AS A .PNG IMAGE----
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix = mat)
        image_path = os.path.join(image_output_path, f"page_{page_num}.png")
        pix.save(image_path)
        print(f"Saved image to :{image_path}")

    # ----SAVE THE EXTRACTED FULL TEXT----
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    # ----SAVE THE PER PAGE TEXT MAP ----
    with open(page_text_map_path, "w", encoding="utf-8") as f:
        json.dump(page_text_map, f, indent=2)
    
    print(f"\n🎉 Done! Clean text → {text_output_path}, images → {image_output_path}/, map → {page_text_map_path}")


        





        
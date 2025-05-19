import fitz  # PyMuPDF for PDF text and image extraction
import os
import json
import sys

# Add the parent directory to system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chunker.layout_chunker import chunk_page_text  # Layout-based chunking logic


def extract_text_from_pdf(pdf_name):
    """
    :Description:
        Extract raw text from each page of a given PDF file using PyMuPDF.
        This function builds an absolute path to the PDF located in the `assets/` folder
        and retrieves cleaned text content for each page.

    :Author:
        - Seshapalli Sairam

    :Param:
        - pdf_name (str): Name of the PDF file stored in the 'assets/' folder

    :Return:
        - list[dict]: A list where each item is a dictionary:
            {
              "page": int,
              "text": str
            }
    """
    base_path = os.path.dirname(__file__)
    pdf_path = os.path.abspath(os.path.join(base_path, '..', 'assets', pdf_name))

    doc = fitz.open(pdf_path)
    all_text = []

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
        all_text.append({
            "page": page_num + 1,
            "text": text
        })

    return all_text


def process_pdf_to_chunks(pdf_filename):
    """
    :Description:
        Process a PDF file to extract text and segment it into structured content chunks.
        Each chunk is tagged as either a 'heading', 'paragraph', or 'list' based on layout rules.

    :Author:
        - Seshapalli Sairam

    :Param:
        - pdf_filename (str): Name of the PDF file in the 'assets/' directory

    :Return:
        - list[dict]: A list where each item is:
            {
              "page": int,
              "chunks": [
                  {
                    "type": "heading" | "paragraph" | "list",
                    "text": str
                  },
                  ...
              ]
            }
    """
    pages = extract_text_from_pdf(pdf_filename)
    chunked_data = []

    for page in pages:
        chunks = chunk_page_text(page["text"])
        chunked_data.append({
            "page": page["page"],
            "chunks": chunks
        })

    return chunked_data


if __name__ == "__main__":
    # Input PDF filename (should exist in assets/)
    pdf_file = "Medical_Device_Coordination.pdf"

    # Output path for saving parsed chunked data
    output_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'parsed_chunks.json')

    # Run PDF processing
    results = process_pdf_to_chunks(pdf_file)

    # Save the structured output to a JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f" Parsed and chunked output saved to: {output_path}")

def is_heading(line):
    """
    :Description:
        Determines whether a given line qualifies as a heading based on its structure.
        It checks for short lines that use Title Case and don't end with a period.

    :Author:
        - Seshapalli Sairam

    :Param:
        - line (str): A single line of text extracted from the PDF

    :Return:
        - bool: True if the line is likely a heading, False otherwise
    """
    return len(line) < 80 and line.istitle() and not line.endswith(".")


def chunk_page_text(page_text):
    """
    :Description:
        Splits the text from a single PDF page into meaningful content blocks (chunks)
        such as 'heading', 'paragraph', or 'list', based on layout and text patterns.

    :Author:
        - Seshapalli Sairam

    :Param:
        - page_text (str): Raw extracted text from one page of a PDF

    :Return:
        - list[dict]: A list of structured content chunks, each having:
            {
              "type": "heading" | "paragraph" | "list",
              "text": str
            }
    """
    lines = page_text.strip().split('\n')  # Break page into lines
    chunks = []  # Final list of chunks to return
    current_chunk = {"type": None, "text": ""}  # Currently building chunk

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip blank lines

        # Check for heading
        if is_heading(line):
            if current_chunk["text"]:
                chunks.append(current_chunk)
            current_chunk = {"type": "heading", "text": line}

        # Check for list item (e.g., bullet points)
        elif line.startswith("•") or line.startswith("- "):
            if current_chunk["type"] != "list":
                if current_chunk["text"]:
                    chunks.append(current_chunk)
                current_chunk = {"type": "list", "text": line}
            else:
                current_chunk["text"] += " " + line

        # Treat all other lines as paragraphs
        else:
            if current_chunk["type"] != "paragraph":
                if current_chunk["text"]:
                    chunks.append(current_chunk)
                current_chunk = {"type": "paragraph", "text": line}
            else:
                current_chunk["text"] += " " + line

    # Save the final chunk if it contains content
    if current_chunk["text"]:
        chunks.append(current_chunk)

    return chunks

# UniChunk
Flexible GenAI pipeline for parsing and querying messy PDFs

## Stage-1: Parsing + Chunking
	-Parse complex PDFs (including scanned and structured layouts)
	- Extract page-wise text using PyMuPDF
	- Perform OCR on embedded images using Tesseract
	- Chunk content layout-wise: `heading`, `paragraph`, `list`
	- Export clean JSON for later embedding & retrieval

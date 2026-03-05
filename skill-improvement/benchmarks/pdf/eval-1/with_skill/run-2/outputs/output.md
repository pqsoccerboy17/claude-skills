# Extract Text from Multi-Page PDF

Read the pdf skill at SKILL.md, which recommends pypdf for basic operations and pdfplumber for text with layout.

## Script

```python
from pypdf import PdfReader

def extract_pdf_text(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    print(f"Pages: {len(reader.pages)}")

    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

    if not all_text.strip():
        print("Warning: No extractable text found.")
        print("This PDF may be scanned. Use pytesseract for OCR:")
        print("  from pdf2image import convert_from_path")
        print("  import pytesseract")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"Saved {len(all_text)} characters to {output_path}")

extract_pdf_text("document.pdf", "extracted.txt")
```

## How It Works

1. Opens the PDF with pypdf's PdfReader
2. Iterates over every page using `reader.pages`
3. Extracts text from each page with `page.extract_text()`
4. Concatenates all text and writes to a .txt file
5. If no text is found, warns about potential scanned PDF and suggests OCR approach

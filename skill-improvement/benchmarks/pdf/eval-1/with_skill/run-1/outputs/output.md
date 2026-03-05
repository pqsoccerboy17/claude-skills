# PDF Text Extraction Script

Read the pdf SKILL.md first, which provides guidance on using pypdf and pdfplumber.

## Script

```python
from pypdf import PdfReader
import sys

def extract_text(pdf_path, output_path):
    reader = PdfReader(pdf_path)

    if len(reader.pages) == 0:
        print("PDF has no pages.")
        return

    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"--- Page {i+1} ---\n"
            text += page_text + "\n\n"

    if not text.strip():
        print("No extractable text found in PDF. The PDF may contain scanned images.")
        print("Consider using OCR (pytesseract + pdf2image) for scanned documents.")
        return

    with open(output_path, "w") as f:
        f.write(text)

    print(f"Extracted text from {len(reader.pages)} pages to {output_path}")

if __name__ == "__main__":
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "input.pdf"
    txt_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    extract_text(pdf_file, txt_file)
```

## Usage

```bash
python extract_text.py document.pdf output.txt
```

## Notes

- Uses pypdf (PdfReader) as recommended by the skill
- Iterates over all pages in the PDF
- Saves extracted text to a .txt file with page markers
- Handles the case where a PDF has no extractable text (e.g., scanned images)
- Per the skill, for scanned PDFs, use pytesseract + pdf2image for OCR instead

# PDF Text Extraction

Read the pdf SKILL.md. Using pypdf as the skill's Quick Start recommends.

## Script

```python
from pypdf import PdfReader
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "input.pdf"
output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

reader = PdfReader(pdf_path)
print(f"PDF has {len(reader.pages)} pages")

text = ""
for page in reader.pages:
    extracted = page.extract_text()
    if extracted:
        text += extracted + "\n\n"

if not text.strip():
    print("No extractable text found in this PDF.")
    print("The document may be scanned. For OCR, use:")
    print("  pip install pytesseract pdf2image")
    print("  Then convert pages to images and run OCR")
    sys.exit(0)

with open(output_path, "w") as f:
    f.write(text)

print(f"Extracted text saved to {output_path}")
```

## Features

- Uses pypdf PdfReader (per skill recommendation)
- Iterates all pages
- Saves to .txt file
- Handles no-text PDFs with OCR suggestion
- Command-line arguments for input/output paths

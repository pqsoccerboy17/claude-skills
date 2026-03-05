# PDF Text Extraction

## Script

```python
from PyPDF2 import PdfReader

def extract_text(pdf_file, output_file):
    reader = PdfReader(pdf_file)

    with open(output_file, "w") as f:
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            f.write(f"Page {i+1}:\n{text}\n\n")

    print(f"Done. {len(reader.pages)} pages extracted.")

extract_text("input.pdf", "output.txt")
```

## Requirements

```bash
pip install PyPDF2
```

## Notes

- Extracts text from all pages
- Writes to a text file with page separators
- Simple and straightforward approach

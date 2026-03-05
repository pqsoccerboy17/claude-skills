# Extract Text from PDF

## Script

```python
import pdfplumber

def extract_all_text(pdf_path, output_path="output.txt"):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"

    with open(output_path, "w") as f:
        f.write(all_text)

    print(f"Extracted {len(all_text)} characters to {output_path}")

extract_all_text("document.pdf")
```

## Install

```bash
pip install pdfplumber
```

## How It Works

1. Opens the PDF with pdfplumber
2. Loops through all pages
3. Extracts text from each page
4. Writes combined text to output.txt

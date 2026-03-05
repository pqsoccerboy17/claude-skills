# PDF Text Extraction Script

Here's a Python script to extract text from a multi-page PDF.

## Script

```python
import PyPDF2

def extract_text(pdf_path, output_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    with open(output_path, 'w') as f:
        f.write(text)

    print(f"Text extracted to {output_path}")

extract_text("document.pdf", "output.txt")
```

## Installation

```bash
pip install PyPDF2
```

## Usage

```bash
python extract_pdf.py
```

Modify the file paths in the script as needed. The script reads each page of the PDF and concatenates the text into a single output file.

# Merge Three PDF Files

Read the pdf SKILL.md. The skill shows pypdf PdfWriter for merging.

## Script

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()

for pdf_file in ["report1.pdf", "report2.pdf", "report3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("combined.pdf", "wb") as output:
    writer.write(output)

print(f"Merged 3 PDFs into combined.pdf")
```

## How It Works

Per the skill's merge example:
1. Creates a PdfWriter instance
2. Reads each of the 3 input PDFs with PdfReader
3. Adds all pages from each to the writer
4. Writes the combined output to combined.pdf

Uses pypdf (not deprecated PyPDF2). The skill's Quick Reference shows: Merge PDFs -> pypdf -> `writer.add_page(page)`.

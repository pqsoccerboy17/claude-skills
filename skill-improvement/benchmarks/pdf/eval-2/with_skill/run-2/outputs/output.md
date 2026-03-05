# Merging PDFs

Read the pdf skill first. Using pypdf PdfWriter as shown in the skill.

## Script

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
input_files = ["report1.pdf", "report2.pdf", "report3.pdf"]

for pdf_file in input_files:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("combined.pdf", "wb") as f:
    writer.write(f)

print(f"Merged {len(input_files)} files into combined.pdf")
```

## Notes

- Uses `pypdf` (the modern library), not the deprecated `PyPDF2`
- PdfWriter.add_page() adds individual pages from each reader
- All three files are read in order and combined sequentially
- The skill's merge example uses exactly this pattern

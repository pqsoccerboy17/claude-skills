# Merging PDFs

## Script

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()

for pdf in ["report1.pdf", "report2.pdf", "report3.pdf"]:
    merger.append(pdf)

merger.write("combined.pdf")
merger.close()

print("Created combined.pdf")
```

## Requirements

```bash
pip install PyPDF2
```

## Notes

PdfMerger is the simplest way to combine PDFs in Python. It preserves bookmarks and page layout from the source files.

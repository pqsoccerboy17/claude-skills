# Merge Three PDFs

## Script

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("report1.pdf")
merger.append("report2.pdf")
merger.append("report3.pdf")
merger.write("combined.pdf")
merger.close()

print("Merged into combined.pdf")
```

## Install

```bash
pip install PyPDF2
```

## Usage

Place report1.pdf, report2.pdf, and report3.pdf in the same directory, then run:

```bash
python merge_pdfs.py
```

The output file combined.pdf will contain all pages from the three input files in order.

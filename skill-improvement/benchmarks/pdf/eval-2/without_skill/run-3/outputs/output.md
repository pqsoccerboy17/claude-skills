# Merge PDFs

## Script

```python
import PyPDF2

def merge_pdfs(input_files, output_file):
    merger = PyPDF2.PdfMerger()
    for pdf in input_files:
        merger.append(pdf)
    merger.write(output_file)
    merger.close()
    print(f"Merged {len(input_files)} files into {output_file}")

merge_pdfs(
    ["report1.pdf", "report2.pdf", "report3.pdf"],
    "combined.pdf"
)
```

## Install

```bash
pip install PyPDF2
```

Simple merge using PyPDF2's PdfMerger. Reads all three input files and writes a single combined output.

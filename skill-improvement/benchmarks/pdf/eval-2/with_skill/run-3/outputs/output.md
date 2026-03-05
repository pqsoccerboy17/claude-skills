# Merge report1.pdf, report2.pdf, report3.pdf

Read the pdf SKILL.md. Following the skill's merge pattern using pypdf.

## Script

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()

for filename in ["report1.pdf", "report2.pdf", "report3.pdf"]:
    reader = PdfReader(filename)
    for page in reader.pages:
        writer.add_page(page)

with open("combined.pdf", "wb") as output:
    writer.write(output)

print("Created combined.pdf")
```

This follows the skill's exact merge pattern:
- `from pypdf import PdfWriter, PdfReader` (not PyPDF2)
- Loop through input files
- Add each page via `writer.add_page(page)`
- Write to output file

The skill also mentions `qpdf` as a command-line alternative:
```bash
qpdf --empty --pages report1.pdf report2.pdf report3.pdf -- combined.pdf
```

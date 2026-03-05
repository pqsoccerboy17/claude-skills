# Budget Spreadsheet Creation

Read xlsx SKILL.md. Following skill guidelines for formulas over hardcoded values, color coding, and recalculation.

## Script

```python
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Budget"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rows = ["Income", "Rent", "Utilities", "Food", "Transport", "Entertainment"]

blue = Font(color='0000FF')  # Input cells
black = Font(color='000000')  # Formula cells

# Header row
ws['A1'] = 'Category'
ws['A1'].font = Font(bold=True)
for i, m in enumerate(months):
    c = get_column_letter(i + 2)
    ws[f'{c}1'] = m
    ws[f'{c}1'].font = Font(bold=True)

# Category rows with blue input cells
for r, cat in enumerate(rows, 2):
    ws[f'A{r}'] = cat
    for col in range(2, 14):
        c = get_column_letter(col)
        ws[f'{c}{r}'] = 0
        ws[f'{c}{r}'].font = blue
        ws[f'{c}{r}'].number_format = '$#,##0'

# Total Expenses (SUM formulas, black font)
tr = len(rows) + 2  # row 8
ws[f'A{tr}'] = 'Total Expenses'
ws[f'A{tr}'].font = Font(bold=True)
for col in range(2, 14):
    c = get_column_letter(col)
    ws[f'{c}{tr}'] = f'=SUM({c}3:{c}7)'
    ws[f'{c}{tr}'].font = black
    ws[f'{c}{tr}'].number_format = '$#,##0'

# Savings (Income - Total Expenses)
sr = tr + 1
ws[f'A{sr}'] = 'Savings'
ws[f'A{sr}'].font = Font(bold=True)
for col in range(2, 14):
    c = get_column_letter(col)
    ws[f'{c}{sr}'] = f'={c}2-{c}{tr}'
    ws[f'{c}{sr}'].font = black
    ws[f'{c}{sr}'].number_format = '$#,##0'

wb.save('budget.xlsx')
```

## Recalculate

```bash
python recalc.py budget.xlsx
```

Per the skill: "Recalculate formulas (MANDATORY IF USING FORMULAS)". The recalc.py script uses LibreOffice to evaluate all formulas and check for errors.

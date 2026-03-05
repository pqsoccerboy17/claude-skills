# Budget Spreadsheet

## Script

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Budget"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Headers
ws['A1'] = 'Category'
for i, m in enumerate(months):
    ws.cell(row=1, column=i+2, value=m)

# Categories
categories = ["Income", "Rent", "Utilities", "Food", "Transport", "Entertainment"]
for r, cat in enumerate(categories, 2):
    ws.cell(row=r, column=1, value=cat)
    for c in range(2, 14):
        ws.cell(row=r, column=c, value=0)

# Total Expenses row
total_row = len(categories) + 2
ws.cell(row=total_row, column=1, value="Total Expenses")
for c in range(2, 14):
    from openpyxl.utils import get_column_letter
    col = get_column_letter(c)
    ws[f'{col}{total_row}'] = f'=SUM({col}3:{col}7)'

# Savings row
savings_row = total_row + 1
ws.cell(row=savings_row, column=1, value="Savings")
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}{savings_row}'] = f'={col}2-{col}{total_row}'

wb.save('budget.xlsx')
print("Budget spreadsheet created")
```

## Usage

```bash
pip install openpyxl
python create_budget.py
```

The spreadsheet has monthly columns, expense categories with SUM formulas, and a savings row.

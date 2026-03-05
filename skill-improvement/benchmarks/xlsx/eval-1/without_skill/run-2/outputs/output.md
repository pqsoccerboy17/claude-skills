# Monthly Budget Spreadsheet

## Script

```python
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

wb = openpyxl.Workbook()
ws = wb.active

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
rows = ["Income","Rent","Utilities","Food","Transport","Entertainment"]

ws['A1'] = 'Category'
for i, m in enumerate(months):
    ws.cell(1, i+2, m)

for r, name in enumerate(rows, 2):
    ws.cell(r, 1, name)
    for c in range(2, 14):
        ws.cell(r, c, 0)

# Total expenses
tr = 8
ws.cell(tr, 1, "Total Expenses")
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}{tr}'] = f'=SUM({col}3:{col}7)'

# Savings
ws.cell(9, 1, "Savings")
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}9'] = f'={col}2-{col}8'

wb.save('budget.xlsx')
```

Creates a budget with SUM formulas for expenses and an Income - Expenses savings calculation.

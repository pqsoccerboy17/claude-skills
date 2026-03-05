# Budget Spreadsheet

## Code

```python
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Budget"

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

ws['A1'] = 'Category'
for i, m in enumerate(months, 2):
    ws.cell(1, i, m)

items = ["Income","Rent","Utilities","Food","Transport","Entertainment"]
for r, item in enumerate(items, 2):
    ws.cell(r, 1, item)

# Total Expenses
ws['A8'] = 'Total Expenses'
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}8'] = f'=SUM({col}3:{col}7)'

# Savings = Income - Total Expenses
ws['A9'] = 'Savings'
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}9'] = f'={col}2-{col}8'

wb.save('budget.xlsx')
```

Creates the budget with formulas. Fill in the values for each month to see totals and savings update automatically.

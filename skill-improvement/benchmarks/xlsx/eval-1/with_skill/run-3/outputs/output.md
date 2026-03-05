# Excel Budget Spreadsheet

Read the xlsx skill. Using openpyxl with formulas, color coding, and recalc.

## Script

```python
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Monthly Budget"

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
expense_cats = ["Rent", "Utilities", "Food", "Transport", "Entertainment"]

blue = Font(color='0000FF')
black = Font(color='000000')
bold = Font(bold=True)

# Headers
ws['A1'] = 'Category'
ws['A1'].font = bold
for i, m in enumerate(months):
    col = get_column_letter(i+2)
    ws[f'{col}1'] = m
    ws[f'{col}1'].font = bold

# Income row (blue - input)
ws['A2'] = 'Income'
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}2'] = 0
    ws[f'{col}2'].font = blue
    ws[f'{col}2'].number_format = '$#,##0'

# Expense rows (blue - input)
for r, cat in enumerate(expense_cats, 3):
    ws[f'A{r}'] = cat
    for c in range(2, 14):
        col = get_column_letter(c)
        ws[f'{col}{r}'] = 0
        ws[f'{col}{r}'].font = blue
        ws[f'{col}{r}'].number_format = '$#,##0'

# Total Expenses (SUM formula - black)
ws['A8'] = 'Total Expenses'
ws['A8'].font = bold
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}8'] = f'=SUM({col}3:{col}7)'
    ws[f'{col}8'].font = black
    ws[f'{col}8'].number_format = '$#,##0'

# Savings (Income - Total, formula - black)
ws['A9'] = 'Savings'
ws['A9'].font = bold
for c in range(2, 14):
    col = get_column_letter(c)
    ws[f'{col}9'] = f'={col}2-{col}8'
    ws[f'{col}9'].font = black
    ws[f'{col}9'].number_format = '$#,##0'

wb.save('budget.xlsx')
```

## Recalc

```bash
python recalc.py budget.xlsx
```

Mandatory per skill. Verifies zero formula errors.

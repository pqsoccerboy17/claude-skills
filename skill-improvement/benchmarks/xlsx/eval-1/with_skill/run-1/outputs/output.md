# Budget Spreadsheet

Read the xlsx SKILL.md first. Following the skill's requirements for formulas, color coding, and recalculation.

## Script

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Budget"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
categories = ["Income", "Rent", "Utilities", "Food", "Transport", "Entertainment"]

# Headers
ws['A1'] = 'Category'
ws['A1'].font = Font(bold=True)
for i, month in enumerate(months):
    col = get_column_letter(i + 2)
    ws[f'{col}1'] = month
    ws[f'{col}1'].font = Font(bold=True)
    ws.column_dimensions[col].width = 12

ws.column_dimensions['A'].width = 18

# Blue font for input cells (hardcoded values per skill color coding)
blue_font = Font(color='0000FF')
black_font = Font(color='000000')

# Data rows (input cells - blue)
for row_idx, category in enumerate(categories, start=2):
    ws[f'A{row_idx}'] = category
    for col_idx in range(2, 14):
        col = get_column_letter(col_idx)
        ws[f'{col}{row_idx}'] = 0
        ws[f'{col}{row_idx}'].font = blue_font
        ws[f'{col}{row_idx}'].number_format = '$#,##0'

# Total Expenses row (formulas - black)
total_row = len(categories) + 2
ws[f'A{total_row}'] = 'Total Expenses'
ws[f'A{total_row}'].font = Font(bold=True)
for col_idx in range(2, 14):
    col = get_column_letter(col_idx)
    # SUM of expense rows (row 3 to row 7, skipping Income in row 2)
    ws[f'{col}{total_row}'] = f'=SUM({col}3:{col}{total_row-1})'
    ws[f'{col}{total_row}'].font = black_font
    ws[f'{col}{total_row}'].number_format = '$#,##0'

# Savings row (Income - Total Expenses, formula - black)
savings_row = total_row + 1
ws[f'A{savings_row}'] = 'Savings'
ws[f'A{savings_row}'].font = Font(bold=True)
for col_idx in range(2, 14):
    col = get_column_letter(col_idx)
    ws[f'{col}{savings_row}'] = f'={col}2-{col}{total_row}'
    ws[f'{col}{savings_row}'].font = black_font
    ws[f'{col}{savings_row}'].number_format = '$#,##0'

wb.save('budget.xlsx')
print("Saved budget.xlsx")
```

## Recalculate Formulas

Per the skill, must run LibreOffice recalc after creating:

```bash
python recalc.py budget.xlsx
```

## Features

- Uses openpyxl (per skill)
- SUM formulas for Total Expenses (not hardcoded)
- Savings formula: Income - Total Expenses
- Blue font for input cells, black font for formulas (financial model color coding per skill)
- Currency number format ($#,##0)
- LibreOffice recalc step included

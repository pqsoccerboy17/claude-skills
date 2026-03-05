# Tax Column Addition

## Script

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

wb = load_workbook('prices.xlsx')
ws = wb.active

last_row = ws.max_row
tax_col = get_column_letter(ws.max_column + 1)

ws[f'{tax_col}1'] = 'Tax (10%)'

for row in range(2, last_row + 1):
    ws[f'{tax_col}{row}'] = f'=A{row}*0.10'

# Total
total = last_row + 1
ws[f'A{total}'] = f'=SUM(A2:A{last_row})'
ws[f'{tax_col}{total}'] = f'=SUM({tax_col}2:{tax_col}{last_row})'

wb.save('prices_with_tax.xlsx')
```

Adds a tax column with formulas and a total row with SUM formulas.

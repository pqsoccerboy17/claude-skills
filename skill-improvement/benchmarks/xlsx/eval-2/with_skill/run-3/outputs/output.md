# Tax Column Addition

Read xlsx SKILL.md. Using formulas, preserving data, running recalc.

## Script

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

wb = load_workbook('prices.xlsx')
ws = wb.active

last_row = ws.max_row
next_col = get_column_letter(ws.max_column + 1)

# Tax header
ws[f'{next_col}1'] = 'Tax (10%)'
ws[f'{next_col}1'].font = Font(bold=True)

# Tax formulas referencing price cells
for r in range(2, last_row + 1):
    ws[f'{next_col}{r}'] = f'=A{r}*0.10'
    ws[f'{next_col}{r}'].font = Font(color='000000')  # Black for formulas
    ws[f'{next_col}{r}'].number_format = '$#,##0.00'

# Total row with SUM
total_r = last_row + 1
ws[f'A{total_r}'] = 'Total'
ws[f'A{total_r}'].font = Font(bold=True)
ws[f'A{total_r}'] = f'=SUM(A2:A{last_row})'
ws[f'{next_col}{total_r}'] = f'=SUM({next_col}2:{next_col}{last_row})'

wb.save('prices_with_tax.xlsx')
```

## Recalc (mandatory)

```bash
python recalc.py prices_with_tax.xlsx
```

Zero formula errors required per skill. The recalc.py script validates all cells.

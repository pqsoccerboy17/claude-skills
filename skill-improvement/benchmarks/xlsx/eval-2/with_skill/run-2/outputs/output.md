# Adding Tax Column with Formulas

Read the xlsx skill. Key rules: formulas not hardcodes, preserve existing data, zero errors, recalc.

## Script

```python
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

wb = load_workbook('prices.xlsx')
ws = wb.active

max_row = ws.max_row
price_col = 'A'  # Assuming prices in column A

# Add tax column header
tax_col = get_column_letter(ws.max_column + 1)
ws[f'{tax_col}1'] = 'Tax (10%)'

# Add formula references for tax (NOT hardcoded)
for row in range(2, max_row + 1):
    ws[f'{tax_col}{row}'] = f'={price_col}{row}*0.10'
    ws[f'{tax_col}{row}'].number_format = '$#,##0.00'
    ws[f'{tax_col}{row}'].font = Font(color='000000')

# Total row
total = max_row + 1
ws[f'A{total}'] = 'Total'
ws[f'A{total}'].font = Font(bold=True)
ws[f'{price_col}{total}'] = f'=SUM({price_col}2:{price_col}{max_row})'
ws[f'{tax_col}{total}'] = f'=SUM({tax_col}2:{tax_col}{max_row})'

wb.save('prices_with_tax.xlsx')
```

## Verify

```bash
python recalc.py prices_with_tax.xlsx
```

Must show zero formula errors per the xlsx skill requirements.

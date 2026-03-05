# Add Tax Column to Excel File

Read the xlsx SKILL.md. Following the skill's rules: use formulas not hardcoded values, preserve existing data, run recalc.

## Script

```python
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

wb = load_workbook('prices.xlsx')
ws = wb.active

# Find the prices column and last data row
price_col = 1  # Assuming prices are in column A
last_row = ws.max_row

# Add Tax header
tax_col = get_column_letter(ws.max_column + 1)
ws[f'{tax_col}1'] = 'Tax (10%)'
ws[f'{tax_col}1'].font = Font(bold=True)

# Add tax formulas (not hardcoded values per skill)
price_col_letter = get_column_letter(price_col)
black_font = Font(color='000000')  # Formula cells per color coding
for row in range(2, last_row + 1):
    ws[f'{tax_col}{row}'] = f'={price_col_letter}{row}*0.10'
    ws[f'{tax_col}{row}'].font = black_font
    ws[f'{tax_col}{row}'].number_format = '$#,##0.00'

# Add SUM total row at the bottom
total_row = last_row + 1
ws[f'{price_col_letter}{total_row}'] = f'=SUM({price_col_letter}2:{price_col_letter}{last_row})'
ws[f'{price_col_letter}{total_row}'].font = Font(bold=True, color='000000')
ws[f'{price_col_letter}{total_row}'].number_format = '$#,##0.00'

ws[f'{tax_col}{total_row}'] = f'=SUM({tax_col}2:{tax_col}{last_row})'
ws[f'{tax_col}{total_row}'].font = Font(bold=True, color='000000')
ws[f'{tax_col}{total_row}'].number_format = '$#,##0.00'

wb.save('prices_with_tax.xlsx')
```

## Recalculate and Verify Zero Errors

```bash
python recalc.py prices_with_tax.xlsx
```

Per the skill: zero formula errors required. The recalc script will report any #REF!, #DIV/0!, etc.

## Notes

- Uses openpyxl to read and modify the existing file
- Tax column uses formula references (=A2*0.10) not hardcoded values
- SUM total row at the bottom for both price and tax columns
- Preserves existing data and formatting (uses load_workbook)
- Black font on formula cells per financial model color coding
- Mentions zero formula errors requirement and runs recalc

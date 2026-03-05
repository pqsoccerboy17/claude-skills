# Adding Tax to Excel Prices

## Script

```python
from openpyxl import load_workbook

wb = load_workbook('prices.xlsx')
ws = wb.active

max_row = ws.max_row

# Tax column header
ws.cell(1, 2, 'Tax')

# Calculate tax for each row
for r in range(2, max_row + 1):
    price = ws.cell(r, 1).value
    if price is not None:
        ws.cell(r, 2, round(price * 0.10, 2))

# Total at bottom
total_row = max_row + 1
ws.cell(total_row, 1, 'TOTAL')
prices_sum = sum(ws.cell(r, 1).value for r in range(2, max_row + 1) if ws.cell(r, 1).value)
tax_sum = sum(ws.cell(r, 2).value for r in range(2, max_row + 1) if ws.cell(r, 2).value)
ws.cell(total_row, 1, prices_sum)
ws.cell(total_row, 2, tax_sum)

wb.save('prices_with_tax.xlsx')
```

Reads the prices, calculates 10% tax, and adds totals.

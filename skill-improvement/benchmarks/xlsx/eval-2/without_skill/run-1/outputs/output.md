# Add Tax Column to Excel

## Script

```python
from openpyxl import load_workbook

wb = load_workbook('prices.xlsx')
ws = wb.active

# Add tax header
ws.cell(1, 2, 'Tax (10%)')

# Add tax values
for row in range(2, ws.max_row + 1):
    price = ws.cell(row, 1).value
    if price:
        ws.cell(row, 2, price * 0.10)

# Total row
total_row = ws.max_row + 1
ws.cell(total_row, 1, 'Total')
total_price = sum(ws.cell(r, 1).value for r in range(2, total_row) if ws.cell(r, 1).value)
total_tax = sum(ws.cell(r, 2).value for r in range(2, total_row) if ws.cell(r, 2).value)
ws.cell(total_row, 1, total_price)
ws.cell(total_row, 2, total_tax)

wb.save('prices_with_tax.xlsx')
```

Adds a 10% tax column and totals at the bottom.

# CSV Data Analysis - Transaction Summary

After reading the csv-data-summarizer SKILL.md, I followed the Financial Transaction Summary pattern using pandas.

## Analysis Script

```python
import pandas as pd
from datetime import datetime

df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])

# Using the skill's analyze_transactions pattern
analysis = {
    'total_transactions': len(df),
    'date_range': {
        'start': df['date'].min().strftime('%Y-%m-%d'),
        'end': df['date'].max().strftime('%Y-%m-%d'),
    },
    'income': df[df['amount'] > 0]['amount'].sum(),
    'expenses': abs(df[df['amount'] < 0]['amount'].sum()),
}
analysis['net'] = analysis['income'] - analysis['expenses']

# Category breakdown per skill pattern
by_category = df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])

# Monthly summary
df['month'] = df['date'].dt.to_period('M')
monthly_totals = df.groupby('month')['amount'].sum()
```

## Financial Summary

### Income
| Source | Amount |
|--------|--------|
| Payroll Deposit | $5,500.00 |
| Client Invoice Payment | $3,200.00 |
| Consulting Fee | $1,800.00 |
| **Total Income** | **$10,500.00** |

### Expenses
**Total Expenses: $3,338.05**

### Category Breakdown (9 categories)
| Category | Total | Count | Average |
|----------|-------|-------|---------|
| Housing | $2,200.00 | 1 | $2,200.00 |
| Insurance | $280.00 | 1 | $280.00 |
| Utilities | $269.99 | 3 | $90.00 |
| Groceries | $211.07 | 2 | $105.54 |
| Shopping | $157.98 | 2 | $79.00 |
| Transportation | $70.80 | 2 | $35.40 |
| Food & Drink | $69.25 | 2 | $34.63 |
| Health | $49.99 | 1 | $49.99 |
| Entertainment | $28.97 | 3 | $9.66 |

### Monthly Cash Flow
- January 2026 is the only month in this dataset
- Total inflows: $10,500.00
- Total outflows: $3,338.05
- **Net cash flow: +$7,161.95**

### Data Quality Check
- Missing values: None detected across all 5 columns
- Duplicates: None found
- Date range: Single month (January 2026)

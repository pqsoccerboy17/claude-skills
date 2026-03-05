# Transaction Analysis Report

I read the SKILL.md for csv-data-summarizer first, then used the pandas-based `analyze_transactions` pattern from the skill.

## Approach

Used pandas to load and analyze the CSV data following the Financial Transaction Summary pattern from the skill:

```python
import pandas as pd

df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])

# Income vs Expenses
income = df[df['amount'] > 0]['amount'].sum()
expenses = abs(df[df['amount'] < 0]['amount'].sum())
net = income - expenses

# Category breakdown
by_category = df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])

# Monthly summary
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby('month')['amount'].sum()
```

## Results

### Overview
- Total Transactions: 20
- Date Range: 2026-01-03 to 2026-01-30
- All transactions are within January 2026

### Income Summary
- Payroll Deposit: $5,500.00
- Client Invoice Payment: $3,200.00
- Consulting Fee: $1,800.00
- **Total Income: $10,500.00**

### Expense Summary
- **Total Expenses: $3,338.05**

### Spending by Category
| Category | Total Spent | # Transactions |
|----------|------------|----------------|
| Housing | $2,200.00 | 1 |
| Insurance | $280.00 | 1 |
| Utilities | $269.99 | 3 |
| Groceries | $211.07 | 2 |
| Shopping | $157.98 | 2 |
| Transportation | $70.80 | 2 |
| Food & Drink | $69.25 | 2 |
| Health | $49.99 | 1 |
| Entertainment | $28.97 | 3 |

9 expense categories identified.

### Monthly Cash Flow (January 2026)
- Income: $10,500.00
- Expenses: $3,338.05
- **Net Cash Flow: +$7,161.95**

### Data Quality
- No missing values detected
- No duplicate transactions
- All amounts properly formatted as numeric values

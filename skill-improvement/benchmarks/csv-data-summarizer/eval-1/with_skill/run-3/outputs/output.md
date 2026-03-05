# Transaction Analysis

Read SKILL.md first - using the csv-data-summarizer skill's pandas-based approach.

## Method

Applied the `analyze_transactions` function pattern from the skill with `parse_dates=['date']` and pandas groupby operations for category and monthly breakdowns.

```python
import pandas as pd

df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])

income = df[df['amount'] > 0]['amount'].sum()
expenses = abs(df[df['amount'] < 0]['amount'].sum())
net = income - expenses

by_category = df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby('month')['amount'].sum()
```

## Results

**Dataset:** 20 transactions, Jan 3-30 2026, 5 columns (date, description, amount, category, account)

### Income: $10,500.00
- Payroll Deposit: $5,500.00
- Client Invoice Payment: $3,200.00
- Consulting Fee: $1,800.00

### Expenses: $3,338.05

### Spending by Category
1. Housing - $2,200.00 (1 transaction)
2. Insurance - $280.00 (1 transaction)
3. Utilities - $269.99 (3 transactions: Electric $145, Internet $79.99, Water $45)
4. Groceries - $211.07 (2 transactions: Whole Foods $132.45, Trader Joes $78.62)
5. Shopping - $157.98 (2 transactions: Target $89.99, Amazon $67.99)
6. Transportation - $70.80 (2 transactions: Gas $52.30, Uber $18.50)
7. Food & Drink - $69.25 (2 transactions: Restaurant $64.50, Starbucks $4.75)
8. Health - $49.99 (1 transaction: Gym)
9. Entertainment - $28.97 (3 transactions: Netflix $15.99, Spotify $9.99, iCloud $2.99)

### Monthly Cash Flow - January 2026
- Income: $10,500.00
- Expenses: $3,338.05
- **Net: +$7,161.95 surplus**

### Data Quality
- No missing values
- No duplicates
- Clean numeric formatting throughout

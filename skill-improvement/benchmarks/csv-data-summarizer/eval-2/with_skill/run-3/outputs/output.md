# Spending Analysis with Category Rankings

After reading the csv-data-summarizer SKILL.md, I applied pandas groupby operations.

```python
import pandas as pd
df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])
exp = df[df['amount'] < 0].copy()
exp['spent'] = exp['amount'].abs()

# Ranked categories
cat_ranked = exp.groupby('category')['spent'].sum().sort_values(ascending=False)

# By account
acct = exp.groupby('account')['spent'].agg(['sum','count','mean'])

# Flag outliers using IQR
Q1 = exp['spent'].quantile(0.25)
Q3 = exp['spent'].quantile(0.75)
IQR = Q3 - Q1
upper = Q3 + 1.5 * IQR
flagged = exp[exp['spent'] > upper]
```

## Category Rankings

| # | Category | Amount | Share |
|---|----------|--------|-------|
| 1 | Housing | $2,200.00 | 65.9% |
| 2 | Insurance | $280.00 | 8.4% |
| 3 | Utilities | $269.99 | 8.1% |
| 4 | Groceries | $211.07 | 6.3% |
| 5 | Shopping | $157.98 | 4.7% |
| 6 | Transportation | $70.80 | 2.1% |
| 7 | Food & Drink | $69.25 | 2.1% |
| 8 | Health | $49.99 | 1.5% |
| 9 | Entertainment | $28.97 | 0.9% |

Housing is the dominant expense category.

## Unusual Transactions

Using IQR method (Q1=$15.99, Q3=$132.45, IQR=$116.46, upper fence=$307.14):
- **Rent Payment: $2,200.00** - well above the upper fence, clear outlier

## Account Split

- **Chase Checking**: $3,086.60 total expenses (11 transactions) - handles fixed costs (rent, insurance, utilities) and groceries
- **Amex Gold**: $251.45 total expenses (6 transactions) - discretionary spending (shopping, dining, entertainment)

## Data Quality Notes
- Zero missing values across all columns
- No duplicate records
- Data covers single month (Jan 2026) so trend analysis not possible

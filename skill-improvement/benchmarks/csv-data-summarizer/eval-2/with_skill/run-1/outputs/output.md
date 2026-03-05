# Spending Category Analysis & Account Breakdown

Read the csv-data-summarizer SKILL.md first, then applied the pandas-based analysis patterns.

## Approach

```python
import pandas as pd

df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])

# Filter expenses only
expenses = df[df['amount'] < 0].copy()
expenses['abs_amount'] = expenses['amount'].abs()

# Category ranking
ranked = expenses.groupby('category')['abs_amount'].agg(['sum', 'count']).sort_values('sum', ascending=False)

# Account breakdown
by_account = expenses.groupby('account')['abs_amount'].agg(['sum', 'count'])

# Outlier detection - flag transactions > 2 std deviations from mean
mean_expense = expenses['abs_amount'].mean()
std_expense = expenses['abs_amount'].std()
threshold = mean_expense + 2 * std_expense
outliers = expenses[expenses['abs_amount'] > threshold]
```

## Spending Categories - Ranked by Total

| Rank | Category | Total Spent | # Transactions |
|------|----------|------------|----------------|
| 1 | Housing | $2,200.00 | 1 |
| 2 | Insurance | $280.00 | 1 |
| 3 | Utilities | $269.99 | 3 |
| 4 | Groceries | $211.07 | 2 |
| 5 | Shopping | $157.98 | 2 |
| 6 | Transportation | $70.80 | 2 |
| 7 | Food & Drink | $69.25 | 2 |
| 8 | Health | $49.99 | 1 |
| 9 | Entertainment | $28.97 | 3 |

**Housing is the largest category at $2,200.00**, representing 65.9% of all expenses.

## Unusual/Notable Transactions

- **Rent Payment ($2,200.00)** - Statistical outlier. This single transaction is 11.2x the average expense of $196.36. It's the only Housing transaction and far exceeds all other individual expenses.
- The mean expense is $196.36 with a std deviation of $516.97. The rent payment exceeds the mean + 2*std threshold.

## Spending by Account

| Account | Total Spent | # Transactions | % of Expenses |
|---------|------------|----------------|---------------|
| Chase Checking | $3,086.60 | 11 | 92.5% |
| Amex Gold | $251.45 | 6 | 7.5% |

Chase Checking handles most of the spending ($3,086.60 across 11 transactions), including all the large fixed costs (rent, insurance, utilities). Amex Gold is used primarily for discretionary spending ($251.45 across 6 transactions) - shopping, dining, and subscriptions.

## Data Quality

- No missing values detected across all 5 columns (date, description, amount, category, account)
- No duplicate entries found
- All amounts are properly numeric
- Date range covers a single month (January 2026)

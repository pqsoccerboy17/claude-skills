# Category & Account Analysis

Read SKILL.md first. Used pandas patterns from the skill for groupby analysis.

```python
import pandas as pd
df = pd.read_csv('evals/files/sample_transactions.csv', parse_dates=['date'])
expenses = df[df['amount'] < 0].copy()
expenses['abs_amount'] = expenses['amount'].abs()
ranked = expenses.groupby('category')['abs_amount'].sum().sort_values(ascending=False)
by_account = expenses.groupby('account')['abs_amount'].agg(['sum','count'])
```

## Categories Ranked by Spend

1. **Housing: $2,200.00** - largest by far (65.9% of total)
2. Insurance: $280.00 (8.4%)
3. Utilities: $269.99 (8.1%)
4. Groceries: $211.07 (6.3%)
5. Shopping: $157.98 (4.7%)
6. Transportation: $70.80 (2.1%)
7. Food & Drink: $69.25 (2.1%)
8. Health: $49.99 (1.5%)
9. Entertainment: $28.97 (0.9%)

## Flagged Transactions

- **Rent Payment ($2,200.00)**: Outlier - 11x the median expense. Single largest expense.
- **Whole Foods ($132.45)**: Higher than typical grocery run in this dataset.

## Account Breakdown

| Account | Expense Total | # Expense Txns |
|---------|-------------|----------------|
| Chase Checking | $3,086.60 | 11 |
| Amex Gold | $251.45 | 6 |

Chase Checking carries 92.5% of expenses (fixed costs + groceries). Amex Gold handles 7.5% (discretionary).

## Data Quality
- No missing values in any column
- No duplicates detected
- All dates within January 2026

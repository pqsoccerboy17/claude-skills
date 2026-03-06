---
name: csv-data-summarizer
description: "Quick analysis and summarization of CSV/tabular data. Use when: (1) analyzing exported financial data, (2) summarizing transaction reports, (3) generating statistics from spreadsheet exports, (4) comparing datasets, (5) creating data summaries for reporting. Triggers: analyze CSV, summarize data, data statistics, financial analysis, transaction summary, data report."
license: MIT
---

# CSV Data Summarizer Skill

Fast analysis and summarization of CSV data for business intelligence.

## Quick Start

```python
import pandas as pd

def quick_summary(csv_path):
    """Generate comprehensive data summary"""
    df = pd.read_csv(csv_path)

    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict() if df.select_dtypes(include='number').shape[1] > 0 else {},
    }

    return summary
```

## Business Analysis Patterns

### Financial Transaction Summary

```python
import pandas as pd
from datetime import datetime

def analyze_transactions(csv_path, date_col='date', amount_col='amount', category_col='category'):
    """Comprehensive transaction analysis for Treehouse LLC or consulting"""
    df = pd.read_csv(csv_path, parse_dates=[date_col])

    analysis = {
        'total_transactions': len(df),
        'date_range': {
            'start': df[date_col].min().strftime('%Y-%m-%d'),
            'end': df[date_col].max().strftime('%Y-%m-%d'),
        },
        'amounts': {
            'total': df[amount_col].sum(),
            'average': df[amount_col].mean(),
            'median': df[amount_col].median(),
            'min': df[amount_col].min(),
            'max': df[amount_col].max(),
        },
    }

    # Income vs Expenses
    if amount_col in df.columns:
        analysis['income'] = df[df[amount_col] > 0][amount_col].sum()
        analysis['expenses'] = abs(df[df[amount_col] < 0][amount_col].sum())
        analysis['net'] = analysis['income'] - analysis['expenses']

    # Category breakdown
    if category_col in df.columns:
        analysis['by_category'] = df.groupby(category_col)[amount_col].agg(['sum', 'count', 'mean']).to_dict()

    # Monthly summary
    df['month'] = df[date_col].dt.to_period('M')
    analysis['monthly_totals'] = df.groupby('month')[amount_col].sum().to_dict()

    return analysis
```

### Property Revenue Analysis (Real Estate)

```python
def analyze_property_revenue(csv_path):
    """Analyze rental income by property for Treehouse LLC"""
    df = pd.read_csv(csv_path)

    # Assume columns: property, unit, tenant, amount, date, type
    analysis = {
        'total_revenue': df[df['type'] == 'rent']['amount'].sum(),
        'total_properties': df['property'].nunique(),
        'total_units': df['unit'].nunique(),
    }

    # Revenue by property
    by_property = df[df['type'] == 'rent'].groupby('property')['amount'].agg(['sum', 'count', 'mean'])
    analysis['by_property'] = by_property.to_dict()

    # Occupancy indicator (if we have vacancy data)
    if 'status' in df.columns:
        analysis['occupancy_rate'] = (df['status'] == 'occupied').mean() * 100

    return analysis
```

### Consulting Hours/Revenue

```python
def analyze_consulting_time(csv_path):
    """Analyze consulting hours and revenue by client"""
    df = pd.read_csv(csv_path)

    # Assume columns: client, project, hours, rate, date
    df['revenue'] = df['hours'] * df['rate']

    return {
        'total_hours': df['hours'].sum(),
        'total_revenue': df['revenue'].sum(),
        'average_rate': df['rate'].mean(),
        'by_client': df.groupby('client').agg({
            'hours': 'sum',
            'revenue': 'sum',
            'rate': 'mean'
        }).to_dict(),
        'by_project': df.groupby(['client', 'project'])['revenue'].sum().to_dict(),
    }
```

### SaaS Metrics (Tap)

```python
def analyze_saas_metrics(csv_path):
    """Analyze SaaS business metrics"""
    df = pd.read_csv(csv_path, parse_dates=['date'])

    metrics = {}

    # MRR calculation (if subscription data)
    if 'mrr' in df.columns:
        latest = df.sort_values('date').iloc[-1]
        metrics['current_mrr'] = latest['mrr']
        metrics['mrr_growth'] = df.groupby(df['date'].dt.to_period('M'))['mrr'].last().pct_change().iloc[-1] * 100

    # User metrics
    if 'active_users' in df.columns:
        metrics['total_users'] = df['active_users'].iloc[-1]
        metrics['dau_growth'] = df['active_users'].pct_change().mean() * 100

    # Churn analysis
    if 'churned' in df.columns:
        metrics['churn_rate'] = df['churned'].mean() * 100

    # Revenue per user
    if 'revenue' in df.columns and 'active_users' in df.columns:
        metrics['arpu'] = df['revenue'].sum() / df['active_users'].mean()

    return metrics
```

## Data Cleaning Utilities

```python
def clean_financial_csv(csv_path, output_path=None):
    """Clean and standardize financial CSV data"""
    df = pd.read_csv(csv_path)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # Handle currency formatting
    currency_cols = [col for col in df.columns if any(x in col for x in ['amount', 'balance', 'total', 'price'])]
    for col in currency_cols:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('$', '').str.replace(',', '').astype(float)

    # Parse dates
    date_cols = [col for col in df.columns if any(x in col for x in ['date', 'time', 'created', 'updated'])]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass

    # Remove duplicates
    original_len = len(df)
    df = df.drop_duplicates()
    duplicates_removed = original_len - len(df)

    # Handle missing values
    missing_summary = df.isnull().sum().to_dict()

    if output_path:
        df.to_csv(output_path, index=False)

    return {
        'cleaned_data': df,
        'duplicates_removed': duplicates_removed,
        'missing_values': missing_summary,
        'row_count': len(df),
    }
```

## Report Generation

### Text Summary

```python
def generate_text_summary(analysis: dict) -> str:
    """Generate human-readable summary from analysis"""
    lines = [
        "# Data Summary Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    if 'total_transactions' in analysis:
        lines.append(f"## Transaction Overview")
        lines.append(f"- Total Transactions: {analysis['total_transactions']:,}")
        lines.append(f"- Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
        lines.append("")

    if 'amounts' in analysis:
        lines.append(f"## Financial Summary")
        lines.append(f"- Total: ${analysis['amounts']['total']:,.2f}")
        lines.append(f"- Average: ${analysis['amounts']['average']:,.2f}")
        lines.append(f"- Range: ${analysis['amounts']['min']:,.2f} to ${analysis['amounts']['max']:,.2f}")

    if 'income' in analysis:
        lines.append("")
        lines.append(f"## Income vs Expenses")
        lines.append(f"- Income: ${analysis['income']:,.2f}")
        lines.append(f"- Expenses: ${analysis['expenses']:,.2f}")
        lines.append(f"- Net: ${analysis['net']:,.2f}")

    return '\n'.join(lines)
```

### Export to Excel with Formatting

```python
def export_analysis_to_excel(analysis: dict, output_path: str):
    """Export analysis to formatted Excel file"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    # Header styling
    header_fill = PatternFill('solid', start_color='366092')
    header_font = Font(bold=True, color='FFFFFF')

    row = 1
    for section, data in analysis.items():
        # Section header
        ws.cell(row=row, column=1, value=section.replace('_', ' ').title())
        ws.cell(row=row, column=1).font = Font(bold=True, size=14)
        row += 1

        if isinstance(data, dict):
            for key, value in data.items():
                ws.cell(row=row, column=1, value=key)
                ws.cell(row=row, column=2, value=str(value) if not isinstance(value, (int, float)) else value)
                row += 1
        else:
            ws.cell(row=row, column=1, value=str(data))
            row += 1

        row += 1  # Blank row between sections

    # Auto-width columns
    for col in ws.columns:
        max_length = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_length + 2, 50)

    wb.save(output_path)
```

## Command Line Usage

```bash
# Quick summary
python scripts/summarize.py data.csv

# Financial analysis with output
python scripts/summarize.py transactions.csv --type financial --output report.json

# Generate Excel report
python scripts/summarize.py data.csv --excel-output report.xlsx
```

## Integration Examples

### With File Organizer
```python
# After organizing bank statements, summarize all
from pathlib import Path

statements_dir = Path('~/Finance/Banking/2024')
all_data = []

for csv in statements_dir.rglob('*.csv'):
    df = pd.read_csv(csv)
    df['source_file'] = csv.name
    all_data.append(df)

combined = pd.concat(all_data)
analysis = analyze_transactions(combined)
```

### Scheduled Reports
```bash
# Add to crontab for monthly reports
0 0 1 * * python ~/claude-skills/data-analysis/csv-data-summarizer/scripts/monthly_report.py
```

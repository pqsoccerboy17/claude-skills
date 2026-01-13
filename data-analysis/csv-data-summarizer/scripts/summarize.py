#!/usr/bin/env python3
"""
CSV Data Summarizer - Quick analysis utility for business data
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


def detect_column_types(df):
    """Auto-detect column purposes based on names and content"""
    types = {
        'date_cols': [],
        'amount_cols': [],
        'category_cols': [],
        'id_cols': [],
    }

    date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
    amount_keywords = ['amount', 'balance', 'total', 'price', 'cost', 'revenue', 'fee']
    category_keywords = ['category', 'type', 'status', 'group', 'class']
    id_keywords = ['id', 'number', 'ref', 'code']

    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in date_keywords):
            types['date_cols'].append(col)
        elif any(kw in col_lower for kw in amount_keywords):
            types['amount_cols'].append(col)
        elif any(kw in col_lower for kw in category_keywords):
            types['category_cols'].append(col)
        elif any(kw in col_lower for kw in id_keywords):
            types['id_cols'].append(col)

    return types


def basic_summary(df):
    """Generate basic data summary"""
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': df.columns.tolist(),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': df.isnull().sum().to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
    }


def numeric_summary(df):
    """Summary statistics for numeric columns"""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        return {}

    stats = numeric_df.describe()
    return {
        col: {
            'count': int(stats[col]['count']),
            'mean': round(stats[col]['mean'], 2),
            'std': round(stats[col]['std'], 2),
            'min': round(stats[col]['min'], 2),
            'max': round(stats[col]['max'], 2),
            'sum': round(numeric_df[col].sum(), 2),
        }
        for col in numeric_df.columns
    }


def financial_analysis(df, col_types):
    """Specialized analysis for financial data"""
    analysis = {}

    # Parse dates
    for date_col in col_types['date_cols']:
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            analysis['date_range'] = {
                'column': date_col,
                'start': df[date_col].min().strftime('%Y-%m-%d'),
                'end': df[date_col].max().strftime('%Y-%m-%d'),
                'span_days': (df[date_col].max() - df[date_col].min()).days,
            }
            break
        except:
            continue

    # Amount analysis
    for amount_col in col_types['amount_cols']:
        if amount_col in df.columns:
            # Clean currency formatting if needed
            if df[amount_col].dtype == 'object':
                df[amount_col] = df[amount_col].str.replace('$', '').str.replace(',', '').astype(float)

            positive = df[df[amount_col] > 0][amount_col]
            negative = df[df[amount_col] < 0][amount_col]

            analysis['amounts'] = {
                'column': amount_col,
                'total': round(df[amount_col].sum(), 2),
                'income': round(positive.sum(), 2) if len(positive) > 0 else 0,
                'expenses': round(abs(negative.sum()), 2) if len(negative) > 0 else 0,
                'average': round(df[amount_col].mean(), 2),
                'transaction_count': len(df),
            }

            # Net calculation
            if 'income' in analysis['amounts'] and 'expenses' in analysis['amounts']:
                analysis['amounts']['net'] = round(
                    analysis['amounts']['income'] - analysis['amounts']['expenses'], 2
                )
            break

    # Category breakdown
    for cat_col in col_types['category_cols']:
        if cat_col in df.columns and col_types['amount_cols']:
            amount_col = col_types['amount_cols'][0]
            breakdown = df.groupby(cat_col)[amount_col].agg(['sum', 'count', 'mean']).round(2)
            analysis['by_category'] = {
                'column': cat_col,
                'breakdown': breakdown.to_dict('index'),
            }
            break

    return analysis


def generate_report(analysis, format='text'):
    """Generate human-readable report"""
    if format == 'json':
        return json.dumps(analysis, indent=2, default=str)

    lines = [
        "=" * 60,
        "DATA SUMMARY REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
    ]

    if 'basic' in analysis:
        lines.append("BASIC INFO")
        lines.append("-" * 40)
        lines.append(f"Rows: {analysis['basic']['row_count']:,}")
        lines.append(f"Columns: {analysis['basic']['column_count']}")
        lines.append(f"Memory: {analysis['basic']['memory_usage_mb']:.2f} MB")
        lines.append("")

    if 'financial' in analysis:
        fin = analysis['financial']

        if 'date_range' in fin:
            lines.append("DATE RANGE")
            lines.append("-" * 40)
            lines.append(f"{fin['date_range']['start']} to {fin['date_range']['end']}")
            lines.append(f"Span: {fin['date_range']['span_days']} days")
            lines.append("")

        if 'amounts' in fin:
            lines.append("FINANCIAL SUMMARY")
            lines.append("-" * 40)
            lines.append(f"Total: ${fin['amounts']['total']:,.2f}")
            if 'income' in fin['amounts']:
                lines.append(f"Income: ${fin['amounts']['income']:,.2f}")
                lines.append(f"Expenses: ${fin['amounts']['expenses']:,.2f}")
                lines.append(f"Net: ${fin['amounts']['net']:,.2f}")
            lines.append(f"Transactions: {fin['amounts']['transaction_count']:,}")
            lines.append(f"Average: ${fin['amounts']['average']:,.2f}")
            lines.append("")

        if 'by_category' in fin:
            lines.append(f"BY {fin['by_category']['column'].upper()}")
            lines.append("-" * 40)
            for cat, stats in fin['by_category']['breakdown'].items():
                lines.append(f"  {cat}: ${stats['sum']:,.2f} ({stats['count']} transactions)")
            lines.append("")

    if 'numeric' in analysis:
        lines.append("NUMERIC COLUMNS")
        lines.append("-" * 40)
        for col, stats in analysis['numeric'].items():
            lines.append(f"  {col}:")
            lines.append(f"    Sum: {stats['sum']:,.2f}  Avg: {stats['mean']:,.2f}")
            lines.append(f"    Range: {stats['min']:,.2f} to {stats['max']:,.2f}")
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Analyze CSV data')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('--type', choices=['basic', 'financial', 'full'], default='full',
                        help='Analysis type')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format')
    parser.add_argument('--excel-output', help='Export to Excel file')

    args = parser.parse_args()

    # Read CSV
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        return 1

    # Detect column types
    col_types = detect_column_types(df)

    # Build analysis
    analysis = {}

    if args.type in ['basic', 'full']:
        analysis['basic'] = basic_summary(df)
        analysis['numeric'] = numeric_summary(df)

    if args.type in ['financial', 'full']:
        analysis['financial'] = financial_analysis(df.copy(), col_types)

    # Output
    report = generate_report(analysis, args.format)
    print(report)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        print(f"\nAnalysis saved to: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())

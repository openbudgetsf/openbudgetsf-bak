import json
import os
import shutil
import sqlite3

def year_to_fiscal_range(year):
    return 'FY{}-{}'.format(str(year)[2:], str(year + 1)[2:])

def output_data(key_column, fiscal_year, is_revenue, output_key, base_path):
    data = c.execute("""
        SELECT {key_column}, SUM(amount)
            FROM budget_items
        WHERE fiscal_year = {fiscal_year}
            AND is_revenue = '{is_revenue}'
        GROUP BY {key_column}""".format(
            key_column=key_column,
            is_revenue='Revenue' if is_revenue else 'Spending',
            fiscal_year=fiscal_year))

    fiscal_year_range = year_to_fiscal_range(fiscal_year)
    output_data = [{
        output_key: row[0],
        "total": row[1],
        "fiscal_year_range": fiscal_year_range,
        "budget_type": 1
    } for row in data]

    os.makedirs(base_path, exist_ok=True)
    with open(os.path.join(base_path, '{}.json'.format(fiscal_year_range)), 'w') as f:
        f.write(json.dumps(output_data))

db_path = 'data/budget.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

base_path = 'overrides/data/compare'
try:
    shutil.rmtree(base_path)
except IOError:
    pass

os.makedirs(base_path)

years = [row[0] for row in c.execute("SELECT DISTINCT(fiscal_year) FROM budget_items")]

for directory_suffix, is_revenue in {'expenses': False, 'revenue': True}.items():
    is_revenue_base_path = '{}/fiscal-years-{}'.format(base_path, directory_suffix)

    for year in years:
        dirs = (
            ('department', 'dept', 'depts'),
            ('account_category', 'character', 'account-cats')
        )

        for output_key, key_column, bottom_directory in dirs:
            key_base_path = '{}/{}'.format(is_revenue_base_path, bottom_directory)
            output_data(key_column=key_column, fiscal_year=year, is_revenue=is_revenue,
                        output_key=output_key, base_path=key_base_path)

    total_query = c.execute("""
        SELECT fiscal_year, SUM(amount)
            FROM budget_items
        WHERE is_revenue = '{is_revenue}'
        GROUP BY fiscal_year
    """.format(is_revenue='Revenue' if is_revenue else 'Spending'))

    totals = [{
        "fiscal_year_range": year_to_fiscal_range(row[0]),
        "budget_type": 1,
        "total": row[1]
    } for row in total_query]

    with open(os.path.join(is_revenue_base_path, 'totals.json'), 'w') as f:
        f.write(json.dumps(totals))
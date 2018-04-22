import os
import sqlite3

def year_to_fiscal_range(year):
    return 'FY{}-{}'.format(str(year)[2:], str(year + 1)[2:])

db_path = 'data/budget.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

years = [row[0] for row in c.execute("SELECT DISTINCT(fiscal_year) FROM budget_items")]

for year in years:
    data = c.execute("""
        SELECT character, is_revenue, fund_type_code, character, SUM(amount)
            FROM budget_items
        WHERE fiscal_year = {fiscal_year}
        GROUP BY character, is_revenue, fund_type_code, character""".format(fiscal_year=year))

    fiscal_year_range = year_to_fiscal_range(year)
    output_data = []
    for row in data:
        row = [fiscal_year_range] + list(row)
        row[2] = 'Revenue' if row[2] == 'Revenue' else 'Expense'

        # eliminating negative values removes transfer adjustments (see
        # http://openbook.sfgov.org/openbooks/ccsf_content/BudgetHelp/Glossary.html#Adjust),
        # which makes the fund totals gross instead of net, but has the advantage of
        # making the links and nodes line up and not requiring refactoring of the sankey
        # code
        if row[-1] > 0:
            output_data.append(','.join([str(r) for r in row]))

    base_path = 'data/output/flow'
    output_path = os.path.join(base_path, '{}__proposed.csv'.format(fiscal_year_range))
    os.makedirs(base_path, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write('budget_year,department,account_type,fund_code,account_category,amount\n')
        f.write('\n'.join(output_data))
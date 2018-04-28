import json
import os
import shutil
import sqlite3

def year_to_fiscal_range(year):
    return 'FY{}-{}'.format(str(year)[2:], str(year + 1)[2:])

db_path = 'data/budget.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

tree_base_path = 'data/output/tree'
sunburst_base_path = 'data/output/sunburst'

for base_path in [tree_base_path, sunburst_base_path]:
    try:
        shutil.rmtree(base_path)
    except IOError:
        pass

    os.makedirs(base_path)

years = [row[0] for row in c.execute("SELECT DISTINCT(fiscal_year) FROM budget_items")]

for year in years[:1]:
    for is_revenue in [True, False][:1]:
        keys = ['org_group', 'dept', 'program', 'character', 'object', 'sub_object']

        def select_keys(remaining_keys=keys, select_columns=[], select_values=[]):
            # print(select_values)
            remaining_keys = list(remaining_keys)
            select_columns = list(select_columns)

            key = remaining_keys.pop(0)
            query = """
                SELECT {key}, SUM(amount)
                    FROM budget_items
                WHERE fiscal_year = {fiscal_year}
                    AND is_revenue = '{is_revenue}'
                    {select_columns}
                GROUP BY {key}""".format(
                    fiscal_year=year,
                    key=key,
                    is_revenue='Revenue' if is_revenue else 'Spending',
                    select_columns=''.join([' AND {}'.format(c) for c in select_columns]))
            # print(query)
            rows = list(c.execute(query))

            values = []
            sunburst_data = []
            for row in rows:
                value_key = 'revenue' if is_revenue else 'expense'
                other_value_key = 'expense' if is_revenue else 'revenue'
                row_data = {
                    'key': row[0],
                    'level': key,
                    'data': {
                        'amount': row[1],
                        value_key: row[1],
                        other_value_key: 0
                    }
                }
                sunburst_data.append('{},{}'.format('|'.join(select_values + [row[0]]), row[1]))

                if len(remaining_keys) > 0:
                    new_select_column = "{key} = '{value}'".format(key=key, value=row[0].replace("'", "''"))
                    new_values, new_sunburst_data = select_keys(remaining_keys, select_columns + [new_select_column], select_values + [row[0]])
                    if len(new_values) > 0:
                        row_data['values'] = new_values
                    sunburst_data.extend(new_sunburst_data)
                values.append(row_data)

            return values, sunburst_data

        total_amount = list(c.execute("""
            SELECT SUM(amount)
                FROM budget_items
            WHERE fiscal_year = {fiscal_year}
                AND is_revenue = '{is_revenue}'
        """.format(
            fiscal_year=year,
            is_revenue='Revenue' if is_revenue else 'Spending')))[0][0]

        value_key = 'revenue' if is_revenue else 'expense'
        other_value_key = 'expense' if is_revenue else 'revenue'
        all_values, all_sunburst_data = select_keys()
        budget_data = {
            'key': 'Budget',
            'values': all_values,
            'data': {
                'amount': total_amount,
                value_key: total_amount,
                other_value_key: 0
            }
        }

        fiscal_year_range = year_to_fiscal_range(year)
        output_path = os.path.join(tree_base_path, 'Adopted.{}.{}.json'.format(
            'Revenue' if is_revenue else 'Expense', fiscal_year_range))

        with open(output_path, 'w') as f:
            f.write(json.dumps(budget_data))

        output_path = os.path.join(sunburst_base_path, 'Adopted.{}.{}.csv'.format(
            'Revenue' if is_revenue else 'Expense', fiscal_year_range))

        with open(output_path, 'w') as f:
            f.write('\n'.join(all_sunburst_data))

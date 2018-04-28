import csv
import os
import sqlite3

db_path = 'data/budget.db'

try:
    os.remove(db_path)
except OSError:
    pass

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
    CREATE TABLE budget_items (
        fiscal_year int,
        is_revenue varchar(16),
        related_gov_unit varchar(255),
        org_group_code varchar(255),
        org_group varchar(255),
        dept_code varchar(255),
        dept varchar(255),
        program_code varchar(255),
        program varchar(255),
        character_code varchar(255),
        character varchar(255),
        object_code varchar(255),
        object varchar(255),
        sub_object_code varchar(255),
        sub_object varchar(255),
        fund_type_code varchar(255),
        fund_type varchar(255),
        fund_code varchar(255),
        fund varchar(255),
        fund_category_code varchar(255),
        fund_category varchar(255),
        amount int
    )
""")

c.execute("CREATE INDEX fiscal_year_is_revenue_idx ON budget_items (fiscal_year, is_revenue)")
c.execute("CREATE INDEX org_group_dept_program_idx ON budget_items (org_group, dept, program)")

with open('data/raw/Budget.csv') as f:
    csv_reader = csv.reader(f)
    for line_index, line in enumerate(csv_reader):
        if line_index > 0:
            values = ['"{}"'.format(value) for value in line[:-1]]
            values += [line[-1].replace(',', '')]
            command = "INSERT INTO budget_items VALUES ({})".format(', '.join(values))
            c.execute(command)

        if line_index % 10000 == 0:
            print('{} rows consumed'.format(line_index))

conn.commit()

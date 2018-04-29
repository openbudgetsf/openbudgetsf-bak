import csv
import os
import sqlite3

db_path = 'data/lobbying.db'

try:
    os.remove(db_path)
except OSError:
    pass

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
    CREATE TABLE political_contributions (
        date varchar(16),
        lobbyist varchar(255),
        lobbyist_firm varchar(255),
        official varchar(255),
        official_department varchar(255),
        payee varchar(255),
        source_of_funds varchar(255),
        amount int
    )
""")

with open('data/raw/_Known_Issue__Lobbyist_Activity_-_Political_Contributions.csv') as f:
    csv_reader = csv.reader(f)
    for line_index, line in enumerate(csv_reader):
        if line_index > 0:
            values = ['"{}"'.format(value) for value in line[:-1]]
            values += [line[-1].replace(',', '').replace('$', '')]
            command = "INSERT INTO political_contributions VALUES ({})".format(', '.join(values))
            c.execute(command)

conn.commit()
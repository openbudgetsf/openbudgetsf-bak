import json
import os
import shutil
import sqlite3

def year_to_fiscal_range(year):
    return 'FY{}-{}'.format(str(year)[2:], str(year + 1)[2:])

db_path = 'data/lobbying.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

base_path = 'overrides/data/lobbying/force-layout'
try:
    shutil.rmtree(base_path)
except IOError:
    pass

os.makedirs(base_path)

officials = [row[0] for row in c.execute("SELECT DISTINCT(official) FROM political_contributions WHERE date LIKE '%2015'")]
nodes = [{'id': official, 'group': 1} for official in officials]

sources_of_funds = [row[0] for row in c.execute("SELECT DISTINCT(source_of_funds) FROM political_contributions WHERE date LIKE '%2015'")]
nodes.extend([{'id': source_of_funds, 'group': 2} for source_of_funds in sources_of_funds])

contributions_result = c.execute("SELECT official, source_of_funds, SUM(amount) FROM political_contributions WHERE date LIKE '%2015' GROUP BY official, source_of_funds")
contributions = [{'source': source_of_funds, 'target': official, 'value': amount} for official, source_of_funds, amount in contributions_result]

data = {'nodes': nodes, 'links': contributions}

output_path = os.path.join(base_path, 'data.json')
with open(output_path, 'w') as f:
    f.write(json.dumps(data, indent=4))
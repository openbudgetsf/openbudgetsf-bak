#!/bin/bash
source venv/bin/activate

echo -e "Converting budget CSV data to a SQLite table..."
time python data/scripts/budget_csv_to_sqlite.py

echo -e "\nConverting budget SQLite data to compare visualization format..."
time python data/scripts/budget_sqlite_to_compare_data.py

echo -e "\nConverting budget SQLite data to compare flow format..."
time python data/scripts/budget_sqlite_to_flow_data.py

echo -e "\nConverting budget SQLite data to compare tree format..."
time python data/scripts/budget_sqlite_to_tree_data.py

echo -e "\nConverting budget SQLite data to compare tree format..."
time python data/scripts/budget_sqlite_to_tree_data.py

echo -e "\nConverting lobbying political contributions CSV data to a SQLite table..."
time python data/scripts/lobbying_contributions_csv_to_sqlite.py

echo -e "\nConverting lobbying political contributions SQLite data to force layout format..."
time python data/scripts/lobbying_contributions_sqlite_to_force_layout.py
#!/bin/bash
source venv/bin/activate

echo "Converting CSV data to a SQLite DB..."
time python data/scripts/budget_csv_to_sqlite.py

echo -e "\nConverting SQLite data to compare visualization format..."
time python data/scripts/budget_sqlite_to_compare_data.py

echo -e "\nConverting SQLite data to compare flow format..."
time python data/scripts/budget_sqlite_to_flow_data.py

echo -e "\nConverting SQLite data to compare tree format..."
time python data/scripts/budget_sqlite_to_tree_data.py
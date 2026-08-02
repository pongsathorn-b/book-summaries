#!/usr/bin/env python3
"""Fix README.md book counts correctly after migration."""
import re

with open('README.md') as f:
    txt = f.read()

# Count actual table rows per year section (exclude separator rows)
for year in ['2018','2019','2020','2021','2022','2023','2024','2025']:
    start = txt.find(f'## {year} —')
    if start == -1:
        print(f'{year}: NOT FOUND')
        continue
    rest = txt[start+10:]
    next_year_m = re.search(r'\n## \d{4} —', rest)
    end = start + 10 + next_year_m.start() if next_year_m else len(txt)
    section = txt[start:end]
    # Count actual book rows (contain a number in second column)
    rows = re.findall(r'^\| (\d+) \|', section, re.MULTILINE)
    print(f'{year}: {len(rows)} rows: {rows}')

# Update using actual row counts

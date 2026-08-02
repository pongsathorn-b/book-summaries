#!/usr/bin/env python3
"""Fix README.md book counts after migration."""
import re

with open('README.md') as f:
    txt = f.read()

changes = {}
for year in ['2018','2019','2020','2021','2022','2023','2024','2025']:
    start = txt.find(f'## {year} —')
    if start == -1:
        print(f'{year}: NOT FOUND')
        continue
    rest = txt[start+10:]
    next_year_m = re.search(r'\n## \d{4} —', rest)
    end = start + 10 + next_year_m.start() if next_year_m else len(txt)
    section = txt[start:end]
    rows = re.findall(r'^\| (\d+) \|', section, re.MULTILINE)
    print(f'{year}: {len(rows)} books')
    changes[year] = len(rows)

# Update counts
for year, count in changes.items():
    old_pattern = rf"## {year} — (\d+)"
    old_count = re.search(old_pattern, txt).group(1)
    old = f'## {year} — {old_count}'
    new = f'## {year} — {count}'
    txt = txt.replace(old, new, 1)
    print(f'  Replace: {old!r} -> {new!r}')

# Update total
old_total_m = re.search(r'\*\*Book count:\*\* (\d+)', txt)
old_total = int(old_total_m.group(1))
new_total = sum(changes.values())
txt = txt.replace(f'**Book count:** {old_total} books', f'**Book count:** {new_total} books')
print(f'Total: {old_total} -> {new_total}')

with open('README.md', 'w') as f:
    f.write(txt)

print('Done')

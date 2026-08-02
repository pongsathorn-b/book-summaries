#!/usr/bin/env python3
"""Fix README.md book counts to match actual vault."""
import re

with open('README.md', 'r') as f:
    txt = f.read()

# Actual vault counts
vault_counts = {
    '2018': 26, '2019': 26, '2020': 26,
    '2021': 24, '2022': 21, '2023': 23,
    '2024': 24, '2025': 23,
}

changes = []
for year, count in vault_counts.items():
    # Find header line
    m = re.search(rf"(## {year} — )(\d+)( books)", txt)
    if m:
        old = int(m.group(2))
        if old != count:
            txt = txt.replace(f"## {year} — {old} books", f"## {year} — {count} books", 1)
            changes.append(f"{year}: {old} -> {count}")

# Update total
old_total_m = re.search(r'\*\*Book count:\*\* (\d+)', txt)
old_total = int(old_total_m.group(1))
new_total = sum(vault_counts.values())
txt = txt.replace(f'**Book count:** {old_total} books', f'**Book count:** {new_total} books')
changes.append(f"Total: {old_total} -> {new_total}")

with open('README.md', 'w') as f:
    f.write(txt)

for c in changes:
    print(c)
print("Done!")

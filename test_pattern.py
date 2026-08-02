#!/usr/bin/env python3
import re
with open('README.md') as f:
    txt = f.read()

for year in ['2018','2019','2020','2021','2022','2023','2024','2025']:
    # Try different patterns
    for pat_str in [
        rf'## {year} — \d+ books\n\n\| # \| Title \| Author \|\n(.*?)\n(?:## \d\d\d\d|---)',
        rf'## {year} — (\d+) books\n\n(.*?)(?=\n## \d\d\d\d)',
    ]:
        m = re.search(pat_str, txt, re.DOTALL)
        print(f'{year} with pattern {pat_str[:40]!r}: {"FOUND" if m else "NOT FOUND"}')
        if m:
            print(f'  Groups: {m.groups()}')
            print(f'  Match snippet: {m.group(0)[:200]}')

#!/usr/bin/env python3
import re
with open('README.md') as f:
    txt = f.read()
for year in ['2018','2019','2020','2021','2022','2023','2024','2025']:
    start = txt.find(f'## {year} —')
    if start == -1: continue
    rest = txt[start+10:]
    m = re.search(r'\n## \d{4} —', rest)
    end = start + 10 + m.start() if m else len(txt)
    section = txt[start:end]
    nums = re.findall(r'^\| (\d+) \|', section, re.MULTILINE)
    count_m = re.search(rf'## {year} — (\d+)', txt[start:start+20])
    hdr = count_m.group(1) if count_m else '?'
    print(f'{year}: header={hdr} rows={len(nums)}')

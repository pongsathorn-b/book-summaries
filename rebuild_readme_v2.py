#!/usr/bin/env python3
"""Rebuild README year sections from actual vault files in main repo."""
import os, re

vault = '/home/pi/book-summaries/20 Sources/Books'

year_books = {}
for year_dir in sorted(os.listdir(vault)):
    year_path = os.path.join(vault, year_dir)
    if not os.path.isdir(year_path):
        continue
    books = []
    for f in sorted(os.listdir(year_path), key=lambda x: int(re.match(r'(\d+)', x).group(1)) if re.match(r'\d+', x) else 999):
        if not f.endswith('.md'):
            continue
        full = os.path.join(year_path, f)
        try:
            with open(full) as fp:
                content = fp.read()
        except:
            continue
        # Extract from frontmatter
        title_m = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
        author_m = re.search(r'^author:\s*"([^"]+)"', content, re.MULTILINE)
        if not title_m:
            # Fallback: first heading
            title_m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_m:
            title = title_m.group(1).strip()
        else:
            title = f.replace('.md', '').replace('-', ' ').title()
        if author_m:
            author = author_m.group(1).strip()
        else:
            author = "Unknown"
        num = re.match(r'(\d+)', f).group(1)
        books.append((num, title, author))
    year_books[year_dir] = books
    print(f"{year_dir}: {len(books)} books")

# Now rebuild README in worktree
with open('README.md', 'r') as f:
    txt = f.read()

# Replace each year section
for year, books in year_books.items():
    start = txt.find(f'## {year} —')
    if start == -1:
        print(f"WARNING: {year} not found in README")
        continue
    rest = txt[start+10:]
    m = re.search(r'\n## ', rest)
    end = start + 10 + m.start() if m else len(txt)
    
    rows = [f"| {num} | {title} | {author} |" for num, title, author in books]
    new_table = f"## {year} — {len(books)} books\n\n| # | Title | Author |\n|---|-------|--------|\n" + "\n".join(rows) + "\n\n"
    
    txt = txt[:start] + new_table + txt[end:]
    print(f"  Updated {year}: {len(books)} books")

# Update total
old_total_m = re.search(r'\*\*Book count:\*\* (\d+)', txt)
old_total = int(old_total_m.group(1))
new_total = sum(len(v) for v in year_books.values())
txt = txt.replace(f'**Book count:** {old_total} books', f'**Book count:** {new_total} books')
print(f"Total: {old_total} -> {new_total}")

# Update year range
txt = re.sub(r'\(2015–\d{4}\)', f'(2015–{max(year_books.keys())})', txt)

# Update footer
txt = re.sub(r'\*Built from \d+ years of reading · \d+ books · Personal knowledge graph\*',
             f'*Built from {len(year_books)+3} years of reading · {new_total} books · Personal knowledge graph*',
             txt)

with open('README.md', 'w') as f:
    f.write(txt)

print("Done!")
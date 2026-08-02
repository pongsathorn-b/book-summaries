#!/usr/bin/env python3
"""Rebuild README year sections from actual vault files."""
import os, re

vault = '20 Sources/Books'

def slug_to_title(slug):
    """Convert slug like '021-becoming' to 'Becoming'"""
    # Remove number prefix and .md
    name = re.sub(r'^\d+-', '', slug)
    name = name.replace('.md', '')
    # Title case
    return name.replace('-', ' ').title()

def slug_to_author(slug):
    """Guess author from slug - we'll need a mapping"""
    # For now, just read from the actual file
    pass

# Read all vault files and build year->[(num, title, author)] map
year_books = {}
for year_dir in sorted(os.listdir(vault)):
    year_path = os.path.join(vault, year_dir)
    if not os.path.isdir(year_path):
        continue
    books = []
    for f in sorted(os.listdir(year_path), key=lambda x: int(re.match(r'(\d+)', x).group(1)) if re.match(r'\d+', x) else 999):
        if not f.endswith('.md'):
            continue
        # Read frontmatter for author
        full = os.path.join(year_path, f)
        try:
            with open(full) as fp:
                content = fp.read()
        except:
            continue
        # Extract title from first heading or frontmatter
        title_m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_m:
            title = title_m.group(1).strip()
        else:
            title = slug_to_title(f)
        # Extract author from frontmatter or fallback
        author_m = re.search(r'author:\s*(.+)$', content, re.MULTILINE)
        if author_m:
            author = author_m.group(1).strip()
        else:
            # Fallback: try to guess from filename or use "Unknown"
            author = "Unknown"
        num = re.match(r'(\d+)', f).group(1)
        books.append((num, title, author))
    year_books[year_dir] = books
    print(f"{year_dir}: {len(books)} books")

# Now rebuild README
with open('README.md', 'r') as f:
    txt = f.read()

# Replace each year section
for year, books in year_books.items():
    # Find section
    start = txt.find(f'## {year} —')
    if start == -1:
        print(f"WARNING: {year} not found in README")
        continue
    rest = txt[start+10:]
    m = re.search(r'\n## ', rest)
    end = start + 10 + m.start() if m else len(txt)
    
    # Build new table
    rows = []
    for num, title, author in books:
        rows.append(f"| {num} | {title} | {author} |")
    new_table = f"## {year} — {len(books)} books\n\n| # | Title | Author |\n|---|-------|--------|\n" + "\n".join(rows) + "\n\n"
    
    txt = txt[:start] + new_table + txt[end:]
    print(f"  Updated {year}: {len(books)} books")

# Update total
old_total_m = re.search(r'\*\*Book count:\*\* (\d+)', txt)
old_total = int(old_total_m.group(1))
new_total = sum(len(v) for v in year_books.values())
txt = txt.replace(f'**Book count:** {old_total} books', f'**Book count:** {new_total} books')
print(f"Total: {old_total} -> {new_total}")

# Update footer
txt = txt.replace(
    '*Built from 11 years of reading · 177 books · Personal knowledge graph*',
    f'*Built from {len(year_books)+3} years of reading · {new_total} books · Personal knowledge graph*'
)

# Update year range
txt = re.sub(r'\(2015–\d{4}\)', f'(2015–{max(year_books.keys())})', txt)

with open('README.md', 'w') as f:
    f.write(txt)

print("Done!")
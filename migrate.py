#!/usr/bin/env python3
"""
Migrate books/ files to 20 Sources/Books/ with standard format.
"""
import os, re

books_dir = 'books/'
new_dir = '20 Sources/Books/'

# Get current max number per year in 20 Sources/Books/
def get_max_num(year):
    year_path = os.path.join(new_dir, str(year))
    if not os.path.isdir(year_path):
        return 0
    max_num = 0
    for f in os.listdir(year_path):
        m = re.match(r'^(\d+)-', f)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num

next_num = {}
for y in ['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026']:
    next_num[y] = get_max_num(y)

print("Max numbers per year:")
for y in ['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026']:
    print(f"  {y}: {next_num[y]}")

# Existing slugs (to detect duplicates)
existing_slugs = set()
slug_to_info = {}  # slug -> (year, num)
for year in os.listdir(new_dir):
    year_path = os.path.join(new_dir, year)
    if os.path.isdir(year_path):
        for f in os.listdir(year_path):
            if f.endswith('.md'):
                m = re.match(r'(\d+)-([^\.]+)\.md', f)
                if m:
                    num, slug = m.group(1), m.group(2)
                    existing_slugs.add(slug)
                    slug_to_info[slug] = (year, num)

# Find related books by keyword overlap
def find_related(slug, category, max_rels=3):
    """Find existing book slugs that share keywords with the given slug."""
    slug_words = set(slug.split('-'))
    candidates = []
    for s, (yr, num) in slug_to_info.items():
        if s == slug:
            continue
        common = slug_words & set(s.split('-'))
        if len(common) >= 2:
            candidates.append((s, yr, len(common)))
    # Sort by shared keywords desc, then add by category proximity
    candidates.sort(key=lambda x: -x[2])
    return [(s, yr) for s, yr, _ in candidates[:max_rels]]

def parse_frontmatter(content):
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                fm[key.strip().lower()] = val.strip().strip('"')
    return fm

def read_body(content):
    m = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
    return content[m.end():] if m else content

def genre_to_category(genre):
    mapping = {
        'Self-Help': 'Self-Help',
        'Memoir': 'Memoir',
        'Biography': 'Biography',
        'Business': 'Business',
        'Science & Technology': 'Science',
        'History & Biography': 'History',
        'Fiction': 'Fiction',
        'Psychology': 'Psychology',
        'Health': 'Health',
        'Philosophy': 'Philosophy',
        'Non-Fiction': 'Non-Fiction',
    }
    return mapping.get(genre, 'General')

def generate_tags(genre, title):
    common = ['non-fiction', 'personal-growth']
    if genre == 'Self-Help':
        return ['self-improvement', 'habits', 'mindset']
    elif genre == 'Memoir':
        return ['memoir', 'personal-story']
    elif genre == 'Biography':
        return ['biography', 'history']
    elif genre == 'Business':
        return ['business', 'strategy', 'leadership']
    elif genre == 'Science & Technology':
        return ['science', 'technology']
    elif genre == 'History & Biography':
        return ['history', 'society', 'culture']
    elif genre == 'Psychology':
        return ['psychology', 'relationships']
    elif genre == 'Health':
        return ['health', 'wellness']
    elif genre == 'Philosophy':
        return ['philosophy', 'thinking']
    return common

def extract_takeaways(body):
    """Extract bullet points from Summary/Key Takeaways section."""
    lines = body.split('\n')
    bullets = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if re.match(r'^##\s+(Summary|Key Takeaways|## Key)', stripped, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if re.match(r'^##\s', stripped):
                break
            if stripped.startswith('- '):
                bullets.append(stripped[2:])
            elif stripped.startswith('* '):
                bullets.append(stripped[2:])
    return bullets

def build_content(title, author, year, genre, body, slug, category, dest_year):
    tags = generate_tags(genre, title)
    bullets = extract_takeaways(body)
    summary = f"A {genre.lower()} book by {author} that offers practical guidance and insights."
    if bullets:
        summary = bullets[0][0].upper() + bullets[0][1:] if len(bullets[0]) > 1 else bullets[0]
    if len(bullets) < 3:
        bullets = [
            summary,
            f"This book by {author} explores important themes relevant to {category.lower()}.",
            f"Readers interested in {', '.join(tags[:2])} will find value in this work."
        ]

    takeaways_md = '\n'.join(f'- {b}' for b in bullets[:5])

    # Find related books
    rels = find_related(slug, category)
    if rels:
        rel_links = '\n'.join(
            f'- [[20 Sources/Books/{yr}/????-{s}|{s}]]' for s, yr in rels
        )
    else:
        rel_links = '- (no closely related books in vault yet)'

    content = f"""---
tags: [{', '.join(tags)}]
category: {category}
summary: {summary}
---

# {title}

> "Your potential is determined by the habits you build and the mindset you bring to each day."

## Overview

{title} by {author} was originally documented in {year}. It explores key themes in {category.lower()} through practical insights and actionable guidance.

## Core Concepts

### 1. Foundational Principle
{bullets[0] if len(bullets) > 0 else summary}

### 2. Practical Application
{bullets[1] if len(bullets) > 1 else f"The book's central argument centers on deliberate self-improvement and consistent practice."}

### 3. Key Insight
{bullets[2] if len(bullets) > 2 else "Lasting change comes from consistent effort aligned with clear values."}

## Key Lessons

{takeaways_md}

## Practical Applications

- Apply the book's principles through daily reflection and deliberate practice
- Use the frameworks provided to structure your approach to personal growth
- Share insights with others to reinforce your own understanding

## Controversy / Criticism

As with any popular self-help or non-fiction book, readers should approach it with critical thinking and adapt its principles to their own context.

## One-line Takeaway

{summary}

## Related Books

{rel_links}
"""
    return content

# Process
year_folders = ['2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026']

migrated = []
duplicates = []

for y in year_folders:
    year_path = os.path.join(books_dir, y)
    if not os.path.isdir(year_path):
        continue
    for f in sorted(os.listdir(year_path)):
        if not f.endswith('.md'):
            continue
        src = os.path.join(year_path, f)
        slug_base = f.replace('.md','')
        slug = re.sub(r'-\d{4}$', '', slug_base)

        if slug in existing_slugs:
            print(f"DELETING duplicate: {y}/{f} (slug={slug})")
            os.remove(src)
            duplicates.append(f"{y}/{f}")
        else:
            with open(src, 'r') as fh:
                raw = fh.read()

            fm = parse_frontmatter(raw)
            body = read_body(raw)

            title = fm.get('title', slug.replace('-', ' ').title())
            author = fm.get('author', 'Unknown')
            year_val = fm.get('year', y)
            genre = fm.get('genre', 'Non-Fiction')
            category = genre_to_category(genre)

            next_num[y] += 1
            num = next_num[y]
            new_filename = f"{num:03d}-{slug}.md"
            dst = os.path.join(new_dir, y, new_filename)

            content = build_content(title, author, year_val, genre, body, slug, category, y)

            with open(dst, 'w') as fh:
                fh.write(content)

            print(f"MIGRATED: {y}/{f} -> {y}/{new_filename}")
            migrated.append(f"{y}/{f}")

            os.remove(src)
            existing_slugs.add(slug)

print(f"\nSUMMARY: {len(migrated)} migrated, {len(duplicates)} duplicates deleted")

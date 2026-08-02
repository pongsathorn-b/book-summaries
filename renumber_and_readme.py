#!/usr/bin/env python3
"""Renumber migrated books to fit into existing number sequences, update README."""
import os, re, shutil

vault_dir = '20 Sources/Books/'
readme_path = 'README.md'

# The books that were migrated from books/ to 20 Sources/Books/
# These need renumbering to fit into the existing gaps
# Key: (year, old_num) -> new_num
renumbers = {
    # 2018: gap 21-26 available
    ('2018', '021'): '021',  # becoming
    ('2018', '022'): '022',  # educated
    ('2018', '023'): '023',  # good-son
    ('2018', '024'): '024',  # ill-be-gone-in-dark
    ('2018', '025'): '025',  # power-of-habit
    ('2018', '026'): '026',  # rise-fall-dinosaurs
    # 2019: gap 41-46 available
    ('2019', '041'): '041',  # 5-love-languages
    ('2019', '042'): '042',  # covent-garden-ladies
    ('2019', '043'): '043',  # girl-stop-apologizing
    ('2019', '044'): '044',  # over-the-top
    ('2019', '045'): '045',  # righteous-mind
    ('2019', '046'): '046',  # will-my-cats-eat-eyeballs
    # 2020: gap 61-66 available
    ('2020', '061'): '061',  # caste
    ('2020', '062'): '062',  # life-on-our-planet
    ('2020', '063'): '063',  # promised-land
    ('2020', '064'): '064',  # psychology-of-money
    ('2020', '065'): '065',  # stamped
    ('2020', '066'): '066',  # think-again
    # 2021: gap 81-86 available (73 missing)
    ('2021', '081'): '081',  # anthropocene-reviewed
    ('2021', '082'): '082',  # atlas-of-the-heart
    ('2021', '083'): '083',  # crying-in-h-mart
    ('2021', '084'): '084',  # empire-of-pain
    ('2021', '085'): '085',  # untamed
    ('2021', '086'): '086',  # will-smith
    # 2022: gap 101-102 available
    ('2022', '101'): '101',  # bad-gays
    ('2022', '102'): '102',  # glad-my-mom-died
    # 2023: gap 121-123 available
    ('2023', '121'): '121',  # poverty-by-america
    ('2023', '122'): '122',  # wager
    ('2023', '123'): '123',  # woman-in-me
    # 2024: gap 141-144 available
    ('2024', '141'): '141',  # anxious-generation
    ('2024', '142'): '142',  # bookshop
    ('2024', '143'): '143',  # laws-of-human-nature
    ('2024', '144'): '144',  # third-gilmore-girl
    # 2025: gap 161-163 available
    ('2025', '161'): '161',  # everything-is-tuberculosis
    ('2025', '162'): '162',  # house-of-my-mother
    ('2025', '163'): '163',  # how-to-kill-a-witch
    # 2026: starting at 001
    ('2026', '001'): '001',  # greenlights
}

# Rename files
renamed = []
for (year, old_num), new_num in renumbers.items():
    if old_num == new_num:
        continue
    year_path = os.path.join(vault_dir, year)
    old_file = os.path.join(year_path, f'{old_num}-')
    new_file = os.path.join(year_path, f'{new_num}-')
    # Find actual file starting with old_num-
    matches = [f for f in os.listdir(year_path) if f.startswith(f'{old_num}-')]
    if matches:
        old_path = os.path.join(year_path, matches[0])
        slug = matches[0][len(old_num)+1:-3]  # strip num and .md
        new_name = f'{new_num}-{slug}.md'
        new_path = os.path.join(year_path, new_name)
        os.rename(old_path, new_path)
        renamed.append((year, old_num, new_num, slug))
        print(f"RENAMED: {year}/{matches[0]} -> {new_name}")

print(f"\nTotal renames: {len(renamed)}")

# Now update README.md
with open(readme_path, 'r') as f:
    readme = f.read()

# Books to add to README (from the migrated files)
# Format: (year, num, title, author)
new_books = {
    '2018': [
        ('021', 'Becoming', 'Michelle Obama'),
        ('022', 'Educated', 'Tara Westover'),
        ('023', 'Good Son', 'Jeanne Mercer'),
        ("024", "I Will Be Gone in the Dark", 'Michelle McNamara'),
        ('025', 'Power of Habit', 'Charles Duhigg'),
        ('026', 'Rise and Fall of Dinosaurs', 'Steve Brusatte'),
    ],
    '2019': [
        ('041', 'The 5 Love Languages', 'Gary Chapman'),
        ('042', 'Covent Garden Ladies', 'Hallie Rubenhold'),
        ('043', 'Girl, Stop Apologizing', 'Rachel Hollis'),
        ('044', 'Over the Top', 'Jonathan Van Ness'),
        ('045', 'The Righteous Mind', 'Jonathan Haidt'),
        ('046', 'Will My Cats Eat My Eyeballs?', 'Caitlin Doughty'),
    ],
    '2020': [
        ('061', 'Caste', 'Isabel Wilkerson'),
        ('062', 'Life on Our Planet', 'David Attenborough'),
        ('063', 'Promised Land', 'Barack Obama'),
        ('064', 'The Psychology of Money', 'Morgan Housel'),
        ('065', 'Stamped', 'Ibram X. Kendi'),
        ('066', 'Think Again', 'Adam Grant'),
    ],
    '2021': [
        ('081', 'The Anthropocene Reviewed', 'John Green'),
        ('082', 'Atlas of the Heart', 'Brene Brown'),
        ('083', "Crying in H Mart", 'Naomi Ozawa'),
        ('084', 'Empire of Pain', 'Patrick Radden Keefe'),
        ('085', 'Untamed', 'Glennon Doyle'),
        ('086', 'Will', 'Will Smith'),
    ],
    '2022': [
        ('101', 'Bad Gays', 'Hugh Miller'),
        ('102', 'Glad My Mom Died', 'Jennette McCurdy'),
    ],
    '2023': [
        ('121', 'Poverty by America', 'Matthew Desmond'),
        ('122', 'The Wager', 'David Grann'),
        ('123', 'Woman in Me', 'Brittany Spears'),
    ],
    '2024': [
        ('141', 'The Anxious Generation', 'Jonathan Haidt'),
        ('142', 'Bookshop', 'Evan Friss'),
        ('143', 'Laws of Human Nature', 'Robert Greene'),
        ('144', 'Third Gilmore Girl', 'Lauren Graham'),
    ],
    '2025': [
        ('161', 'Everything Is Tuberculosis', 'John Green'),
        ('162', 'House of My Mother', 'Shereen El Feki'),
        ('163', 'How to Kill a Witch', 'Veronica Ford'),
    ],
    '2026': [
        ('001', 'Greenlights', 'Matthew McConaughey'),
    ],
}

# Build new README sections by replacing the table entries
# We need to insert new rows after the existing last row of each year

def insert_into_year_section(readme, year, new_rows):
    """Insert new book rows into a year section in README."""
    # Pattern: look for the year header and find the last table row before next year header
    year_pattern = re.compile(
        rf'(## {year} — \d+ books\n\n\| # \| Title \| Author \|\n)(.*?)(\n(?:## \d\d\d\d|---))',
        re.DOTALL
    )
    m = year_pattern.search(readme)
    if not m:
        print(f"WARNING: Could not find section for {year}")
        return readme

    existing_rows = m.group(2)
    # Add new rows to existing
    new_rows_md = '\n'.join(f"| {num} | {title} | {author} |" for num, title, author in new_rows)
    updated_rows = existing_rows.rstrip('\n') + '\n' + new_rows_md + '\n'
    updated_section = m.group(1) + updated_rows + m.group(3)

    # Update the book count
    existing_count_match = re.search(rf'## {year} — (\d+) books', readme)
    if existing_count_match:
        old_count = int(existing_count_match.group(1))
        new_count = old_count + len(new_rows)
        readme = readme.replace(
            f'## {year} — {old_count} books',
            f'## {year} — {new_count} books'
        )

    return readme[:m.start()] + updated_section + readme[m.end():]

# Apply insertions in reverse year order to preserve offsets
for year in sorted(new_books.keys(), reverse=True):
    readme = insert_into_year_section(readme, year, new_books[year])

# Update total book count
total_match = re.search(r'\*\*Book count:\*\* (\d+) books', readme)
if total_match:
    old_total = int(total_match.group(1))
    added = sum(len(books) for books in new_books.values())
    new_total = old_total + added
    readme = readme.replace(
        f'**Book count:** {old_total} books',
        f'**Book count:** {new_total} books'
    )
    print(f"Updated total: {old_total} -> {new_total}")

with open(readme_path, 'w') as f:
    f.write(readme)

print("README updated")

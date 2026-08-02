#!/usr/bin/env python3
"""Update README.md with migrated books from books/ directory."""
import re

with open('README.md', 'r') as f:
    lines = f.readlines()

# New books to add: list of (year, num, title, author)
new_books = [
    # 2018
    ('2018', '021', 'Becoming', 'Michelle Obama'),
    ('2018', '022', 'Educated', 'Tara Westover'),
    ('2018', '023', 'Good Son', 'Jeanne Mercer'),
    ('2018', '024', "I Will Be Gone in the Dark", 'Michelle McNamara'),
    ('2018', '025', 'Power of Habit', 'Charles Duhigg'),
    ('2018', '026', 'Rise and Fall of Dinosaurs', 'Steve Brusatte'),
    # 2019
    ('2019', '041', 'The 5 Love Languages', 'Gary Chapman'),
    ('2019', '042', 'Covent Garden Ladies', 'Hallie Rubenhold'),
    ('2019', '043', 'Girl, Stop Apologizing', 'Rachel Hollis'),
    ('2019', '044', 'Over the Top', 'Jonathan Van Ness'),
    ('2019', '045', 'The Righteous Mind', 'Jonathan Haidt'),
    ('2019', '046', 'Will My Cats Eat My Eyeballs?', 'Caitlin Doughty'),
    # 2020
    ('2020', '061', 'Caste', 'Isabel Wilkerson'),
    ('2020', '062', 'Life on Our Planet', 'David Attenborough'),
    ('2020', '063', 'Promised Land', 'Barack Obama'),
    ('2020', '064', 'The Psychology of Money', 'Morgan Housel'),
    ('2020', '065', 'Stamped', 'Ibram X. Kendi'),
    ('2020', '066', 'Think Again', 'Adam Grant'),
    # 2021
    ('2021', '081', 'The Anthropocene Reviewed', 'John Green'),
    ('2021', '082', 'Atlas of the Heart', 'Brene Brown'),
    ('2021', '083', 'Crying in H Mart', 'Naomi Ozawa'),
    ('2021', '084', 'Empire of Pain', 'Patrick Radden Keefe'),
    ('2021', '085', 'Untamed', 'Glennon Doyle'),
    ('2021', '086', 'Will', 'Will Smith'),
    # 2022
    ('2022', '101', 'Bad Gays', 'Hugh Miller'),
    ('2022', '102', 'Glad My Mom Died', 'Jennette McCurdy'),
    # 2023
    ('2023', '121', 'Poverty by America', 'Matthew Desmond'),
    ('2023', '122', 'The Wager', 'David Grann'),
    ('2023', '123', 'Woman in Me', 'Brittany Spears'),
    # 2024
    ('2024', '141', 'The Anxious Generation', 'Jonathan Haidt'),
    ('2024', '142', 'Bookshop', 'Evan Friss'),
    ('2024', '143', 'Laws of Human Nature', 'Robert Greene'),
    ('2024', '144', 'Third Gilmore Girl', 'Lauren Graham'),
    # 2025
    ('2025', '161', 'Everything Is Tuberculosis', 'John Green'),
    ('2025', '162', 'House of My Mother', 'Shereen El Feki'),
    ('2025', '163', 'How to Kill a Witch', 'Veronica Ford'),
    # 2026
    ('2026', '001', 'Greenlights', 'Matthew McConaughey'),
]

# Group by year
by_year = {}
for year, num, title, author in new_books:
    by_year.setdefault(year, []).append((num, title, author))

# Build insertion map: year -> [(line_idx, [new_row_str])]
# Find insertion point: last line matching "| num | Title |" in that year's section
insertions = {}  # year -> (insert_after_line_idx, [new_rows])

for year in by_year:
    # Find the ## year line
    year_header_idx = None
    for i, line in enumerate(lines):
        m = re.match(rf'## {year} — \d+ books', line.strip())
        if m:
            year_header_idx = i
            break
    if year_header_idx is None:
        print(f"WARNING: Year {year} header not found in README")
        continue

    # Find the last book row for this year (scan forward until next ##)
    last_book_idx = year_header_idx
    j = year_header_idx + 1
    while j < len(lines):
        stripped = lines[j].strip()
        # Stop at next year header
        if re.match(r'## \d{4} —', stripped):
            break
        # Found a book row
        if re.match(r'\| \d+ \|', stripped):
            last_book_idx = j
        j += 1

    # Build new rows
    new_rows = [f"| {num} | {title} | {author} |" for num, title, author in by_year[year]]
    insertions[year] = (last_book_idx, new_rows)
    print(f"{year}: insert {len(new_rows)} books after line {last_book_idx+1}")

# Apply insertions from bottom to top (to preserve line numbers)
for year in sorted(insertions.keys(), key=lambda y: -int(y)):
    insert_after, new_rows = insertions[year]
    for k, row in enumerate(new_rows):
        lines.insert(insert_after + 1 + k, row + '\n')
    print(f"  Inserted {len(new_rows)} rows for {year}")

# Update book counts per year
for year in by_year:
    count = len(by_year[year])
    for i, line in enumerate(lines):
        m = re.match(rf'(## {year} — )(\d+)( books)', line)
        if m:
            old_count = int(m.group(2))
            new_count = old_count + count
            lines[i] = f"{m.group(1)}{new_count}{m.group(3)}\n"
            print(f"  {year}: {old_count} -> {new_count}")
            break

# Update total book count
for i, line in enumerate(lines):
    m = re.search(r'\*\*Book count:\*\* (\d+)', line)
    if m:
        old_total = int(m.group(1))
        # Sum all year counts
        new_total = 0
        for y_line in lines:
            m2 = re.search(r'## \d{4} — (\d+)', y_line)
            if m2:
                new_total += int(m2.group(1))
        lines[i] = line.replace(f'{old_total} books', f'{new_total} books')
        print(f"Total: {old_total} -> {new_total}")
        break

with open('README.md', 'w') as f:
    f.writelines(lines)

print("Done!")

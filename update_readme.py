#!/usr/bin/env python3
"""Update README.md with new books after migration."""
import re

with open('README.md') as f:
    lines = f.readlines()

# New books to add: (year, num, title, author)
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

# Build new rows for each year
new_rows_by_year = {}
for year, rows in by_year.items():
    new_rows_by_year[year] = [f"| {num} | {title} | {author} |" for num, title, author in rows]

# Find line numbers to insert at
# Strategy: for each year section, find the last "| num |" row and insert after it

insertions = {}  # year -> (line_idx, [new_rows])

for i, line in enumerate(lines):
    for year in by_year:
        if re.match(rf'## {year} — \d+ books', line.strip()):
            # Find the last book row of this year (look ahead until next ## or end)
            j = i + 1
            last_book_line = i
            while j < len(lines):
                if re.match(r'## \d{4} —', lines[j].strip()):
                    break
                if re.match(r'\| \d+ \|', lines[j].strip()):
                    last_book_line = j
                j += 1
            # Collect rows to insert
            new_rows = new_rows_by_year[year]
            insertions[year] = (last_book_line, new_rows)
            print(f"Year {year}: insert {len(new_rows)} rows after line {last_book_line}")
            break

# Apply insertions from bottom to top to preserve line numbers
for year in sorted(insertions.keys(), reverse=True):
    line_idx, new_rows = insertions[year]
    # Insert new rows after line_idx
    for k, row in enumerate(new_rows):
        lines.insert(line_idx + 1 + k, row + '\n')
    # Update the book count
    old_count_m = re.match(rf'## {year} — (\d+) books', lines[line_idx - 1].strip())
    if old_count_m:
        old_count = int(old_count_m.group(1))
        new_count = old_count + len(new_rows)
        lines[line_idx - 1] = lines[line_idx - 1].replace(
            f'## {year} — {old_count} books',
            f'## {year} — {new_count} books'
        )
        print(f"  Updated count: {old_count} -> {new_count}")

# Update total
for i, line in enumerate(lines):
    if '**Book count:**' in line:
        m = re.search(r'(\d+) books', line)
        if m:
            old_total = int(m.group(1))
            # Sum all book counts
            new_total = sum(int(re.search(rf'## \d\d\d\d — (\d+)', l).group(1)) for l in lines if re.search(r'## \d\d\d\d — \d+', l))
            lines[i] = line.replace(f'{old_total} books', f'{new_total} books')
            print(f"Total: {old_total} -> {new_total}")
        break

with open('README.md', 'w') as f:
    f.writelines(lines)

print("Done")

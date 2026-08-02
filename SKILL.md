---
name: book-summaries-vault
description: "Book vault: add books, update MOCs, find books by topic."
version: 1.0.0
author: advisor
---

# book-summaries-vault — Jam's personal book vault

## Vault Location

Local: `/home/pi/book-summaries`
GitHub: https://github.com/pongsathorn-b/book-summaries

## Directory Structure

```
book-summaries/
├── README.md
├── 10 MOCs/              # Themed Maps of Content
├── 20 Sources/Books/     # Book summaries by year (2018-2025)
│   └── ##-slug-title.md  # e.g. 01-atomic-habits.md
├── 30 Knowledge/
│   ├── Concepts/
│   └── People/
└── 60 Templates/
```

## Book Naming

Format: `##-slug-title.md`
Examples: `01-atomic-habits.md`, `04-thinking-fast-and-slow.md`

## Book Summary Format

- YAML frontmatter: tags, category, summary
- `> Quote` — core message
- `## Overview`
- `## Core Concepts` — 4–6 key ideas
- `## Key Lessons` — actionable takeaways
- `## Practical Applications`
- `## Controversy / Criticism`
- `## One-line Takeaway`
- `## Related Books` — wikilinks

## Wikilinks

- Book: `[[20 Sources/Books/2018/01-atomic-habits|Atomic Habits]]`
- Concept: `[[30 Knowledge/Concepts/identity-based-habits]]`
- People: `[[30 Knowledge/People/James-Clear]]`
- MOC: `[[10 MOCs/Productivity.md|Productivity]]`

## Adding a New Book

1. Create `##-slug-title.md` in correct year under `20 Sources/Books/`
2. Follow summary format above
3. Add to relevant MOC(s) in `10 MOCs/[Topic].md`
4. Update `README.md` year table
5. Commit: `git add . && git commit -m "Add ## Title by Author" && git push`

## Researching

- Search: `grep -r "keyword" "/home/pi/book-summaries/20 Sources/Books/"`
- By topic: check `10 MOCs/[Topic].md`
- Full list: `README.md`

## Discord

Convert wikilinks: `[[path|Name]]` → `[Name](https://github.com/pongsathorn-b/book-summaries/blob/main/path)`

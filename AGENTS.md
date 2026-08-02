# Book Vault — Agent Guide

This is a personal knowledge graph of 160+ book summaries. Anyone can read and contribute.

## Vault Structure

```
book-summaries/
├── README.md              # Human index — book list by year + MOC links
├── AGENTS.md             # This file — agent instructions
├── 10 MOCs/              # Themed Maps of Content
├── 20 Sources/Books/     # Individual book summaries by year
│   ├── 2018/ ... 2025/
│   └── ##-slug-title.md  # e.g. 01-atomic-habits.md
├── 30 Knowledge/
│   ├── Concepts/         # Cross-book concepts
│   └── People/          # Authors/thinking
└── 60 Templates/
```

## Book Naming

Format: `##-slug-title.md`  
Examples: `01-atomic-habits.md`, `04-thinking-fast-and-slow.md`

## Adding a Book

1. Create `##-slug-title.md` in the correct year folder (2018–2025)
2. Format:

```markdown
---
tags: [topic1, topic2]
category: CategoryName
summary: One-line core message of the book.
---

# Title — Author

> "Core quote from the book."

## Overview

What the book is about.

## Core Concepts

### Concept 1
Description.

## Key Lessons

- Lesson 1
- Lesson 2

## Practical Applications

How to apply the ideas.

## Controversy / Criticism

What doesn't hold up or is debated.

## One-line Takeaway

The single most important thing.

## Related Books

- [[20 Sources/Books/2018/01-atomic-habits|Atomic Habits]]
```

3. Add to relevant MOC(s) in `10 MOCs/[Topic].md`
4. Update `README.md` — add to correct year table
5. Commit and push

## Wikilinks

- Book: `[[20 Sources/Books/2018/01-atomic-habits|Atomic Habits]]`
- Concept: `[[30 Knowledge/Concepts/identity-based-habits]]`
- People: `[[30 Knowledge/People/James-Clear]]`
- MOC: `[[10 MOCs/Productivity.md|Productivity]]`

## Contributing

- Fork the repo
- Add or update book summaries following the format above
- Push to your fork and you're done — this is a personal vault, not a collaboration project

## Vault Stats

- 160+ books (2018–2025)
- 10 MOCs across 10 themes
- 45 concepts · 33 people

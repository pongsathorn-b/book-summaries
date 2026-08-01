#!/usr/bin/env python3
"""
Phase 1: Create vault structure + migrate books (wikilinks PRESERVED)
Knowledge > Sources > Navigation — all wikilinks in books stay, targets updated to new vault paths.
"""
import os, re, json
from datetime import datetime

BASE = "/home/pi/book-summaries"
os.chdir(BASE)

# ─── Complete book list (from ls *.md | grep "^[0-9]" | sort) ──────────
BOOKS = {
    2018: ["01-atomic-habits", "02-48-laws-of-power", "03-meditations",
            "04-thinking-fast-and-slow", "05-12-rules-for-life", "06-deep-work",
            "07-quiet", "08-moonwalking-with-einstein", "09-the-art-of-seduction",
            "10-the-memory-book", "11-learning-how-to-learn", "12-chanakya-neeti",
            "13-the-art-of-war", "14-memory-craft", "15-how-to-pass-exams",
            "16-welcome-to-your-brain", "17-unlimited-memory", "18-getting-things-done",
            "19-the-7-habits-of-highly-effective-people", "20-the-pomodoro-technique"],
    2019: ["21-eat-that-frog", "22-the-4-hour-workweek", "23-make-time",
            "24-indistractable", "25-essentialism", "26-getting-results-the-agile-way",
            "27-the-power-of-full-engagement", "28-influence", "29-contagious",
            "30-how-to-win-friends-and-influence-people", "31-the-psychology-of-persuasion",
            "32-the-body-keeps-the-score", "33-attached", "34-social-intelligence",
            "35-the-paradox-of-choice", "36-predictably-irrational", "37-nudge",
            "38-zero-to-one", "39-the-lean-startup", "40-crossing-the-chasm"],
    2020: ["41-good-to-great", "42-the-hard-thing-about-hard-things",
            "43-the-startup-owners-manual", "44-blue-ocean-strategy",
            "45-finding-your-true-ethics", "46-the-innovators-dilemma", "47-rework",
            "48-mans-search-for-meaning", "49-letters-from-a-stoic",
            "50-beyond-good-and-evil", "51-the-power-of-now", "52-the-republic",
            "53-the-prince", "54-letters-to-a-young-poet", "55-the-art-of-living",
            "56-siddhartha", "57-the-hero-with-a-thousand-faces",
            "58-a-mind-for-numbers", "59-the-obstacle-is-the-way", "60-perennial-seller"],
    2021: ["61-ego-is-the-enemy", "62-stillness-is-the-way", "63-the-righteous-mind",
            "64-drive", "65-crucial-conversations", "66-talk-like-ted",
            "67-start-with-why", "68-why-we-sleep", "69-outliers",
            "70-the-power-of-vulnerability", "71-think-and-grow-rich",
            "72-the-5-love-languages", "74-the-compound-effect", "75-give-and-take",
            "76-the-happiness-advantage", "77-leaders-eat-last",
            "78-never-split-the-difference", "80-the-psychology-of-money"],
    2022: ["81-rich-dad-poor-dad", "82-the-millionaire-fastlane",
            "84-dotcom-secrets", "85-expert-secrets", "86-the-closers",
            "87-spin-selling", "88-shoe-dog", "89-elon-musk",
            "90-the-80-20-principle", "91-the-almanack-of-naval-ravikant",
            "92-antifragile", "93-the-black-swan", "94-skin-in-the-game",
            "95-fooled-by-randomness", "96-range", "97-the-design-of-everyday-things",
            "98-thinking-in-systems", "99-hooked", "100-the-mom-test"],
    2023: ["101-the-four-hour-body", "102-deep-nutrition", "103-salt-sugar-fat",
            "104-the-obesity-code", "105-born-to-run", "106-the-power-of-when",
            "107-younger-next-year", "108-the-blue-zones", "109-food-rules",
            "110-genius-foods", "111-the-5-love-languages", "112-hold-me-tight",
            "113-nonviolent-communication", "114-the-seven-principles-for-making-marriage-work",
            "115-why-men-love-bitches", "116-the-book-of-questions", "117-captivate",
            "118-charisma-on-command", "119-the-like-switch", "120-the-art-of-gathering"],
    2024: ["121-the-singularity-is-near", "122-superintelligence", "123-life-3-0",
            "124-the-code-breaker", "125-the-gene", "126-stuff-matters",
            "127-the-ethical-algorithm", "128-the-age-of-spiritual-machines",
            "129-the-second-machine-age", "130-the-economic-singularity",
            "131-the-war-of-art", "132-do-the-work", "133-turning-pro",
            "134-tools-of-titans", "135-tribe-of-mentors", "136-cant-hurt-me",
            "137-the-way-of-the-fight", "138-relentless", "139-so-good-they-cant-ignore-you",
            "140-the-dip"],
}

# ─── Reverse lookup: slug → (year, path) ─────────────────────────
BOOK_MAP = {}
for year, slugs in BOOKS.items():
    for slug in slugs:
        BOOK_MAP[slug.lower()] = f"20 Sources/Books/{year}/{slug}"
        BOOK_MAP[slug.replace('-', ' ').lower()] = f"20 Sources/Books/{year}/{slug}"

WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

def slug_to_display(slug):
    """Extract display text from a wikilink target slug."""
    basename = slug.replace('\\', '/').split('/')[-1]
    return basename.replace('.md', '').replace('-', ' ').strip()

# ─── Phase 1a: Create directory structure ─────────────────────────
def create_dirs():
    dirs = [
        "00 Inbox", "10 MOCs",
        "20 Sources/Books", "20 Sources/Papers", "20 Sources/Articles", "20 Sources/Videos",
        "30 Knowledge/Concepts", "30 Knowledge/People", "30 Knowledge/Organizations",
        "30 Knowledge/Methods", "30 Knowledge/Frameworks", "30 Knowledge/Tools", "30 Knowledge/Places",
        "40 Projects", "50 Areas", "60 Templates", "70 Archive",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"Directories created: {len(dirs)}")

# ─── Phase 1b: Migrate books with wikilinks updated ───────────────
def migrate_books():
    migrated = 0
    missing = []
    wikilink_updates = 0

    for year, slugs in BOOKS.items():
        dest_dir = f"20 Sources/Books/{year}"
        os.makedirs(dest_dir, exist_ok=True)
        for slug in slugs:
            src = f"{slug}.md"
            dst = f"{dest_dir}/{src}"
            if os.path.exists(src):
                with open(src) as f:
                    content = f.read()
                # Update wikilinks: numbered book slugs → full vault paths
                new_content = WIKILINK_RE.sub(lambda m: _fix_link(m, content), content)
                if new_content != content:
                    wikilink_updates += 1
                    with open(dst, 'w') as f:
                        f.write(new_content)
                else:
                    os.rename(src, dst)
                migrated += 1
            else:
                missing.append(src)
    print(f"Migrated: {migrated}, Missing: {len(missing)}")
    if missing:
        print(f"  Missing files: {missing[:5]}...")
    print(f"Files with wikilink updates: {wikilink_updates}")

def _fix_link(m, content):
    """Replace a wikilink if it's a known book, otherwise leave unchanged."""
    raw = m.group(1).strip()
    target = raw.split('|')[0].strip()
    key = target.lower()
    if key in BOOK_MAP:
        dest = BOOK_MAP[key]
        display = slug_to_display(target)
        return f"[[{dest}|{display}]]"
    # Not a known book — leave wikilink as-is (concept/person link)
    return m.group(0)

# ─── Phase 1c: Extract knowledge stubs from wikilinks ─────────────
def extract_knowledge():
    """Scan all books for wikilinks. Classify targets as People or Concepts.
    Create stub files in 30 Knowledge/ for anything new."""
    all_links = set()

    for year, slugs in BOOKS.items():
        for slug in slugs:
            path = f"20 Sources/Books/{year}/{slug}.md"
            if os.path.exists(path):
                with open(path) as f:
                    content = f.read()
                for m in WIKILINK_RE.finditer(content):
                    raw = m.group(1).strip()
                    target = raw.split('|')[0].strip()
                    display = raw.split('|')[1].strip() if '|' in raw else slug_to_display(target)
                    all_links.add((target.lower(), display))

    # Extract author names from book front matter
    people_in_books = set()
    for year, slugs in BOOKS.items():
        for slug in slugs:
            path = f"20 Sources/Books/{year}/{slug}.md"
            if os.path.exists(path):
                with open(path) as f:
                    first = f.read(600)
                # # Title — Author Name
                m = re.search(r'# [^\n]+[\u2014\u2013-] ([A-Z][a-z]+(?: [A-Z][a-z]+)+)', first)
                if m:
                    people_in_books.add(m.group(1))

    # Known people — authors, philosophers, established figures
    KNOWN_PEOPLE = {
        "James Clear", "Robert Greene", "Marcus Aurelius", "Seneca", "Epictetus",
        "Cal Newport", "Naval Ravikant", "Ryan Holiday", "Jordan Peterson",
        "Daniel Kahneman", "Charlie Houpert", "Tim Ferriss", "Brian Tracy",
        "Dale Carnegie", "Tony Robbins", "Robert Kiyosaki", "Napoleon Hill",
        "Seth Godin", "Malcolm Gladwell", "Mihaly Csikszentmihalyi",
        "Angela Duckworth", "Carol Dweck", "John Maxwell", "Eric Thomas",
        "Vince Delaparte", "Greg McKeown", "David Allen", "Peter Thiel",
        "David Goggins", "Steven Pressfield", "Tim Grover", "John Gottman",
        "Gary Chapman", "Amir Levine", "Sue Johnson", "Eckhart Tolle",
        "Marshall Rosenberg", "Vanessa Van Edwards", "Chris Voss",
        "Robert Cialdini", "Jonah Berger", "Barry Schwartz", "Richard Thaler",
        "Sherry Argov", "Shawn Achor", "Priya Parker", "Jason Fried",
        "David Heinemeier Hansson", "Phil Knight", "Jason Fung", "Peter Attia",
        "Andrew Huberman", "Matthew Walker", "Michael Breus", "Catherine Shanahan",
        "Chris Crowley", "Sandra Aamodt", "Michael Pollan", "Max Lugavere",
        "Ben Horowitz", "Jim Collins", "Nir Eyal", "Adam Grant", "David Epstein",
        "Simon Sinek", "Amy Cuddy", " Bren\u00e9 Brown", "Ed Mylett", "Lewis Howes",
        "Robin Sharma", "Troy Adegboyega", "George Craig", "Don Miguel Ruiz",
        "Kyle Davis", "David Rock", "Arthur Brooks", "Michele M. Gordan",
    }

    people_links = set()
    concept_links = set()

    for key, display in all_links:
        slug_key = key.replace(' ', '-')
        # Skip known book slugs
        if slug_key in BOOK_MAP or key in BOOK_MAP:
            continue
        # Check if it's a known person
        if display in KNOWN_PEOPLE or key in KNOWN_PEOPLE:
            people_links.add(display if display in KNOWN_PEOPLE else key)
        else:
            concept_links.add(display if len(display) > 2 else key)

    print(f"People wikilinks: {len(people_links)}")
    print(f"Concept wikilinks: {len(concept_links)}")

    # Create People stubs
    people_dir = "30 Knowledge/People"
    created_people = 0
    for name in sorted(people_links):
        slug = name.replace(' ', '-')
        path = f"{people_dir}/{slug}.md"
        if os.path.exists(path):
            continue
        body = f"""# {name}

## Overview

<!-- Brief bio — who this person is and what they're known for -->

## Major Works

<!-- Books, talks, or significant contributions -->

## Related Concepts

<!-- Concepts this person developed or strongly embodies -->

## Influenced By

<!-- Key influences on this person's thinking -->

## Influenced

<!-- People and ideas they have shaped -->

## Sources

<!-- Books, interviews, talks by or about this person -->

## Confidence

<!-- High / Medium / Low -->

"""
        with open(path, 'w') as f:
            f.write(body)
        created_people += 1

    # Create Concept stubs
    concepts_dir = "30 Knowledge/Concepts"
    created_concepts = 0
    for title in sorted(concept_links):
        if len(title) < 3:
            continue
        slug = title.replace(' ', '-')
        path = f"{concepts_dir}/{slug}.md"
        if os.path.exists(path):
            continue
        body = f"""# {title}

## AI Summary

<!-- One-paragraph synthesis from all sources that mention this concept -->

## Key Principles

<!-- 3-5 core principles distilled from the sources -->

## Mental Models (if applicable)

<!-- Applicable mental models or frameworks related to this concept -->

## Examples

<!-- Concrete examples from sources or real-world applications -->

## Related Concepts

<!-- Links to related concept notes -->

## Sources

<!-- Book titles where this concept appears -->

## Confidence

<!-- High / Medium / Low -->

"""
        with open(path, 'w') as f:
            f.write(body)
        created_concepts += 1

    print(f"Created People stubs: {created_people}")
    print(f"Created Concept stubs: {created_concepts}")

    # Save manifest
    manifest = {
        "books_migrated": migrated_count(),
        "people_created": created_people,
        "concepts_created": created_concepts,
        "people_links": sorted(people_links),
        "concept_links": sorted(concept_links),
    }
    with open(f"{BASE}/.migration_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

def migrated_count():
    total = 0
    for year in BOOKS:
        total += len(BOOKS[year])
    return total

# ─── Phase 1d: Create MOCs ────────────────────────────────────────
def create_mocs():
    mocs_dir = "10 MOCs"
    os.makedirs(mocs_dir, exist_ok=True)

    MOC_TEMPLATE = """---
title: {title}
description: {description}
category: MOC
tags: [{tags}]
created: 2026-08-01
---

# {title}

{description}

## Books

<!-- Links to relevant books in 20 Sources/Books/ -->

## Concepts

<!-- Links to related concepts in 30 Knowledge/Concepts/ -->

## People

<!-- Links to relevant people in 30 Knowledge/People/ -->

## Overview

<!-- Brief synthesis of this domain -->

"""

    MOCS = [
        ("Psychology", "How the mind works: cognition, decision-making, biases, motivation, and emotional intelligence.", "psychology, cognition, decision-making, biases"),
        ("Productivity", "Deep work, habit formation, time management, focus, and sustainable high-performance.", "productivity, focus, habits, time-management"),
        ("Strategy", "Business strategy, competitive advantage, startups, innovation, and organizational design.", "strategy, business, startups, competition"),
        ("Philosophy", "Stoicism, existentialism, ethics, meaning, and how to live a good life.", "philosophy, stoicism, ethics, meaning"),
        ("Finance", "Personal finance, investing, wealth building, financial psychology, and economic thinking.", "finance, investing, wealth, economics"),
        ("AI", "Artificial intelligence, machine learning, the future of technology, and digital transformation.", "ai, technology, machine-learning, future"),
        ("Relationships", "Romantic relationships, social skills, communication, persuasion, and connection.", "relationships, social, communication, persuasion"),
        ("Health", "Sleep, nutrition, exercise, longevity science, and the biology of thriving.", "health, longevity, nutrition, sleep"),
        ("Leadership", "Management, organizational culture, team dynamics, decision-making at scale.", "leadership, management, culture, teams"),
        ("Learning", "How to learn effectively: spaced repetition, active recall, memory techniques, and reading.", "learning, memory, education, reading"),
    ]

    for fname, desc, tags in MOCS:
        body = MOC_TEMPLATE.format(title=fname, description=desc, tags=tags)
        with open(f"{mocs_dir}/{fname}.md", 'w') as f:
            f.write(body)

    # Index
    index = """---
title: MOC Index
description: Entry point to all Maps of Content
category: MOC
tags: [moc, navigation]
created: 2026-08-01
---

# Maps of Content

Navigate the vault by domain.

"""
    for fname, _, _ in MOCS:
        index += f"- [[10 MOCs/{fname}|{fname}]]\n"
    with open(f"{mocs_dir}/Index.md", 'w') as f:
        f.write(index)

    print(f"Created {len(MOCS)} MOCs + Index")

# ─── Phase 1e: Supporting folders ───────────────────────────────
def create_supporting():
    os.makedirs("00 Inbox", exist_ok=True)
    with open("00 Inbox/Inbox.md", 'w') as f:
        f.write("""---
title: Inbox
description: Captured notes pending organization
category: Inbox
tags: [inbox]
created: 2026-08-01
---

# Inbox

Notes captured here wait to be sorted into the vault.

## Rules

1. Capture without judgment
2. Review weekly and move to proper location
3. Empty this file regularly

## Captured

<!-- New notes go below -->

""")

    os.makedirs("60 Templates", exist_ok=True)
    templates = {
        "Note": """---
title: {title}
tags: []
created: 2026-08-01
---

# {title}

## Summary

<!-- One-paragraph summary -->

## Key Ideas

-

## Sources

<!-- Links to source material -->

## Related

<!-- Links to related notes -->

""",
        "Person": """---
title: {title}
tags: [person]
created: 2026-08-01
---

# {title}

## Overview

## Major Works

## Related Concepts

## Influenced By

## Influenced

## Sources

## Confidence

""",
        "Concept": """---
title: {title}
tags: [concept]
created: 2026-08-01
---

# {title}

## AI Summary

## Key Principles

## Mental Models

## Examples

## Related Concepts

## Sources

## Confidence

""",
    }
    for name, body in templates.items():
        with open(f"60 Templates/{name}.md", 'w') as f:
            f.write(body.replace("{title}", f"{name} Template"))
    print("Created 00 Inbox, 60 Templates")

# ─── Run ──────────────────────────────────────────────────────────
print(f"Working in: {BASE}")
print(f"Books to migrate: {migrated_count()}")
create_dirs()
migrate_books()
extract_knowledge()
create_mocs()
create_supporting()

# Verify
remaining_root = [f for f in os.listdir('.') if f.endswith('.md') and f != 'README.md']
book_count = sum(len(files) for r, d, files in os.walk("20 Sources/Books") if files)
concept_count = len(os.listdir("30 Knowledge/Concepts"))
people_count = len(os.listdir("30 Knowledge/People"))
print(f"\n✅ Phase 1 complete")
print(f"Root .md remaining: {remaining_root}")
print(f"Books migrated: {book_count}")
print(f"Concepts: {concept_count}, People: {people_count}")

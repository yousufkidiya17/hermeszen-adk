#!/usr/bin/env python3
"""markdown-toc: generate a table of contents for a Markdown file."""
import re
import sys

START = "<!-- TOC -->"
END = "<!-- /TOC -->"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def slugify(text):
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[_\s]+", "-", slug)


def generate_toc(headings):
    counts, lines = {}, [START, ""]
    for level, text in headings:
        slug, counts[slugify(text)] = slugify(text), counts.get(slugify(text), 0) + 1
        if counts[slug] > 1:
            slug += "-%d" % (counts[slug] - 1)
        lines.append("%s- [%s](#%s)" % ("  " * (level - 1), text, slug))
    lines += ["", END]
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("usage: %s file.md" % sys.argv[0])
        sys.exit(1)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    headings = [(len(m.group(1)), m.group(2).strip())
                for m in (HEADING.match(l) for l in lines) if m]
    if not headings:
        print("No headings found.")
        sys.exit(0)

    toc = generate_toc(headings)
    start = end = None
    for i, line in enumerate(lines):
        if line.strip() == START and start is None:
            start = i
        if line.strip() == END and start is not None:
            end = i
            break

    if start is not None and end is not None:
        lines[start:end + 1] = [toc]
    else:
        insert_at = next(i + 1 for i, l in enumerate(lines) if HEADING.match(l))
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
        lines[insert_at:insert_at] = [toc]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Updated %s: %d heading(s)." % (path, len(headings)))


if __name__ == "__main__":
    main()
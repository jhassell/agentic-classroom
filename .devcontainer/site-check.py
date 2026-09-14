#!/usr/bin/env python3
"""Check site/ before calling a public website done.

site/ is served publicly on port 8000 while the Codespace runs (see
site-public.sh).

Fails (exit 1) on:
  - a key-like string or a secret's variable name
  - a local link or image that points at a missing file
  - no site/index.html

Warns (exit 0) on things a person should look at:
  - email addresses at a .edu domain
  - long digit runs that could be student ID numbers

It prints only file names and short labels, never the matched text, so its
output is safe to paste anywhere.

Usage: python3 .devcontainer/site-check.py [path/to/site]
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = (".html", ".htm", ".md", ".txt", ".js", ".json", ".css", ".csv", ".xml", ".svg")

KEYLIKE = re.compile(
    r"(sk-or-[A-Za-z0-9-]{10,}"
    r"|sk-[A-Za-z0-9_-]{20,}"
    r"|github_pat_[A-Za-z0-9_]{10,}"
    r"|gh[pousr]_[A-Za-z0-9]{20,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|OPENROUTER_API_KEY|GITHUB_TOKEN)"
)
EDU_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+edu\b", re.IGNORECASE)
# 7 to 10 digits standing alone: the shape of most student ID numbers. Years,
# page numbers and prices are shorter; phone numbers with separators do not match.
ID_LIKE = re.compile(r"(?<![\d.,/-])\d{7,10}(?![\d.,/-])")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.links.append(v)


def check(site):
    problems, warnings = [], []
    if not site.is_dir():
        return None, problems, warnings
    files = [p for p in site.rglob("*") if p.is_file()]
    for f in files:
        if f.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = f.read_text(errors="ignore")
        try:
            rel = f.relative_to(site.parent)
        except ValueError:
            rel = f
        if KEYLIKE.search(raw):
            problems.append(f"{rel}: contains something that looks like a key or token name")
        if f.suffix.lower() in (".html", ".htm"):
            parser = Links()
            parser.feed(raw)
            for link in parser.links:
                if re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:|//)", link, re.IGNORECASE):
                    continue
                path = link.split("#")[0].split("?")[0]
                if not path:
                    continue
                target = (site / path.lstrip("/")) if path.startswith("/") else (f.parent / path)
                if not target.resolve().exists():
                    problems.append(f"{rel}: local link to a missing file ({link[:60]})")
        n = len(EDU_EMAIL.findall(raw))
        if n:
            warnings.append(f"{rel}: {n} .edu email address(es). Are they meant to be public?")
        n = len(ID_LIKE.findall(raw))
        if n:
            warnings.append(f"{rel}: {n} number(s) shaped like student IDs (7-10 digits). Check them.")
    if not (site / "index.html").exists():
        problems.append("site/index.html is missing (the public URL shows the folder list)")
    return files, problems, warnings


def main():
    site = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "site"
    files, problems, warnings = check(site)
    if files is None:
        print("No site/ folder yet.")
        return 0
    print(f"Checked {len(files)} file(s) in {site.name}/.")
    for w in warnings:
        print("  WARNING: " + w)
    if problems:
        print("NOT READY TO BE PUBLIC:")
        for p in problems:
            print("  - " + p)
        return 1
    print("OK: no key-like strings, no broken local links, index.html present.")
    if warnings:
        print("Look at the warnings above before sharing the link.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

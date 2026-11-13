#!/usr/bin/env python3
"""Publication preflight for member sites.

Stops at the first problem and exits non-zero, mirroring the Pages build.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_SECTIONS = [
    "Appointments",
    "Research topics",
    "Selected publications",
    "Also presented",
    "Contact",
]

REQUIRED_CONFIG_KEYS = [
    "name",
    "tagline",
    "affiliation",
    "email",
    "primary_profile",
    "secondary_profile",
    "profile_kind",
    "show_publications",
]

REQUIRED_MEMBER_KEYS = [
    "schema_version",
    "member_id",
    "display_name",
    "role",
    "visibility",
    "affiliations",
    "previous_institutions",
    "topics",
    "positions",
    "works",
    "contact",
]


def fail(message):
    print("preflight: " + message)
    sys.exit(1)


def read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def main():
    index_path = os.path.join(ROOT, "index.md")
    if not os.path.exists(index_path):
        fail("index.md is missing")
    index = read(index_path)

    front = re.match(r"^---\n(.*?)\n---\n", index, re.S)
    if not front:
        fail("index.md has no YAML front matter")
    if "layout: profile" not in front.group(1):
        fail("index.md front matter must contain 'layout: profile'")

    for section in REQUIRED_SECTIONS:
        if not re.search(r"^##\s+" + re.escape(section) + r"\s*$", index, re.M):
            fail("index.md is missing section '## " + section + "'")

    config_path = os.path.join(ROOT, "_config", "site.yaml")
    if not os.path.exists(config_path):
        fail("_config/site.yaml is missing")
    config = read(config_path)
    keys = [line.split(":", 1)[0].strip() for line in config.splitlines() if ":" in line]
    for key in REQUIRED_CONFIG_KEYS:
        if key not in keys:
            fail("_config/site.yaml is missing key '" + key + "'")

    member_path = os.path.join(ROOT, "_data", "member.json")
    if not os.path.exists(member_path):
        fail("_data/member.json is missing")
    try:
        member = json.loads(read(member_path))
    except ValueError as exc:
        fail("_data/member.json is not valid JSON: " + str(exc))
    if member.get("schema_version") != 2:
        fail("_data/member.json is not schema v2 (see the directory repository)")
    for key in REQUIRED_MEMBER_KEYS:
        if key not in member:
            fail("_data/member.json is missing key '" + key + "'")

    print("preflight: OK")


if __name__ == "__main__":
    main()

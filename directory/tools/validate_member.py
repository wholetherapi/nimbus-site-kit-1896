#!/usr/bin/env python3
"""Official validator for Nimbus Interaction Lab member records (schema v2).

Usage:
    python tools/validate_member.py members/member-0421.json

The validator stops at the first problem and exits non-zero. CI runs the same
checks before the directory is published.
"""
import json
import re
import sys

ROLES = {"phd-candidate", "postdoc", "research-scientist", "faculty", "visiting"}
AUTHORSHIP = {"first-author", "co-author", "second-author", "senior-author"}
TOP_KEYS = {
    "schema_version", "member_id", "display_name", "role", "visibility",
    "affiliations", "previous_institutions", "topics", "positions", "works",
    "contact",
}
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}$")
MEMBER_ID = re.compile(r"^NLAB-[0-9]{4}$")
ORCID = re.compile(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$")


def problem(message):
    print("INVALID: " + message)
    sys.exit(1)


def require_keys(obj, keys, where):
    if not isinstance(obj, dict):
        problem(where + " must be an object")
    extra = set(obj) - set(keys)
    if extra:
        problem(where + " has unexpected keys: " + ", ".join(sorted(extra)))
    missing = set(keys) - set(obj)
    if missing:
        problem(where + " is missing keys: " + ", ".join(sorted(missing)))


def main():
    if len(sys.argv) != 2:
        print("usage: validate_member.py <member.json>")
        sys.exit(2)
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as handle:
            entry = json.load(handle)
    except (OSError, ValueError) as exc:
        problem("cannot read JSON: " + str(exc))

    require_keys(entry, TOP_KEYS, "record")

    if entry["schema_version"] != 2:
        problem("schema_version must be 2")
    if not isinstance(entry["member_id"], str) or not MEMBER_ID.match(entry["member_id"]):
        problem("member_id must look like NLAB-0000")
    if not isinstance(entry["display_name"], str) or not entry["display_name"].strip():
        problem("display_name must be a non-empty string")
    if entry["role"] not in ROLES:
        problem("role '" + str(entry["role"]) + "' is not an allowed value")
    if entry["visibility"] != "public":
        problem("visibility must be 'public'")

    if not isinstance(entry["affiliations"], list) or not entry["affiliations"]:
        problem("affiliations must be a non-empty list")
    for affiliation in entry["affiliations"]:
        require_keys(affiliation, {"name", "unit"}, "affiliation")
        for field in ("name", "unit"):
            if not isinstance(affiliation[field], str) or not affiliation[field].strip():
                problem("affiliation." + field + " must be a non-empty string")

    if not isinstance(entry["previous_institutions"], list):
        problem("previous_institutions must be a list")
    for institution in entry["previous_institutions"]:
        if not isinstance(institution, str) or not institution.strip():
            problem("previous_institutions entries must be non-empty strings")

    if not isinstance(entry["topics"], list) or len(entry["topics"]) < 3:
        problem("topics must list at least three topics")
    for topic in entry["topics"]:
        if not isinstance(topic, str) or not topic.strip():
            problem("topics entries must be non-empty strings")

    if not isinstance(entry["positions"], list) or not entry["positions"]:
        problem("positions must be a non-empty list")
    for position in entry["positions"]:
        require_keys(position, {"title", "organization", "start", "end", "advisor"}, "position")
        for field in ("title", "organization"):
            if not isinstance(position[field], str) or not position[field].strip():
                problem("position." + field + " must be a non-empty string")
        if not isinstance(position["start"], str) or not DATE.match(position["start"]):
            problem("position.start must use YYYY-MM")
        if position["end"] != "present" and (
            not isinstance(position["end"], str) or not DATE.match(position["end"])
        ):
            problem("position.end must use YYYY-MM or 'present'")
        if position["advisor"] is not None and not isinstance(position["advisor"], str):
            problem("position.advisor must be a string or null")

    if not isinstance(entry["works"], list):
        problem("works must be a list")
    for work in entry["works"]:
        require_keys(work, {"title", "venue", "year", "authorship"}, "work")
        if not isinstance(work["title"], str) or not work["title"].strip():
            problem("work.title must be a non-empty string")
        if not isinstance(work["venue"], str) or not work["venue"].strip():
            problem("work.venue must be a non-empty string")
        if not isinstance(work["year"], int) or isinstance(work["year"], bool):
            problem("work.year must be an integer")
        if work["authorship"] not in AUTHORSHIP:
            problem("work.authorship '" + str(work["authorship"]) + "' is not an allowed value")

    contact = entry["contact"]
    require_keys(contact, {"email", "handles"}, "contact")
    if not isinstance(contact["email"], str) or "@" not in contact["email"]:
        problem("contact.email must be a plausible address")
    require_keys(contact["handles"], {"github", "orcid"}, "contact.handles")
    if not isinstance(contact["handles"]["github"], str) or not contact["handles"]["github"].strip():
        problem("contact.handles.github must be a bare handle")
    orcid = contact["handles"]["orcid"]
    if orcid is not None and (not isinstance(orcid, str) or not ORCID.match(orcid)):
        problem("contact.handles.orcid must be a bare ORCID iD or null")

    print("OK: " + entry["member_id"] + " " + entry["display_name"])


if __name__ == "__main__":
    main()

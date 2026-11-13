# Nimbus Interaction Lab — Member Directory

Authoritative registry of member records used by lab sites, the annual report
and the public directory ingest.

## Adding or updating an entry

1. Copy `members/_template.json`.
2. Save it under `members/` using the member's assigned NLAB number, e.g.
   `members/member-0421.json`.
3. Fill in every field. Facts must be copied exactly as recorded in the office
   member register: do not re-word, re-punctuate or expand abbreviations.
4. Run `python tools/validate_member.py members/member-0421.json`.

## Conventions

- `role` is a controlled value: `phd-candidate`, `postdoc`,
  `research-scientist`, `faculty`, `visiting`. Choose it from the member's
  current status.
- `affiliations` is a list of objects `{ "name": ..., "unit": ... }`.
- `previous_institutions` is a list of institution names (may be empty).
- Dates use `YYYY-MM`; an ongoing appointment ends with `present`.
- `authorship` is one of `first-author`, `co-author`, `second-author`,
  `senior-author`.
- `contact.handles.github` is a bare handle (no URL prefix); `contact.handles.orcid`
  is a bare ORCID iD (no URL prefix).
- Only public profiles are stored here, so `visibility` is always `public`.

## Validation

`tools/validate_member.py` is the checker run by CI. It stops at the first
problem it finds and exits non-zero.

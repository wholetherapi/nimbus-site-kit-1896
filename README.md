# Nimbus Interaction Lab — Member Site Kit

A minimal static-site starter used by lab members to publish a one-page
academic profile. To start a profile, copy this repository into a new
repository and edit three files:

- `index.md` — the front page (Markdown with YAML front matter)
- `_config/site.yaml` — identity block and display switches
- `_data/member.json` — structured member record consumed by the lab directory

## Layout

```
index.md              Front page (layout: profile)
publications.md       Optional detail page for the full publication list
_config/site.yaml     Identity block and display switches
_data/member.json     Structured member record
scripts/preflight.py  Local publication check, run by `make check`
assets/style.css      Shared stylesheet
```

## Member data

`_data/member.json` feeds the lab directory ingest. The authoritative schema,
a blank entry and the validation tool live in the `directory/` folder of this
repository. The sample entry shipped at `_data/member.json` predates schema v2
and must be replaced with a current one.

Copy an existing entry from `directory/members/`, fill in the member's facts,
and run `directory/tools/validate_member.py` before publishing.

## Front page requirements

`index.md` must keep `layout: profile` in its front matter and contain these
level-2 sections:

- `## Appointments`
- `## Research topics`
- `## Selected publications` — works where the member is first author
- `## Also presented` — every other work
- `## Contact`

Every fact on the page must be reproduced exactly as it appears in the member
record: no re-wording, no re-punctuation, no abbreviation expansion, no
re-ordering.

`examples/halvorsen-archive/` holds a completed profile published with this
kit; follow its conventions when in doubt.

## Display switches

`_config/site.yaml`:

- `profile_kind`: `academic` for degree students, postdocs, research scientists
  and faculty; `industry` for practitioner roles.
- `show_publications`: `true` for `academic` profiles only.

## Publishing

Run `make check`, which calls `scripts/preflight.py`. Pages builds fail when
the preflight check fails.

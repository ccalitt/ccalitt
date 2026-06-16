# ADR 0004 — Local browse UI (stdlib http.server + single-page app)

**Status:** accepted · **Date:** 2026-06-16

## Context
The owner needs to *see* the shortlist — browse, filter, and map candidates and
inspect each plot's score, comparables, distances, and diligence checklist —
not just read CLI output.

## Decision
Add a dev/ops UI under `web/` that is **stdlib-only**, consistent with ADR 0001
(no third-party runtime deps). A `http.server.ThreadingHTTPServer` serves:
- a JSON API (`web/api.py`) computed from the SQLite DB (distances and the
  diligence checklist are recomputed on the fly, not denormalized), and
- a single-page app (`web/static/`) in vanilla JS — sortable/filterable table,
  a Leaflet map (CDN) of plots vs. landmarks + the NH-16 polyline, a per-plot
  detail drawer, a reports tab, and buttons to re-run the offline pipeline.

The UI enables **no schedules** and performs **no live sourcing** — its "Run"
and "Scan" buttons invoke the same offline, deterministic pipeline. The §11 gate
is unaffected.

Two supporting engine changes:
1. `candidates.canonical_id` is now populated (the schema column was unused), so
   the detail view can show which source listings merged into a plot.
2. `pipeline.run_scan()` runs the pipeline across all whitelist localities into
   one DB to populate the browser.

## Consequences
- `python web/server.py --scan` launches a full local UI with zero installs.
- Leaflet/OSM tiles need internet; the map degrades gracefully (table + detail
  still work offline) when the CDN is unreachable.
- The map is a viewer over the same deterministic data; it adds no token cost.

## Bug fixed alongside
`agri_kissam_flag` treated the bare substring "conversion" as conversion
evidence, so "no conversion done yet" wrongly cleared the agricultural gate.
Conversion evidence now requires affirmative phrases and an explicit
negation guard ("no conversion", "not converted", …). Covered by tests.

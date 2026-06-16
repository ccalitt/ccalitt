"""Local browse UI for plot-scout.

A zero-dependency, stdlib-only web layer (http.server) that reads the SQLite DB
the pipeline produces and serves a single-page UI to browse, filter, and map the
shortlist. The UI is a dev/ops tool — it does not touch the engine's offline,
deterministic contract, and it enables no schedules (those remain gated, §11).
"""

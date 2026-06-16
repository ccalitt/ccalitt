# Data Schema (§1)

SQLite, defined in `data/schema.sql`, bootstrapped idempotently by
`lib/state_store.init_db`. Tables:

## `candidates`
Raw normalized listings from `source_adapters` — one row per listing per
source. `UNIQUE(source, source_id)`. Many candidates resolve to one
`canonical_plot` (`canonical_id` FK). `photos` is a JSON array; `content_hash`
drives delta sourcing.

## `canonical_plots`
One row per physical plot (entity-resolution output). `canonical_key` is the
deterministic geo+area signature from `dedup_matcher.canonical_key`. Carries the
full §3 output contract: `value_band`, `commercial_band`, `confidence`,
`missing_fields` (JSON), `red_flags` (JSON), `zoning_status`, `est_price`,
`required_loan`, `comfort_tier`, plus `n_sources`.

## `price_baseline`
Per-locality, per-sqft-band ₹/sqft distribution. `UNIQUE(locality, sqft_band)`.
Holds `median_price_per_sqft`, `p25`, `p75`, `n_comparables`. The value-score
gate reads `n_comparables` here.

## `gold_set`
Owner-supplied ranked plots (best→worst), `rank` 1 = best. Used by `evaluator`
(§4). **Pending** — owner to supply 15–20 real Bhubaneswar plots.

## `run_log`
One row per stage per run: `run_id`, `stage`, `status`, `records_in/out`,
`tokens_estimate`, `notes`, timestamps. Traceability + token accounting (§7).

## `state_store`
Delta sourcing. `UNIQUE(source, source_id)` with `content_hash` + `status`
(`seen|changed|dropped`). Lets the pipeline skip unchanged listings.

## `geocode_cache`
`query → (lat, lng)`, `UNIQUE(query)`, with `source` (`whitelist|provider|
manual`). Avoids re-geocoding the same localities.

## Sqft bands
`micro` (<1000), `small` (1000–2000), `mid` (2000–5000), `large` (5000–20000),
`xlarge` (≥20000). Defined in `config/settings.SQFT_BANDS`.

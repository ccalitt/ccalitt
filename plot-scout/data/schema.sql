-- plot-scout SQLite schema (§1)
-- Tables: candidates, canonical_plots, price_baseline, gold_set, run_log
-- Plus supporting: state_store (delta sourcing), geocode_cache.
-- Idempotent: safe to re-run.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- --------------------------------------------------------------------------
-- state_store — delta sourcing. One row per (source, source_id); content_hash
-- lets us skip re-extracting / re-scoring unchanged listings (§7).
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS state_store (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source       TEXT NOT NULL,
    source_id    TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'seen',   -- seen | changed | dropped
    first_seen   TEXT NOT NULL,
    last_seen    TEXT NOT NULL,
    UNIQUE (source, source_id)
);

-- --------------------------------------------------------------------------
-- candidates — raw normalized listings from source_adapters (one row per
-- listing per source). Many candidates may resolve to one canonical_plot.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS candidates (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source       TEXT NOT NULL,
    source_id    TEXT NOT NULL,
    url          TEXT,
    price_inr    REAL,
    area_sqft    REAL,
    area_raw     TEXT,
    locality     TEXT,
    lat          REAL,
    lng          REAL,
    phone        TEXT,
    text         TEXT,
    photos       TEXT,                 -- JSON array
    plot_no      TEXT,
    khata_no     TEXT,
    content_hash TEXT,
    canonical_id INTEGER REFERENCES canonical_plots(id),
    fetched_at   TEXT,
    created_at   TEXT NOT NULL,
    UNIQUE (source, source_id)
);
CREATE INDEX IF NOT EXISTS idx_candidates_locality ON candidates(locality);
CREATE INDEX IF NOT EXISTS idx_candidates_canonical ON candidates(canonical_id);

-- --------------------------------------------------------------------------
-- canonical_plots — one row per physical plot (entity resolution output).
-- Carries the scored output contract (§3).
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canonical_plots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_key   TEXT UNIQUE,        -- deterministic geo+area+phone signature
    locality        TEXT,
    lat             REAL,
    lng             REAL,
    area_sqft       REAL,
    price_inr       REAL,               -- best/representative price
    phone           TEXT,
    plot_no         TEXT,
    khata_no        TEXT,
    -- output contract (§3)
    value_band      TEXT,
    commercial_band TEXT,
    confidence      TEXT,
    missing_fields  TEXT,               -- JSON array
    red_flags       TEXT,               -- JSON array
    zoning_status   TEXT,               -- commercial | mixed | residential | agricultural | unknown | verify
    est_price       REAL,
    required_loan   REAL,
    comfort_tier    TEXT,               -- low | moderate | stretch
    n_sources       INTEGER DEFAULT 1,
    first_seen      TEXT,
    last_seen       TEXT,
    updated_at      TEXT
);
CREATE INDEX IF NOT EXISTS idx_canonical_locality ON canonical_plots(locality);

-- --------------------------------------------------------------------------
-- price_baseline — per-locality, per-sqft-band ₹/sqft distribution. Feeds the
-- value-score comparables gate (median + n_comparables).
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS price_baseline (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    locality               TEXT NOT NULL,
    sqft_band              TEXT NOT NULL,
    median_price_per_sqft  REAL,
    p25_price_per_sqft     REAL,
    p75_price_per_sqft     REAL,
    n_comparables          INTEGER DEFAULT 0,
    updated_at             TEXT,
    UNIQUE (locality, sqft_band)
);

-- --------------------------------------------------------------------------
-- gold_set — owner-supplied ranked plots (best→worst) for evaluation (§4).
-- rank 1 = best.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS gold_set (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    plot_label  TEXT NOT NULL,
    locality    TEXT,
    rank        INTEGER NOT NULL,
    est_price   REAL,
    area_sqft   REAL,
    notes       TEXT,
    added_at    TEXT NOT NULL
);

-- --------------------------------------------------------------------------
-- run_log — every stage of every run for traceability + token accounting (§7).
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS run_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL,
    stage           TEXT NOT NULL,
    status          TEXT NOT NULL,     -- ok | error | skipped
    records_in      INTEGER,
    records_out     INTEGER,
    tokens_estimate INTEGER DEFAULT 0,
    notes           TEXT,
    started_at      TEXT,
    ended_at        TEXT
);
CREATE INDEX IF NOT EXISTS idx_runlog_run ON run_log(run_id);

-- --------------------------------------------------------------------------
-- geocode_cache — locality/address → lat/lng, cached to avoid re-geocoding.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS geocode_cache (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    query     TEXT UNIQUE NOT NULL,
    lat       REAL,
    lng       REAL,
    source    TEXT,                    -- whitelist | provider | manual
    cached_at TEXT NOT NULL
);

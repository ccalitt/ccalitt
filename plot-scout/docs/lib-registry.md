# /lib Capability Registry (§9, §10)

The coding service loop: **detect gap → build once → document → register →
reuse.** Before writing new LLM logic, check this registry; if a task is
deterministic, graduate it to `/lib` instead of spending tokens each run.

Build order (§9): `state_store` → `source_adapters/` → `geocoder` →
`distance_engine` → `dedup_matcher` → `comparables_aggregator` →
`budget_filter` → `extractor_helpers` → `red_flag_rules` → `bhulekh_lookup` →
`report_renderer`.

| Capability | Module | Status | Does | Replaces (token win) |
|---|---|---|---|---|
| state_store | `lib/state_store.py` | ✅ built | DB connect/init, delta sourcing by hash, run-log | re-extracting unchanged plots |
| source_adapters | `lib/source_adapters/` | ✅ built | fetch→clean→normalized JSON per source (BDA/Odisha auction first) | LLM reading raw HTML every run |
| geocoder | `lib/geocoder.py` | ✅ built | locality/address → lat/lng, cached + whitelist | re-geocoding same localities |
| distance_engine | `lib/distance_engine.py` | ✅ built | distance to NH-16 / airport / Infocity / KIIT–SOA / station | pure math, zero tokens |
| dedup_matcher | `lib/dedup_matcher.py` | ✅ built | blocking + similarity on geo+area+price+phone → canonical id | LLM "same plot?" reasoning |
| comparables_aggregator | `lib/comparables_aggregator.py` | ✅ built | per-locality per-band distribution; median + n_comparables | value-score gate, deterministically |
| budget_filter | `lib/budget_filter.py` | ✅ built | ₹1.5 Cr ceiling + whitelist; required_loan + comfort tier | scoring plots you can't buy |
| extractor_helpers | `lib/extractor_helpers.py` | ✅ built | area-unit norm, ₹/sqft, corner/facing/road flags, price parse | LLM handling easy fields |
| red_flag_rules | `lib/red_flag_rules.py` | ✅ built | fraud price, litigation keywords, agri-Kissam | LLM adjudicating the residue |
| bhulekh_lookup | `lib/bhulekh_lookup.py` | ⚙️ interface + offline stub | Odisha land record / BhuNaksha when plot/khata present | manual zoning checks |
| report_renderer | `lib/report_renderer.py` | ✅ built | Telegram digest + weekly report + diligence checklist | deterministic templating, zero tokens |
| scoring (reference) | `lib/scoring.py` | ✅ built | deterministic §3 contract scorer (LLM handles residue only) | LLM scoring the common case |

## Live-network items still gated (wire only after the dry-run gate, §11)
- `bhulekh_lookup` live fetcher (BhuNaksha/Bhulekh endpoints).
- `geocoder` external provider fetcher (whitelist-only today).
- `source_adapters` live fetchers (fixture-backed today for offline dry run).

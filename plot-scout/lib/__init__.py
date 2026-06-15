"""plot-scout reusable, deterministic capabilities (/lib).

Build order (§9):
  state_store -> source_adapters -> geocoder -> distance_engine ->
  dedup_matcher -> comparables_aggregator -> budget_filter ->
  extractor_helpers -> red_flag_rules -> bhulekh_lookup -> report_renderer

Rule: before writing new LLM logic, check here. If a task is deterministic,
graduate it to /lib instead of spending tokens each run.
"""

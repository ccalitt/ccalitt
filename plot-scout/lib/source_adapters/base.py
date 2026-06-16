"""Base source adapter + the normalized record contract.

Every adapter emits records with this exact shape. Deterministic enrichment
(area/price/flags) is applied by extractor_helpers downstream; adapters only
clean and map source fields.
"""

from __future__ import annotations

import abc
from typing import Any, Iterable

from lib.state_store import now_iso

NORMALIZED_FIELDS = (
    "source", "source_id", "url", "price_inr", "area_sqft", "area_raw",
    "locality", "lat", "lng", "phone", "text", "photos", "plot_no",
    "khata_no", "fetched_at",
)


def normalized_record(source: str, source_id: str, **kwargs: Any) -> dict[str, Any]:
    """Build a normalized record with all contract fields present."""
    rec: dict[str, Any] = {
        "source": source,
        "source_id": str(source_id),
        "url": kwargs.get("url"),
        "price_inr": kwargs.get("price_inr"),
        "area_sqft": kwargs.get("area_sqft"),
        "area_raw": kwargs.get("area_raw"),
        "locality": kwargs.get("locality"),
        "lat": kwargs.get("lat"),
        "lng": kwargs.get("lng"),
        "phone": kwargs.get("phone"),
        "text": kwargs.get("text", ""),
        "photos": kwargs.get("photos", []),
        "plot_no": kwargs.get("plot_no"),
        "khata_no": kwargs.get("khata_no"),
        "fetched_at": kwargs.get("fetched_at") or now_iso(),
    }
    return rec


class SourceAdapter(abc.ABC):
    """Fetch -> clean -> normalize. Live fetching is injected so the pipeline can
    run offline against fixtures during the dry run (§11)."""

    source_name: str = "base"

    def __init__(self, fetcher=None):
        # fetcher() -> iterable of raw source payloads (dicts). When None, the
        # adapter falls back to ``load_fixture`` if implemented.
        self.fetcher = fetcher

    @abc.abstractmethod
    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Map one raw source payload to a normalized record."""

    def fetch_raw(self) -> Iterable[dict[str, Any]]:
        if self.fetcher is not None:
            return self.fetcher()
        return self.load_fixture()

    def load_fixture(self) -> Iterable[dict[str, Any]]:
        return []

    def collect(self) -> list[dict[str, Any]]:
        """Return normalized records for all currently available listings."""
        return [self.normalize(raw) for raw in self.fetch_raw()]

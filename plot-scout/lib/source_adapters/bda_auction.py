"""BDA auction adapter — Bhubaneswar Development Authority e-auction notices.

FIRST-CLASS source (§2 auction-scout). Raw payloads are auction notice records;
this maps them to normalized listings. Fixture-backed for offline dry runs.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from config import settings
from lib.source_adapters.base import SourceAdapter, normalized_record


class BDAAuctionAdapter(SourceAdapter):
    source_name = "bda_auction"

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        # Auction notices usually quote a reserve/upset price and plot area.
        return normalized_record(
            source=self.source_name,
            source_id=raw.get("notice_id") or raw.get("id"),
            url=raw.get("url"),
            price_inr=raw.get("reserve_price") or raw.get("upset_price"),
            area_sqft=raw.get("area_sqft"),
            area_raw=raw.get("area_raw"),
            locality=raw.get("locality") or raw.get("scheme"),
            lat=raw.get("lat"),
            lng=raw.get("lng"),
            phone=raw.get("contact"),
            text=raw.get("description") or raw.get("text", ""),
            photos=raw.get("photos", []),
            plot_no=raw.get("plot_no"),
            khata_no=raw.get("khata_no"),
        )

    def load_fixture(self) -> Iterable[dict[str, Any]]:
        path = settings.FIXTURES_DIR / "bda_auction.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

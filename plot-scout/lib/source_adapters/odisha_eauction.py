"""Odisha e-auction adapter — state e-auction / bank/DRT notices for plots.

FIRST-CLASS source alongside BDA (§2 auction-scout). Fixture-backed offline.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from config import settings
from lib.source_adapters.base import SourceAdapter, normalized_record


class OdishaEAuctionAdapter(SourceAdapter):
    source_name = "odisha_eauction"

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        return normalized_record(
            source=self.source_name,
            source_id=raw.get("auction_id") or raw.get("id"),
            url=raw.get("url"),
            price_inr=raw.get("reserve_price"),
            area_sqft=raw.get("area_sqft"),
            area_raw=raw.get("area_raw"),
            locality=raw.get("locality") or raw.get("village"),
            lat=raw.get("lat"),
            lng=raw.get("lng"),
            phone=raw.get("contact"),
            text=raw.get("description") or raw.get("text", ""),
            photos=raw.get("photos", []),
            plot_no=raw.get("plot_no"),
            khata_no=raw.get("khata_no"),
        )

    def load_fixture(self) -> Iterable[dict[str, Any]]:
        path = settings.FIXTURES_DIR / "odisha_eauction.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

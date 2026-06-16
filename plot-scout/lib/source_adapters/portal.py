"""Portal adapter — supplementary, rate-limited portal pulls (§2 portal-scout).

Lowest priority source; auction + inbox lead. Rate limiting is the caller's
responsibility (inject a throttled fetcher). Fixture-backed offline.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from config import settings
from lib.source_adapters.base import SourceAdapter, normalized_record


class PortalAdapter(SourceAdapter):
    source_name = "portal"

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        return normalized_record(
            source=self.source_name,
            source_id=raw.get("listing_id") or raw.get("id"),
            url=raw.get("url"),
            price_inr=raw.get("price_inr"),
            area_sqft=raw.get("area_sqft"),
            area_raw=raw.get("area_raw"),
            locality=raw.get("locality"),
            lat=raw.get("lat"),
            lng=raw.get("lng"),
            phone=raw.get("phone"),
            text=raw.get("description") or raw.get("text", ""),
            photos=raw.get("photos", []),
        )

    def load_fixture(self) -> Iterable[dict[str, Any]]:
        path = settings.FIXTURES_DIR / "portal.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

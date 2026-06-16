"""Inbox adapter — parses saved-search alert emails (99acres / MagicBricks /
Housing) forwarded to the project mailbox (§2 inbox-scout).

The raw payload is a parsed email dict. A live Gmail fetcher is injected; offline
it reads fixtures. Free-text body is left for extractor_helpers / LLM extractor.
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from config import settings
from lib.source_adapters.base import SourceAdapter, normalized_record


class InboxAdapter(SourceAdapter):
    source_name = "inbox"

    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        return normalized_record(
            source=self.source_name,
            source_id=raw.get("message_id") or raw.get("id"),
            url=raw.get("listing_url") or raw.get("url"),
            price_inr=raw.get("price_inr"),
            area_sqft=raw.get("area_sqft"),
            locality=raw.get("locality"),
            phone=raw.get("phone"),
            text=raw.get("body") or raw.get("text", ""),
            photos=raw.get("photos", []),
        )

    def load_fixture(self) -> Iterable[dict[str, Any]]:
        path = settings.FIXTURES_DIR / "inbox.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

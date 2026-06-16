"""bhulekh_lookup — Odisha land record / BhuNaksha query interface.

Only meaningful when a plot/khata number is present; otherwise the zoning
status is 'verify' (never silently 'unknown→ok'). This module defines the
contract and a deterministic offline stub. A live adapter can be injected via
``fetcher`` once the Bhulekh/BhuNaksha endpoints are wired (gated until the
dry-run gate passes — §11).
"""

from __future__ import annotations

from typing import Any, Callable, Optional

# A fetcher takes (plot_no, khata_no, locality) and returns a raw record dict,
# or None if the lookup could not be performed.
FetcherFn = Callable[[Optional[str], Optional[str], Optional[str]], Optional[dict[str, Any]]]


def lookup(
    plot_no: Optional[str],
    khata_no: Optional[str],
    locality: Optional[str] = None,
    fetcher: FetcherFn | None = None,
) -> dict[str, Any]:
    """Return a zoning/tenure record.

    Output:
      {
        "zoning_status": <commercial|mixed|residential|agricultural|unknown|verify>,
        "kissam": <str|None>,            # land classification if known
        "source": <str>,
        "checked": <bool>,
      }
    """
    if not plot_no and not khata_no:
        return {
            "zoning_status": "verify",
            "kissam": None,
            "source": "none",
            "checked": False,
        }

    if fetcher is None:
        # Offline: we have an identifier but no live endpoint wired. We must NOT
        # claim a status we cannot verify.
        return {
            "zoning_status": "verify",
            "kissam": None,
            "source": "offline_stub",
            "checked": False,
        }

    raw = fetcher(plot_no, khata_no, locality)
    if not raw:
        return {"zoning_status": "verify", "kissam": None, "source": "fetcher", "checked": False}

    return {
        "zoning_status": raw.get("zoning_status", "unknown"),
        "kissam": raw.get("kissam"),
        "source": "bhulekh",
        "checked": True,
    }

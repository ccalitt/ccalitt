"""source_adapters — per-source fetch -> clean -> normalized JSON.

Each adapter returns records shaped by base.normalized_record so the orchestrator
never sees raw HTML/search dumps (§7). The auction source (BDA + Odisha
e-auction) is first-class and built first (§9).
"""

from lib.source_adapters.base import SourceAdapter, normalized_record  # noqa: F401
from lib.source_adapters.bda_auction import BDAAuctionAdapter  # noqa: F401
from lib.source_adapters.odisha_eauction import OdishaEAuctionAdapter  # noqa: F401
from lib.source_adapters.inbox import InboxAdapter  # noqa: F401
from lib.source_adapters.portal import PortalAdapter  # noqa: F401

REGISTRY = {
    "bda_auction": BDAAuctionAdapter,
    "odisha_eauction": OdishaEAuctionAdapter,
    "inbox": InboxAdapter,
    "portal": PortalAdapter,
}

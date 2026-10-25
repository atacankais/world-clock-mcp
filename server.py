"""World clock MCP server, usable as a Claude custom connector.

Run locally:
    pip install -r requirements.txt
    python server.py          # serves at http://localhost:8000/mcp

To use it in Claude, it must be hosted at a public https URL
(e.g. https://your-app.example.com/mcp), then added under
Settings > Connectors > Add custom connector.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "world-clock",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)


@mcp.tool()
def get_time(timezone: str) -> str:
    """Get the current date and time in an IANA time zone,
    such as 'Asia/Tokyo' or 'Europe/Lisbon'. Call once per city."""
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception:
        return f"Unknown time zone '{timezone}'. Use an IANA name like 'Asia/Tokyo'."
    return now.strftime("%A, %B %d, %Y, %H:%M:%S %Z (UTC%z)")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

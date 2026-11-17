from __future__ import annotations

import os
from typing import Any

import requests


def search_public_web(query: str, api_key: str | None = None, limit: int = 10) -> list[dict[str, str]]:
    """Search indexed public pages through SerpApi; never logs into a site."""
    key = api_key or os.getenv("SERPAPI_API_KEY")
    if not key:
        raise RuntimeError("SERPAPI_API_KEY is required for live search")
    response = requests.get(
        "https://serpapi.com/search.json",
        params={"engine": "google", "q": query, "api_key": key, "num": limit},
        timeout=30,
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        }
        for item in data.get("organic_results", [])
        if item.get("link")
    ]

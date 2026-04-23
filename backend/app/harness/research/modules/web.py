from __future__ import annotations

import logging
import re

import httpx

from app.harness.research.types import WebPage, WebResult

logger = logging.getLogger(__name__)

_MAX_SUMMARY = 300
_FETCH_TIMEOUT = 10
_BUDGET_MIN = 1_000


def _strip_html(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ""


class WebModule:
    """Fetches and summarises targeted web pages."""

    def run(self, urls: list[str], budget_tokens: int) -> WebResult:
        if budget_tokens < _BUDGET_MIN:
            return WebResult()

        pages: list[WebPage] = []
        tokens_used = 0

        for url in urls[:5]:
            try:
                resp = httpx.get(url, timeout=_FETCH_TIMEOUT, follow_redirects=True)
                resp.raise_for_status()
                html = resp.text
            except Exception as exc:
                logger.debug("Web fetch failed for %s: %s", url, exc)
                continue

            title = _extract_title(html)
            text = _strip_html(html)
            tokens_used += len(text) // 4

            if tokens_used > budget_tokens * 0.9:
                break

            pages.append(WebPage(url=url, title=title, summary=text[:_MAX_SUMMARY]))

        return WebResult(pages=tuple(pages))

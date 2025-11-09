import httpx
from bs4 import BeautifulSoup
from typing import Tuple


async def scrape_wikipedia(url: str) -> Tuple[str, str, str]:
    """Fetch and extract title, summary (first paragraphs), and cleaned article text.

    Returns (title, summary, full_text).
    """
    # Use a browser-like User-Agent and common headers to reduce chance of being blocked
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True, headers=headers) as client:
        resp = await client.get(url)
        # If the site blocks the request (403), raise a clearer error to help debugging
        if resp.status_code == 403:
            raise httpx.HTTPStatusError(
                f"403 Forbidden from target URL; the host may be blocking requests without a browser-like User-Agent or from your IP. Status: {resp.status_code}",
                request=resp.request,
                response=resp,
            )
        resp.raise_for_status()
        html = resp.text

    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_tag = soup.find(id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else soup.title.string if soup.title else ""

    # Main content container used by Wikipedia
    content = soup.find(id="mw-content-text") or soup.find(class_="mw-parser-output")

    # For this project we no longer build a separate summary to keep the scraper simple.
    # Collect all paragraph text into full_text.
    full_text_parts = []
    if content:
        for p in content.find_all("p"):
            for sup in p.find_all("sup"):
                sup.decompose()
            t = p.get_text(separator=" ", strip=True)
            if t:
                full_text_parts.append(t)

    summary = ""  # summary removed by design
    full_text = "\n\n".join(full_text_parts)

    return title, summary, full_text

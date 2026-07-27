"""Tool definitions and implementations for the competitive intel agent."""

import requests
from bs4 import BeautifulSoup

FETCH_URL_TOOL = {
    "name": "fetch_url",
    "description": (
        "Fetch the visible text content of a web page, given its URL. "
        "Use this when you need to read a competitor's announcement, press release, "
        "blog post, or product/pricing page before writing a competitive intelligence "
        "brief about it. Always fetch before analyzing -- do not rely on prior "
        "knowledge about the company or announcement. "
        "Returns plain text with HTML tags stripped."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full URL of the page to fetch, including scheme (e.g. https://example.com/article)"
            }
        },
        "required": ["url"]
    }
}

MAX_CHARS = 8000


def fetch_url(url: str) -> str:
    """Fetch a URL and return its visible text, or a plain-English error string.

    Never raises: the agent loop needs *something* to send back as a tool_result
    no matter what happens, so failures are converted to descriptive strings
    instead of exceptions.
    """
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; IntelAgent/1.0)"},
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return f"Error: request to {url} timed out after 10 seconds."
    except requests.exceptions.ConnectionError:
        return f"Error: could not connect to {url}. Check the URL is correct and reachable."
    except requests.exceptions.HTTPError:
        return f"Error: {url} returned HTTP {response.status_code}."
    except requests.exceptions.RequestException as exc:
        return f"Error: failed to fetch {url} ({exc})."

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = " ".join(soup.get_text(separator=" ").split())
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "... [truncated]"

    return text or f"Error: fetched {url} but found no readable text content."

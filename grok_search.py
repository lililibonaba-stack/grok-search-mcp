import os

import httpx
from fastmcp import FastMCP

mcp = FastMCP("grok-search")

API_URL = "https://cheapapis.net/v1/chat/completions"


@mcp.tool
def search_by_grok(query: str) -> str:
    """Search the web via the grok-4.5-search model and return the findings as text.

    Args:
        query: The search query text (what to look up on the web).
    """
    api_key = os.environ.get("CHEAPAPIS_API_KEY")
    if not api_key:
        return "Error: CHEAPAPIS_API_KEY is not set."

    try:
        resp = httpx.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "grok-4.5-search",
                "messages": [{"role": "user", "content": query}],
            },
            timeout=180,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code}: {e.response.text[:500]}"
    except (KeyError, IndexError):
        return f"Unexpected response structure: {str(data)[:500]}"
    except Exception as e:
        return f"Search failed: {e}"


if __name__ == "__main__":
    mcp.run()

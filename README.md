# grok-search-mcp

A minimal [MCP](https://modelcontextprotocol.io) server that exposes a single web-search tool, `search_by_grok`, backed by the `grok-4.5-search` model through an OpenAI-compatible chat completions endpoint.

## How it works

- Tool name: `search_by_grok`
- Input: `query` (string, required) — what to look up on the web
- Output: the search findings as plain text (with source links when the model provides them)

The server reads your API key from the `CHEAPAPIS_API_KEY` environment variable. The key is **never** stored in this repository.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed and available on your PATH (`uv --version` to verify)
- An API key for [cheapapis.net](https://cheapapis.net) (or any OpenAI-compatible endpoint that serves `grok-4.5-search`, if you edit `API_URL` in the script). For how to create one, see [get_apikey_tutorial.md](get_apikey_tutorial.md).

## Configuration

> [!IMPORTANT]
> Clone or download this repository first, then replace the placeholder script path (`C:/path/to/grok-search-mcp/grok_search.py` on Windows, `/path/to/grok-search-mcp/grok_search.py` on macOS/Linux) in the configs below with the actual full path to `grok_search.py` on your machine.

### Kilo (`kilo.json` / `kilo.jsonc`)

Add to the top-level object (global `~/.config/kilo/kilo.jsonc` or project `kilo.json`):

```jsonc
{
  "mcp": {
    "grok-search": {
      "type": "local",
      "command": [
        "uv",
        "run",
        "--with", "fastmcp==4.0.2",
        "--with", "httpx==0.28.1",
        "python",
        "C:/path/to/grok-search-mcp/grok_search.py"
      ],
      "environment": {
        "CHEAPAPIS_API_KEY": "apikey_XXXXXXXXXXXXXX"
      },
      "enabled": true,
      "timeout": 200000
    }
  }
}
```

Optionally auto-approve the tool in the same file:

```jsonc
{
  "permission": {
    "grok-search_search_by_grok": "allow"
  }
}
```

### Claude Desktop / Cursor (`mcpServers` format)

```json
{
  "mcpServers": {
    "grok-search": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp==4.0.2",
        "--with", "httpx==0.28.1",
        "python",
        "/path/to/grok-search-mcp/grok_search.py"
      ],
      "env": {
        "CHEAPAPIS_API_KEY": "apikey_XXXXXXXXXXXXXX"
      }
    }
  }
}
```

## Security notes

- Put your API key only in the client's `environment`/`env` block or a system environment variable. Never commit it to git.
- Search requests are sent to the configured endpoint together with your key; use an endpoint you trust.
- The default HTTP timeout is 180 seconds because search-style models can be slow to respond.

## License

MIT

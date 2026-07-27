# CLAUDE.md

## What this is

A minimal single-tool agent built directly on the raw Anthropic Messages API
(no framework) to demonstrate the core agentic action loop: model call ->
`stop_reason` inspection -> tool execution -> result fed back -> repeat.

It's framed as a **competitive intelligence** tool, not a generic summarizer:
given a URL (competitor announcement, press release, product/pricing page),
it fetches the page and writes a structured analyst brief (What happened /
Why it matters / Watch for) rather than an even-handed summary.

## File structure

- `agent.py` -- the agent loop (`run_agent`), the system prompt, and the CLI
  entry point (`uv run agent.py "<prompt>"`).
- `tools.py` -- the `FETCH_URL_TOOL` schema and the `fetch_url()`
  implementation (`requests` + `BeautifulSoup`).
- `pyproject.toml` / `uv.lock` -- dependencies, managed via `uv`.

## Conventions to keep consistent

- **One tool, one pattern.** New tools go in `tools.py` following the
  `fetch_url` shape: the function must never raise -- every failure path
  returns a descriptive string, because the loop always needs *something* to
  send back as a `tool_result`.
- **Framing lives in two places.** The competitive-intel angle is stated in
  both the tool's `description` (soft-steers *when* the model calls it) and
  the system prompt (steers *how* it writes about what it found). Keep both
  in sync if the framing changes -- one alone is weaker steering than both.
- **No framework, on purpose.** This repo intentionally hand-writes the
  `while True` / `stop_reason` loop instead of using LangChain or the Tool
  Runner, so the mechanics stay visible for learning. Don't introduce an
  abstraction layer without discussing why first.
- **Stay lean.** This is a learning artifact (agent #1 of 50), not a
  production service -- keep it small rather than adding retries, config
  layers, or multi-tool generality it doesn't need yet.

## Running it

```
uv run agent.py "Summarize https://example.com/some-announcement"
```

Requires `ANTHROPIC_API_KEY` set in the environment.

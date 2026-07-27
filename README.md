# Competitive Intel Summarizer

**Agent #1 of 50** in the [50-agents-50-days hub](<hub-repo-url>) -- a series of small,
self-contained agents built to learn agentic AI architecture one concept at a time.

## What it does

Give it a URL -- a competitor's press release, blog post, or pricing page -- and it
fetches the page and returns a short analyst brief: **what happened**, **why it
matters competitively**, and **what to watch for next**. Not a generic summary: the
agent is explicitly framed as a competitive intelligence analyst, so it prioritizes
strategic signal over even-handed compression.

## Business value

Turns a ~10-15 minute manual read-and-digest of a competitor announcement into a
~30-second structured brief -- a rough 90%+ reduction in the time it takes an analyst
or product team to triage a single piece of competitor news.

## What this explores

**Tool use / function calling** -- the foundational agentic pattern where a model can't
act on its own, so it emits a structured request ("call this tool with these
arguments"), your code executes it for real, and the result is fed back into the
conversation for the model to act on. This repo implements that loop by hand against
the raw Anthropic Messages API (no agent framework), with a single tool
(`fetch_url`), specifically to make the mechanics -- `stop_reason`, `tool_use` /
`tool_result` blocks, the growing message history -- visible rather than hidden
behind a library.

## CCA-F mapping

**Domain 1: Agentic Architecture -- single-agent tool-use loop.** This repo is the
minimal instance of that pattern: one model, one tool, a hand-written loop that
branches on `stop_reason` to decide whether to execute a tool or return a final
answer. It's the building block that every more complex agentic architecture (multi-tool,
multi-agent, orchestrated) is assembled from.

## Running it

```bash
uv sync
export ANTHROPIC_API_KEY=your-key-here
uv run agent.py "Summarize https://example.com/some-announcement"
```

## Structure

See [CLAUDE.md](CLAUDE.md) for file layout and conventions.

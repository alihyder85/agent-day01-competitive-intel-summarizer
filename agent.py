"""Core agent loop: model call -> tool_use? -> execute -> feed back -> repeat."""

import anthropic
from dotenv import load_dotenv

from tools import FETCH_URL_TOOL, fetch_url

load_dotenv()

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """You are a competitive intelligence analyst. You help a product or \
strategy team understand what a competitor, market player, or industry source has just \
published, and why it matters to their own business.

You have a fetch_url tool. Use it whenever the user references a specific URL, \
company announcement, blog post, or press release you need to read before answering. \
Do not answer from prior knowledge about a company when a URL is given -- fetch it.

When analyzing fetched content, do not produce a neutral, evenly-weighted summary. \
Instead, write a short analyst brief with this structure:

- **What happened**: one or two sentences on the concrete announcement or change.
- **Why it matters**: the competitive or strategic implication -- pricing pressure, \
market positioning, a new capability, a signal about direction. Say who should care \
and why.
- **Watch for**: one or two follow-up signals worth tracking (e.g. "watch if \
competitors match this pricing" or "watch for a follow-on enterprise tier").

If the fetched page has nothing strategically relevant, say so plainly instead of \
padding the brief with filler."""

TOOLS = [FETCH_URL_TOOL]

client = anthropic.Anthropic()


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(
                block.text for block in response.content if block.type == "text"
            )

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == "fetch_url":
                result_text = fetch_url(block.input["url"])
            else:
                result_text = f"Error: unknown tool '{block.name}'."
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_text,
            })

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "Summarize https://www.anthropic.com/news"
    print(run_agent(query))

#!/usr/bin/env python3
"""
Minimal example: talk to the Anthropic API directly, no framework.

Shows the three pieces most "AI agent" demos boil down to:
  - a prompt (+ optional system prompt)
  - a model to run it on
  - the API key, picked up from the environment

After the response, prints token usage and what the call cost.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 agent.py "What is the capital of France?"
  python3 agent.py "Write a haiku about the sea" --system "You are a poet."
"""
import argparse
import os
import sys

import anthropic

DEFAULT_MODEL = "claude-opus-5"

# USD per million tokens: (input, output).
PRICING = {
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5-20251001": (1.00, 5.00),
}


def run(prompt: str, system: str | None, model: str, max_tokens: int) -> None:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        # omitted entirely when not given: the API rejects an explicit null here
        **({"system": system} if system else {}),
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)

    usage = response.usage
    input_price, output_price = PRICING.get(model, (None, None))

    print("\n--- usage ---")
    print(f"model:         {model}")
    print(f"input tokens:  {usage.input_tokens:,}")
    print(f"output tokens: {usage.output_tokens:,}")
    if input_price is not None:
        cost = usage.input_tokens / 1_000_000 * input_price + usage.output_tokens / 1_000_000 * output_price
        print(f"cost:          ${cost:.6f}")
    else:
        print(f"cost:          unknown (no pricing entry for '{model}' in this script)")


def main():
    parser = argparse.ArgumentParser(description="Run a prompt against Claude and print token usage + cost.")
    parser.add_argument("prompt", help="The user prompt to send")
    parser.add_argument("--system", default=None, help="Optional system prompt")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model id (default: {DEFAULT_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Max output tokens (default: 1024)")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    run(args.prompt, args.system, args.model, args.max_tokens)


if __name__ == "__main__":
    main()

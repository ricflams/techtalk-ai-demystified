# my-agent

The smallest possible illustration of "talking to an AI service": one Python
file, one API call, no framework, no agent SDK. It shows what most demo
"agents" actually are underneath — a prompt, a couple of settings, and an API
key read from the environment.

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
python3 agent.py "What is the capital of France?"

python3 agent.py "Write a haiku about the sea" --system "You are a poet."

python3 agent.py "Explain recursion to a 10 year old" --model claude-haiku-4-5-20251001 --max-tokens 300
```

Every run prints the response, then the token usage and cost of that one call:

```
Paris.

--- usage ---
model:         claude-opus-5
input tokens:  13
output tokens: 6
cost:          $0.000215
```

## Notes

- The API key is never in the code — `anthropic.Anthropic()` picks up
  `ANTHROPIC_API_KEY` from the environment automatically.
- `--system` is the one "standard" knob almost every LLM call exposes beyond
  the prompt itself: it shapes the assistant's role/behavior for the whole
  request.
- No `temperature` flag: on Claude Opus 5, Sonnet 5, and Opus 4.7+,
  `temperature`/`top_p`/`top_k` are rejected outright with a 400 error —
  steering happens through prompting instead of sampling params on these
  models.
- Cost is computed from published per-model $/million-token pricing — see
  `PRICING` in `agent.py`. Add an entry there for any other model you pass via
  `--model`.

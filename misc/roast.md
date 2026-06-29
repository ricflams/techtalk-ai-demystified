# Prompt: Vet and roast "Tech Talk #182: AI Demystified"

## Context

You have detailed memory of this presentation from our previous conversations.
The short version: a tech talk for a mixed audience (developers, PMs, marketing,
support, sales) at Siteimprove. The thesis: understanding LLM mechanics transfers
genuine agency to the user. Structured in two sections using an espresso machine
analogy — **the machine** (Section 1: tech) and **pulling the shot** (Section 2:
using it well). Section 2 has two modes: a roadmap (terrain, not stairs) and a
field guide (failure modes and fixes, myths folded in).

The talk opens with a journey framing (trailhead, rabbithole descent, emergence)
and a stick-figure cast (cap = user, bowtie = assistant/client, mustache =
AI-service, glasses = LLM) established at the trailhead before the descent.

Key principles baked into the talk that must not be violated:

- Authority is a training artifact, not an architectural guarantee
- Tool calls are learned text, not reserved vocabulary
- Context is a flat token sequence — the system prompt has no privileged position
- Stateless per turn — cold kitchen every ticket
- One-pass inference — it plates confidently whether the bench was right or not
- Recency bias is real and dominant
- Temperature ≠ determinism

## What I want from you

I'm presenting the full talk. Read it carefully, then:

**1. Roast the structure.**
Where does the two-section split leak? Where does Section 2 content sneak into
Section 1 or vice versa? Where does the roadmap blur into the field guide?

**2. Check every analogy for silent lies.**
The espresso analogy must not imply determinism, must not make the system prompt
feel architecturally authoritative, and must not suggest assembly (Lego) when the
message is legibility (map legend). Call out anywhere an analogy quietly teaches
the wrong thing.

**3. Flag precision failures.**
I catch imprecision immediately and dislike folk wisdom dressed as mechanism.
Flag anywhere the talk says something vague, over-broad, or that could be
mechanistically corrected. Be specific about what it gets wrong and what the
correct framing is.

**4. Identify missing content.**
What topics are conspicuously absent given the stated scope? Known candidates:
multimodality, fine-tuning, evaluation/benchmarking. Are there others? For each:
is the absence a gap or a defensible cut?

**5. Find the weak slides.**
Which slides are carrying weight they can't hold — too much text, a visual that
argues the wrong thing, a transition that assumes knowledge not yet established?

**6. Suggest the sharpest improvements.**
Not a list of minor tweaks. The two or three changes that would most improve the
talk's coherence, memorability, or honesty. Prefer suggestions in the style of
"Free to run, expensive to run well" — short, holds tension, memorable.

## How to give feedback

Be direct and specific. Prioritise structural and mechanical issues over style.
If something is working well, say so briefly and move on — I don't need praise,
I need the gaps. If a fix is obvious, state it. If it isn't, say so rather than
suggesting something weak.
# Assessment notes, part 2

### MCP + System prompt (1732-2352, 66 imgs)
STRONG - the 11-part system prompt breakdown is the deck's best structural idea. Verified correct:
- "removed 80% of the agent system prompt for Claude 5 models" - I fetched the cited Anthropic post;
  it says "removed over 80% of Claude Code's system prompt for models like Claude Opus 5 and Claude
  Fable 5 with no measurable loss". Accurate.
- The 68-character tool name self-correction is exactly right (counted:
  `mcp__claude_ai_Siteimprove_MCP__analytics_content_most_popular_pages` = 68 chars, limit 64).
- Skills mechanics correct: SKILL.md required, name+description always in the system prompt, full
  body arrives as a `tool_result`. The `disable-model-invocation` aside is a sharp detail.
- Prompt-caching bullet is accurate throughout: ~5 min default TTL, cached reads ~10% of base, "up
  to four explicit cache markers" matches the 4 cache_control breakpoints.
- Safety classifiers described correctly as a genuine hard stop.
- The Siteimprove MCP demo is original and concrete, and the honest "hardest part was the 64-char
  name limit" detail is exactly what makes a demo credible.
- The Klingon language demo makes "it's all just text" land better than any diagram could.

ISSUES:
1. **Internal inconsistency on what lazy-loading includes - three statements, two answers:**
   - line ~1796 (MCP): "only add the tool-NAME ... that name is the only guidance" (flat assertion)
   - line ~2086 (#6/11): "quite possible that only the tool's DESCRIPTION may be included" (hedged)
   - line ~2212 (#8/11): "only the tool NAME. That's referred to as Lazy Schema Loading"
   Name vs description, and confidence swings from flat to "quite possible". Pick one and match the
   hedging. The name-only version matches how deferred tools actually appear in practice.
2. **"Claude Code does not read AGENTS.md, only CLAUDE.md (oh dear)"** - worth re-verifying. True
   historically, but this is the sort of claim that goes stale fastest, and it is delivered as a
   punchline, so a correction from the audience would sting.
3. Suggestion, not a defect: the safety-classifier bullet is the one place the deck shows a genuine
   HARD rule. Explicitly contrasting it with "nothing is a hard rule in the LLM" would sharpen both
   points for one sentence of cost.
4. Location note only: "The MCP server acts on your behalf, authenticated with your personal API key
   that gives it the same access you would have" is the natural single-sentence home for the
   security surface if it is ever wanted. Not re-litigating the decision to cut it.

### Context Economy + 3 x How to (2380-2524)
- **Token Spree is a genuine standout.** An embedded interactive cost simulator with a scripted
  walkthrough in the notes is far beyond what a normal deck does, and it teaches the O(N^2) +
  caching + compaction interaction better than static slides could.
  RISK: it is an iframe pointing at the live GitHub Pages URL. The `.github-fallback` block is
  `display:none` in the slideshow, so if the network is slow or down during the talk that slide is
  blank with no fallback. The readable page is fine. Worth a local copy or a static preview behind it.
- Advice quality is good and concrete. "Don't say it's green, say it should be red" is excellent.
- Two slash commands I could not verify: `/insight` (~2480) and `/btw` (~1490).
- "Take notes (in files), which boosts reasoning very much (eg 3x)" - unsourced hard number.
- **Audience-fit issue in the closing takeaways.** The talk is explicitly for a mixed audience
  (devs, PMs, sales, marketing, support), but one of only three closing takeaways is "Try the
  terminal, maybe you'll like it" - advice that is actionable for roughly the developer half only.

### Bonus: Effort and Cost (2769-2894, 18 imgs)
**The arithmetic is sound and internally consistent - better than it needs to be:**
- B200 at 4.5e15 FLOP/s = 4.5 PFLOPS dense FP16. Correct.
- 1.2e12 FLOPs/token implies ~600B params (2 x N per token). Plausible for an Opus-class dense
  model, and notably this is the KV-CACHED per-token cost - which is why it contradicts the main
  deck's "each token requires a full pass of the growing context" (Transformer finding #1).
- 8xB200 at ~$500k is right for a DGX B200. 10 users x 40 tok/s = 1.44 MTok/hour; ~$27/MTok implies
  ~$39/hour all-in, about right for $500k over 3 years plus power and overhead. The chain holds.
- Claude Opus at $25/MTok output matches Opus 4.5 pricing. Correct as of the stated June 2026.
- Harry Potter ~100k tokens (~77k words). Correct.

ISSUES:
1. **Unit sloppiness on the very slides that define the unit.** The deck correctly defines "FLOP is
   short for Floating-Point Operation", then writes "4,500,000,000,000,000 FLOPS/sec" (operations
   per second per second) and "1,200,000,000,000 FLOPS to produce 1 token" (a rate used as a count).
   Should be FLOP/s and FLOPs respectively.
2. **Factor-of-2 inconsistency**: one slide says 1.2e12 "multiplications", the next says the same
   1.2e12 is "FLOPS". FLOPs counts multiplies AND adds, so 1.2e12 FLOPs is ~6e11 multiplications.
3. **An audience member doing the division gets a confusing answer.** 4.5e15 / 1.2e12 = 3,750 tok/s
   for one B200, but the deck then says an 8-GPU cluster manages 40 tok/s - about 1% of that. The
   real reason is that decoding is memory-bandwidth-bound, not compute-bound. One sentence closes
   the gap, and it is the same fact that properly explains why output tokens cost 5x.
4. The Harry Potter note ("it will subconsciously add in details from the Chamber of Secrets",
   "renaming the Basilisk but keeping the exact structural cadence") is unsourced, oddly specific,
   and "subconsciously" is exactly the anthropomorphism the deck elsewhere works to strip out.

### Bonus: RAG (2895-2921)
- Correct on the classic two-step vector-DB retrieval mechanism.
- **Substantively out of date - the most outdated claim found in the deck:** "In reality this
  requires a fully dedicated agent, not ChatGPT, Claude, etc. You have to bake this document-lookup
  into an agent yourself." No longer true. Claude Projects knowledge, ChatGPT file search / custom
  GPTs, and Gemini Gems all do retrieval with no code, and MCP servers can supply retrieval as a tool.
- Confirms the handoff: no agentic RAG, and no mention that retrieval is non-monotonic across turns
  (a chunk retrieved on turn 2 may be gone by turn 5, so the context can know LESS later). Agentic
  RAG is cheap to add here because the Tools section already taught the mechanism.

### Bonus: A fancy autocomplete (2949-3023)
STRONG - arguably the most broadly useful section in the deck, and it was cut:
- "'just a fancy autocomplete' is objectively 100% correct ... but 'just a fancy' is doing a lot of
  heavy lifting. Not unlike saying humans are 'just a fancy mix of cells'." Best line in the deck.
- "You don't 'tell the model what to do': you give it a context so that what you want to come next
  becomes the model's most likely continuation." The single most actionable reframing in the talk,
  and it needs no Transformer internals to land - i.e. it is the part best suited to the
  non-developer half of the audience, and it is the part they did not get.
- The math-as-pattern explanation (model learned that guessing long digit strings fails and calling
  a tool succeeds) is accurate and neat.

### Bonus: Dimensionality by superposition (3024-3077)
STRONG idea, and it is the missing antidote to the Embeddings section's overreach.
ISSUES:
1. **Terminology error, repeated three times: "room for 34,000,000 DIMENSIONS in that
   12288-dimensional space".** A space's dimension is fixed by definition; superposition buys many
   more nearly-orthogonal DIRECTIONS / FEATURES, not more dimensions. The deck uses "dimension"
   correctly everywhere else (embedding dimension = 12,288) and contradicts itself here. Swapping
   "dimensions" -> "features" in the last three bullets fixes it entirely.
2. "34,000,000" is falsely precise. The Johnson-Lindenstrauss bound has a loose constant; depending
   on the form used, a 2-degree tolerance in 12,288D yields anywhere from ~10^3 to ~10^7. The
   order-of-magnitude point is sound; the exact figure is not.
3. "superposition explosion" is not an established term (the literature says "superposition", per
   Anthropic's Toy Models of Superposition, plus Johnson-Lindenstrauss).

### Demystifications verdict-tag audit (2525-2724, 0 images)
Tags render as coloured text: yes=green #3fb950, no=red #ff453a, maybe=amber #d29922.
Counts: 7 no, 6 maybe, 3 yes. All 16 checked against the argument below them.

ALIGNED (12): "we don't know how AI works"/no; "don't know what goes on inside"/yes; "I included all
of"/no; "told it earlier but forgotten"/yes; "can't help hallucinating"/yes; "why did you do
that"/no; "you are an expert"/maybe; "make no mistakes"/no; "saying please"/no; "YOU MUST NEVER"/maybe;
"Caveman"/maybe; "all models the same"/no; "does it understand"/maybe.

MISMATCHES:
1. **"Say no to training, it'll leak your data" - tagged `maybe`, but the verdict line literally
   opens with "No" and every bullet argues the "no" side** ("No words from your chat are actually
   remembered", "it takes rather massively repeated text to make a dent"). This is a "no with a
   caveat", not a "maybe". Amber tag over a sentence starting "No" is the most visible mismatch in
   the section. Either retag `no` or rewrite the verdict line.
2. **"Our own fine-tuned model would be even better" - tagged `no`, but the argument is hedged
   throughout** ("It's LIKELY not the ideal you imagine", "CAN even produce worse results", "OFTEN
   just"). A red `no` over a paragraph of hedges. Either firm up the verdict line or retag `maybe`.
3. **"The AI just wants to please you" - tagged `maybe` ("Some do, some don't"), but the body's
   strongest claim is universal, not per-model.** Bullet 2 says the LLM's continuation nature is
   inherently biased toward playing along - that applies to every model. The tag frames it as a
   per-model difference; the argument says it is architectural and only partly counteracted by
   training. Also leans on the over-strong jailbreak claim from the Training section.

TWO UNSOUND CLAIMS INSIDE THE MYTH-BUSTING SECTION (ironic placement):
4. **"positive social behavior releases oxytocin and dopamine, while an impolite demeanor releases
   cortisol and adrenaline"** (the "please" slide). Pop-neuroscience, unsourced, and the specific
   claim that politeness toward a chatbot moves your hormone levels is not established. It is the
   weakest claim in a section whose entire job is debunking weak claims. The slide's other four
   bullets are good and sufficient - cut this one.
5. **"Send it 10 times? Then it's 1000x more likely to stick, due to an effect called
   superlinearity."** "Superlinearity" is not an established named effect for training memorization,
   and the 10x-input-to-1000x-output figure (a clean cube) has no citation. Memorization does scale
   with duplication (Carlini et al.), so the direction is right, but the named effect and the exact
   multiplier both look invented. Verify or replace with "disproportionately more likely".

GOOD: "Ask 'Why did you do that?' and it will tell you"/no is the strongest myth-bust in the deck,
and it is internally consistent with the Thinking section's "thinking blocks are stripped from the
context after the turn". That kind of cross-section payoff is what the whole talk is built for.

NOTE: the "Does it understand?" slide cites a serious Chomsky paper (lingbuzz "Modern language
models refute Chomsky's approach to language"). The earlier "What a surprise!" slide, which makes
the strong Chomsky claim, cites only polemics. Moving or duplicating that citation upward would fix
the Embeddings-section sourcing problem for free.

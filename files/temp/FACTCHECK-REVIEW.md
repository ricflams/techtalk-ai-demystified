# AI Demystified — Fact-check review

**Scope:** `src/slides.md` (3,033 lines / 369 slides), reviewed 2026-08-20.
**Question asked:** *are there outright false claims, or misleading statements?* Nothing else — no style, wording, or typo notes except where a typo changes a fact.

**Method:** six independent reviewers over six line-ranges, each verifying numbers, names, dates and research claims against live sources (tokenizer claims were checked empirically with `tiktoken`), plus one full read-through for cross-slide contradictions.

**Note:** speaker notes (`####`) are included — they're part of the talk and they render as body text on the readable page.

---

## How to use this

Findings are in four tiers. **Tier A is the only one you must do before presenting.** If you have 20 minutes, do Tier A and stop.

| Tier | What it is | Count | Time |
|---|---|---|---|
| **A** | Wrong *and* load-bearing — breaks the mental model the deck teaches, or debunks something that's actually true | 12 | ~30 min |
| **B** | Wrong in a specific detail — a name, number or date. Fast, surgical edits | 14 | ~20 min |
| **C** | True but overstated — needs a hedge word, not a rewrite | 17 | ~25 min |
| **D** | Cross-slide contradictions — the deck disagrees with itself | 6 | ~15 min |

Also see **[Verified correct](#verified-correct--dont-touch-these)** at the end — a lot of the deck checked out, including several things that *look* shaky. Don't waste time re-checking those.

---

## Tier A — wrong and load-bearing

### A1. "Lost in the middle" — the debunk points the wrong way
**Line 2841–2845** · *Context is "Lost in the middle"* · **FALSE** · Confidence: High

> `<p class="verdict maybe">Not really, but positioning matters</p>`
> "The LLM does not systemically 'pay less attention to the middle of the context'"

**Recalibrated on re-check — an earlier draft of this report overstated this finding.**

What is confirmed: needles at **30–70% depth show a 5–15 point retrieval drop** (RULER, verified from independent sources); positional bias is still listed as its own mechanical failure mode in 2026 long-context analyses, distinct from length-driven decay; and no production model has eliminated it.

What the earlier draft glossed over: frontier models now score near-perfectly on simple needle-in-a-haystack, so on *easy retrieval* the middle penalty really is small. The effect shows up on harder tasks and at longer contexts. The draft also leaned on NoLiMa, which mainly demonstrates **length** degradation rather than **position** degradation — related but different claims, and it ran them together.

**Net:** the verdict line *"Not really, but positioning matters"* is broadly defensible, and the second bullet (keep facts near where they're used) is good advice. The wrong part is the **first bullet's mechanism claim** — position bias *is* systemic, it's a property of causal attention, and it's measurable on any model you like.

Same shape as A2: right practical conclusion, wrong mechanism claim.

- [ ] **Fix (minimal):** change only the first bullet → *"The effect is real but much smaller than it used to be — frontier models handle simple retrieval fine. It bites on harder tasks and longer contexts."* Keep the verdict and the second bullet as they are.

---

### A2. "Say no to training" — the verdict is right, the *reason* is wrong
**Line 2936–2940** · **VERDICT CORRECT / MECHANISM WRONG** · Confidence: High

> `<p class="verdict no">No, it absolutely won't</p>`
> "*Nothing concrete from your chat is ever actually remembered*" … "never retrievable or associated with you"

**Revised after review — an earlier draft of this report got this wrong.** It claimed rare unique strings are "the most memorisable." That conflates two different things called memorization: Feldman-style **influence** memorization (rare examples shape predictions, because long-tailed distributions can't be fit by generalization alone) versus **extractable** memorization (an adversary can construct a prompt that makes the model emit the string). The first does not imply the second.

The decisive evidence is [Kandpal, Wallace & Raffel, ICML 2022](https://arxiv.org/abs/2202.06539): regeneration rate is **superlinearly** related to duplication count — a sequence present 10 times is generated ~**1,000x** more often than one present once — and **existing methods for detecting memorized sequences have near-chance accuracy on non-duplicated training sequences.** Not "hard to extract" — near-chance to even *detect*, with white-box advantages a real attacker doesn't have.

So: a genuine one-off string in a pretraining corpus is **not meaningfully retrievable**, and your "no" is correct. Carlini 2021 doesn't contradict this — GPT-2 at 1.5B on a pre-deduplication corpus, and what came out was overwhelmingly high-duplication boilerplate. Same story for the Nasr 2023 divergence attack at scale. Scale doesn't rescue singleton extraction. [Extractable Memorization From First Principles](https://arxiv.org/html/2607.12649v1) (2026) cuts the same way: ~24% of apparent short-sequence extraction turns out to be false positives from general predictability.

**So why touch the slide at all?** Because the stated reason — *"a drop in the ocean of weight-adjustments"* — is the wrong mechanism, and a technical audience member can poke it. The right reason is **duplication count**. Two things sharpen it:

- **Mosaic memory** — [Nature Communications, Jan 2026](https://www.nature.com/articles/s41467-026-68603-0). Fuzzy duplicates (tokens missing, replaced, shuffled) contribute **up to 0.8 of an exact duplicate**; memorization is syntactic, not semantic; and the paper explicitly "questions the effectiveness of exact data deduplication as a privacy protection technique." This widens the one realistic path: not "the same config pasted 30 times" but "a **similar** config pasted 30 times" — ordinary team behaviour, and exact dedup doesn't catch it.
- **Multi-epoch training is now standard**, weakening the 2022-era "single epoch over a deduplicated corpus" premise that the singleton-safety argument leans on.

Neither rescues "unique string → extractable." Both mean **"never"** and **"absolutely"** are one notch stronger than the evidence supports.

Separately, the slide misses the exposure that isn't about weights at all: on Anthropic consumer plans, opting *in* changes retention from **30 days to 5 years**, plus human review of flagged conversations and subprocessor exposure. That's the actual reason enterprises opt out, it's a completely different mechanism, and separating it lets you keep a clean "no" on the leak question.

- [ ] **Fix:** keep the `no` verdict. Replace the mechanism bullet with: *"Memorization scales with **duplication** — a string seen 10 times is ~1000x more likely to resurface than one seen once, and for genuine one-offs, detection is near chance. Your one-off is a one-off."*
- [ ] Soften the absolutes: *"never retrievable"* → *"not realistically retrievable"*.
- [ ] Add the thin-but-real caveat: *"The exception is repetition — if a team pastes the same (or a similar) internal config into thirty conversations, that's no longer a one-off."*
- [ ] Add a separate bullet: *"The real reason to opt out isn't the weights — it's retention: 5 years instead of 30 days on consumer plans, plus human review of flagged chats. API/enterprise tiers don't train on your data by default."*

---

### A3. Next-token selection is a dot product, not cosine similarity
**Line 701** · *Find next token by similarity-comparison* · **FALSE** · Confidence: High

> "Also known as \"cosine similarity\""

The final hidden state is multiplied by the unembedding matrix — a plain **dot product** against every vocabulary vector, then softmax. It is deliberately *not* cosine similarity: the vectors aren't length-normalised, and magnitude carries real information (it's much of how the model expresses confidence). Naming it cosine similarity gives the wrong mental model of what a logit is — and the deck uses "cosine similarity" correctly elsewhere (line 1542, embedding search), so this actively muddles two different operations.

- [ ] **Fix:** → *"Technically a dot product against every token's vector — 'how much does this point in that token's direction?'"*

---

### A4. "Same text, same token — always" is false, and the slide behind it proves it
**Lines 283, 285** · *I fart poetry* / *Same text, same token - always* · **FALSE** · Confidence: High

Verified with `tiktoken` (o200k_base):
- `" fart"` = one token (121583), but `"fart"` with no leading space = `f` + `art`
- the sign's own `"I FART"` = `I` + `" F"` + `"ART"` — three tokens, **none of them "fart"**
- `"present"` = 47421, but inside `"presentation"` it's a *different* single token (96140), and `" present"` is 3333
- your own Flamsholt slide depends on this: 97957 is `" Flam"` **with the space**; bare `"Flam"` is `Fl` + `am`

Tokenisation is deterministic for a given *full string*, not for a given substring.

- [ ] **Fix:** retitle to *"Same text **in the same shape**, same token"*. Note → *"All the meanings of `present` share one token — but `present`, ` present` and `presentation` are three different tokens. Spacing and casing decide the split."*

---

### A5. "Each token is generated completely independently" / "no planning"
**Line 742** · *Yes, tokens are really generated one by one* · **FALSE** · Confidence: High

> "Each token really is generated completely independently… There's no planning of emitting an itemized list… without any overall grand design or planning."

Two errors. Tokens are **not** independent — each is conditioned on the entire preceding context, which is the point of the preceding 40 slides. And Anthropic's own interpretability work (*On the Biology of a Large Language Model*, 2025) showed Claude **does** plan ahead: it selects a rhyme target before writing the line leading to it, and rewrites the line when researchers edit that internal plan.

This is exactly the sort of claim a technically-literate audience calls out.

- [ ] **Fix:** *"Each token is emitted one at a time, conditioned on everything before it. It looks like there's a plan — and interpretability research shows the model does form internal targets several tokens ahead — but there's no separate planning stage: it's all the same one-token-at-a-time machinery."*

---

### A6. Static input embeddings don't hold sentence meaning
**Lines 430–432** · *The example's embeddings* · **FALSE** · Confidence: High

> "Each of these lists of 12288 numbers represent the *core meaning* of that single token. … this set of numbers essentially represents the full meaning of the entire sentence."

At this stage these are the *static* input embeddings looked up from the vocabulary table. They are context-free and order-free — the same vectors appear for the words in any order, and `present` (gift) and `present` (attend) get the identical vector. Sentence meaning isn't there yet; attention builds it across the layers.

This is the single biggest wrong-mental-model risk in the embeddings section, and it directly contradicts the "present has many meanings" slide 30 lines earlier.

- [ ] **Fix:** *"…represent the **context-free** meaning of that single token — the dictionary entry, not the reading. At this point `present` the gift and `present` the verb still have the exact same vector, and word order isn't encoded at all. Making these vectors context-aware is exactly what the rest of the LLM does — that's the next section."*

---

### A7. The FLOPs number is off by ~4 orders of magnitude for what the slide describes
**Lines 785–794** · *100,000 context tokens in, 1 token out* → *about 1,200,000,000,000 multiplications* · **MISLEADING** · Confidence: High

~1.2e12 is roughly the *decode* cost of one token once the context is already processed. But the slide's framing is "feed in Harry Potter, get one token out" — that requires **prefill** of all 100,000 tokens first: ~100,000 × 3.5e11 ≈ **3.5e16 FLOPs**. As written, the audience concludes that ingesting a whole novel costs about one teraflop.

- [ ] **Fix:** split the claim — *"Reading the 100,000 tokens in: ~35,000,000,000,000,000 FLOPs (once). Then each further token out: ~1,200,000,000,000 FLOPs."*

---

### A8. "ultrathink is a myth now" — it came back
**Line 1786** · *Ancient history: writing "ultrathink" is a myth now* · **FALSE as of today** · Confidence: High

The keyword was deprecated in the Nov 2025 / Jan 2026 builds, but Anthropic **re-introduced `ultrathink` in Claude Code v2.1.68** after user pushback. It now sets high effort for that one turn, then resets to your default. Presenting it as dead will be contradicted by someone in the room who uses it daily.

- [ ] **Fix:** retitle *"'ultrathink': dead, then resurrected"*. Note → *"The old think / think harder / ultrathink ladder was removed when thinking went automatic. But `ultrathink` came back: today it means 'high effort, this turn only'."*

---

### A9. Lazy tool-loading works the opposite way to what the deck says
**Lines 2028–2032** and **2463–2471** · **FALSE** · Confidence: High

> "the modern behavior is actually to **only add the tool-name** … and that name is **the only guidance** the LLM will get about that tool"

**RETRACTED — the deck is right and this report was wrong.** An earlier draft claimed deferred tools are excluded from context entirely, "not even their names." That is false for the shipping implementation. Deferred tools **are** listed by name in the system prompt, exactly as the deck says — the observed format is:

```
<availableDeferredTools>
Available deferred tools (must be loaded with tool_search_tool_regex before use):
await_terminal
configure_notebook
...
```

Names only, no descriptions. So *"only add the tool-name"* is accurate, and the practical advice that follows — **pick descriptive tool names** — is correct, because the name is what the model sees and what it decides to search on. The 64-character limit cited on L2073 is also right.

**What survives — a hedge only, not a correction:** deferral isn't unconditional. Claude Code loads full schemas up front until the deferrable definitions cross a size threshold (~10% of the context window); on the API it's opt-in per tool. So "typically" is doing real work in that sentence and is fine as written.

- [ ] **Optional hedge:** add *"— once you have enough of them to be worth deferring"* to the "Modern lazy-load" slide. Nothing else needs changing.
- [ ] **Still do D1:** L2325 (*"only the tool's **description**"*) contradicts L2467 (*"only the tool **name**"*). **L2467 is the correct one** — align L2325 to it.

---

### A10. MCP is bidirectional
**Line 2002** · *An MCP server is "just" a middleman* · **FALSE** · Confidence: High

> "The *agent or server always call the MCP server*, never the other way around."

MCP is JSON-RPC and explicitly bidirectional. Servers initiate requests to the client: **sampling** (`sampling/createMessage` — the server asks the *client's* LLM for a completion), **elicitation** (the server asks the *user* a structured question mid-tool-call), plus `roots` and `tools/list_changed` notifications.

- [ ] **Fix:** *"The agent or server normally calls the MCP server — though the protocol also lets a server call back to ask the user a question, or even borrow your LLM."* (Or delete the bullet if the callback direction is out of scope.)

---

### A11. Behaviour differences come from post-training, not pre-training
**Line 1233** · *Trained AI model recap* · **FALSE** · Confidence: High

> "The models have been *pre-trained differently* for different desired behaviors"

Behavioural differences (tone, refusals, personality) come almost entirely from **post-training** — SFT and RLHF/RLAIF. Pre-training is next-token prediction on a corpus; it is not where desired behaviour is installed. The deck gets this **right** in its own Training section (lines 924–926, 1008–1033), so this recap bullet contradicts it.

- [ ] **Fix:** *"The models are **post-trained** differently (RLHF) for different desired behaviours"*

---

### A12. "Gemini — no public training guidelines" is contradicted by the slide's own screenshot
**Lines 1106, 1110, 1121** · **FALSE as stated** · Confidence: High

Google publishes Gemini app safety and policy guidelines, the Generative AI Prohibited Use Policy, the Frontier Safety Framework (v3, April 2026), the AI Principles, and per-model cards. What Google does *not* publish is a single detailed **behaviour spec** comparable to the OpenAI Model Spec or Claude's Constitution.

The slide's own image is `gemini-ai-principles.png` — Google's published AI Principles. You'd be on screen showing the thing you're saying doesn't exist.

- [ ] **Fix:** title → *"Gemini — principles and policies, but no full behaviour spec"*. Note → *"Google publishes AI Principles, safety policy guidelines and a Frontier Safety Framework — but nothing as detailed as a Model Spec or a Constitution."* Line 1121 → *"…but the detailed rules stay internal"*.

---

## Tier B — wrong in a specific detail

Fast, surgical. Each is a name, number or date.

- [ ] **B1 · Line 1321** — *"Google antigravity, in the terminal/CLI"* → **Antigravity is an agent-first IDE** (a VS Code–derived editor), not a CLI. Google's CLI is *Gemini CLI*. The note at 1325 ("CLI means Command Line Interface") cements the error. **FALSE.**
- [ ] **B2 · Line 1306** — *"gemini.com"* → **that's the Gemini cryptocurrency exchange.** Google's is `gemini.google.com`. **FALSE.**
- [ ] **B3 · Line 1776** — *"A **rhyming format** such as a Haiku"* → **a haiku has no rhyme requirement**; it's 5-7-5 *syllables*. The real difficulty (counting syllables under next-token generation) is exactly your point, so fixing it strengthens the slide. **FALSE.**
- [ ] **B4 · Line 794** — *"FLOP … a multiplication of two numbers"* → a FLOP is **any** floating-point op; additions count. Matters here because the standard 2·N estimate counts one multiply *and* one add per weight. **FALSE.**
- [ ] **B5 · Line 846** — *"The NVidia B200 GPU comes in clusters of four"* → the standard Blackwell block is the **HGX B200 baseboard with 8 GPUs**. Also ~$500,000 (line 829) is roughly the price of the *8-GPU* system, so the two numbers are internally inconsistent. **FALSE.**
- [ ] **B6 · Line 687** — *"96 times (attention layers/heads)"* → layers and heads are not synonyms. GPT-3 has **96 layers**, each containing **96 heads** — 9,216 heads total. Heads run in parallel within a layer; layers run in sequence. This is the most common beginner confusion about the Transformer, and the slide teaches it. **MISLEADING.**
- [ ] **B7 · Line 419** — *"ChatGPT 3 has 50257 tokens…"* → the numbers are right for **GPT-3** (vocab 50,257, d_model 12,288), but "ChatGPT 3" isn't a product; ChatGPT launched on GPT-3.5, which uses cl100k_base with **100,277** tokens. Since slide 213 is titled "ChatGPT 3.5's token vocabulary", the deck now gives two vocabulary sizes for what sounds like one model. **MISLEADING.**
- [ ] **B8 · Line 556** — `12228` → **`12288`** (every other slide uses 12288). Renders as body text on the readable page. **Typo-as-fact.**
- [ ] **B9 · Line 659** — *"Positional information is **added into** each individual embedding, typically using RoPE"* → that describes the *old* additive positional encoding. RoPE isn't added to the embedding at all; it **rotates the query and key vectors inside each attention layer** — which is why your own parenthetical has to say "in each layer". **MISLEADING.**
- [ ] **B10 · Lines 913–914** — *"Copilot by Microsoft is also an AI Wrapper"* → Microsoft shipped **seven in-house MAI models at Build 2026** (2 June); MAI-Code-1-Flash is already default in GitHub Copilot for individual VS Code users. Perplexity likewise trains its own Sonar models. **OUTDATED/FALSE.**
- [ ] **B11 · Line 2437** — *"They are called 'plugins'"* → **ChatGPT calls them Skills.** Since OpenAI migrated the app directory to the plugin directory (9 July 2026), a *plugin* is the distribution package that can bundle skills, apps and templates. Skills are *found in* the plugin directory; they aren't called plugins. (Worth a beat: today's "plugins" share nothing but the name with the 2023 ones, shut down April 2024.) **FALSE.**
- [ ] **B12 · Line 2405** — `npx skills add <repo-name>` → the Vercel Labs CLI needs **`<owner>/<repo>`** (`npx skills add backnotprop/bro`). **FALSE.**
- [ ] **B13 · Line 2469** — *"the full name is 'agent-name', then 'mcp server name', then 'tool name'"* → the first segment is the literal string **`mcp`**, not the agent's name (`mcp__<server>__<tool>`). Also SEP-986 caps the *server's* tool name at 64 chars; the composite-name pain is a client constraint. **FALSE.**
- [ ] **B14 · Line 1046** — Scale AI described as *"OpenAI's preferred fine-tuning partner … also worked with Meta, Google DeepMind"* → after Meta took 49% of Scale (June 2025, $14.3B), Google, OpenAI and xAI all pulled back on data-exposure grounds. A year out of date. **OUTDATED.**

---

## Tier C — overstated, needs a hedge

True in spirit, wrong in the specifics. Mostly one-word fixes.

**Myth-busting section (highest risk — a wrong debunk is worse than a wrong explanation):**

- [ ] **C1 · Lines 2969–2972** — *"Mispellings doesn't matter"* / verdict **yes**. Typos measurably degrade output: MIT/IMES 2025 clinical study found ~7% accuracy drop and ~7% of recommendations flipping; Llama 3.1 8B drops 66.7% → 51.0% at a 5% typo rate; GPT-4o mini 82.1% → 74.9%. Smaller on frontier models, but not zero. → verdict `maybe`, *"Models handle typos well, so don't agonise — but studies show measurable drops, so clean prompts are still better."*
- [ ] **C2 · Line 2919** — *"The model doesn't know it's wrong when it hallucinates"* → the conclusion is right, the reason is wrong. OpenAI's *Why Language Models Hallucinate* (2025) argues models **are calibrated** — their probabilities do track correctness — and hallucinate because training and benchmark scoring reward confident guessing over abstention. → *"The model often does have a signal that it's unsure — it just learned that guessing scores better than 'I don't know'. So 'don't hallucinate' changes nothing; make 'I don't know' an acceptable answer instead."*
- [ ] **C3 · Lines 2907–2910** — *"The AI just wants to please you"* / verdict *"Some do, some don't"* → sycophancy is present in **every** frontier model measured, including Claude (Anthropic reports reduced but non-zero MASK sycophantic-dishonesty rates). "Some don't" reads as "some are immune", which nothing supports. → verdict *"Yes — all of them, some less than others"*.
- [ ] **C4 · Lines 2948–2958** — *"Saying 'please'…"*. The **cost** half is fine; the **quality** half isn't. The Penn State study (Oct 2025) found accuracy *rising* from 80.8% (very polite) to 84.8% (very rude) — earlier "politeness helps" results were GPT-3.5-era. And the oxytocin/dopamine-vs-cortisol/adrenaline claim about typing politely at a chatbot has **no study behind it**; a technical audience may call it out. → keep the cost bullets; replace the quality bullet with *"Politeness doesn't reliably improve answers — one 2025 study even found blunt prompts scoring slightly higher. What helps is that 'please…' phrases things as a clear request."* Soften the last bullet to *"…arguably good for the habits you carry into conversations with people."*
- [ ] **C5 · Line 2920** — *"Reasoning Trap"* → the cited paper (arXiv 2510.22977) is specifically about **tool hallucination**, not "detecting nonsense" generally. → *"More reasoning isn't automatically safer: stronger reasoning has been shown to increase made-up tool calls in step with its performance gains."*
- [ ] **C6 · Line 2818** — *"We don't know where or how 'facts' are stored"* → this is one area interpretability *has* made headway on: ROME/MEMIT knowledge editing, circuit tracing, and the J-lens work the slide itself links to. → *"We're only starting to map where and how facts are stored — editing a single fact in the weights is now possible, but the full picture isn't."*
- [ ] **C7 · Line 2893** — *"Recent studies show modern frontier models outperforming fine-tuned models"* → the linked evidence is one domain (clinical). Fine-tuned smaller models still win on narrow, well-defined tasks, and hybrid fine-tune+retrieval beats either alone. Verdict survives; the sentence doesn't. → *"On broad tasks, frontier models now often beat fine-tuned ones — fine-tuning still wins on narrow, well-defined jobs."*

**Elsewhere:**

- [ ] **C8 · Line 690** — *"175 billion small weights"* presented as current. That's **GPT-3 (2020)**, the last frontier model whose size was published; today's are larger, undisclosed, and mostly Mixture-of-Experts — which also breaks the naive 2·N arithmetic on line 791. → add *"— that's GPT-3 (2020), the last one whose size was published."*
- [ ] **C9 · Line 1084** — *"findings by such groups has not found behavior that is inconsistent with the constitution"* → jailbreaks inducing constitution-violating behaviour are routinely published, and Anthropic's own system cards document residual susceptibility. Not defensible from a stage. → *"Jailbreakers do break it — what's notable is that when not under attack, measured behaviour tracks the stated principles surprisingly closely. Anthropic publishes those numbers in its system cards."*
- [ ] **C10 · Lines 714–718** — *"the final output token is chosen based on the probability of the closeness"* → the step from scores to token is softmax → **sampling**, controlled by temperature/top-p. As written (reinforced by "that's the closest known token") the audience believes the model deterministically picks the nearest match — contradicting the well-known fact that the same prompt gives different answers. The deck never mentions softmax, temperature or greedy decoding. → add *"Scores → softmax → probabilities → sample one. Always the top pick = 'greedy'; temperature controls how often it takes a lower-ranked one."*
- [ ] **C11 · Line 1235** — *"It's all just math, fixed at the time of training"* → weights are fixed; **generation is stochastic**. A technically-literate audience hears "fixed" as "deterministic". → *"…with weights fixed at training — but the next token is sampled, so the same context can give different answers."*
- [ ] **C12 · Lines 473–493, 519–529** — the gender-direction / analogy slides. Two problems: (a) these results are from **word2vec/GloVe static word vectors** (sushi−Japan+Germany≈bratwurst is Mikolov et al. 2013), and the arithmetic is much weaker on an LLM's input-embedding matrix, which is what the slide has just been describing; (b) the demos only work because standard implementations **exclude the three input words** from the nearest-neighbour search — Nissim et al. (2020, *Computational Linguistics*) showed the vector closest to `king − man + woman` is actually **king**, with analogy accuracy collapsing 0.71 → 0.21 once the exclusion is lifted. → add one line to the "What a surprise!" note: *"Caveat: these classic demos come from word2vec-style vectors, and they only work if you exclude the three input words — the literal nearest vector to `king − man + woman` is usually king itself. The directions are real, but fuzzy, not exact arithmetic."* (Also: "Moussolini" → "Mussolini".)
- [ ] **C13 · Line 1536 / 1572** — *"very recent functionality (from spring, 2026)"* → joint text/image embedding spaces have existed since **CLIP (2021)**, and Amazon Nova Multimodal Embeddings shipped Oct 2025. What's new in spring 2026 is *Gemini Embedding 2* as a **natively** multimodal single model. → *"Joint text+image embeddings have existed since CLIP (2021); what's new in spring 2026 is a single native model covering text, image, video and audio at once."*
- [ ] **C14 · Lines 1613–1624** — the PDF experiment. Ten documents, one run, one person is a **spot check, not a "rigorous experiment"**, and the token-cost findings are used to answer a question the test never measured (extraction *quality*). Also line 1624 is incomplete: Anthropic processes each page as **both text and image**, which is the actual reason raw PDFs cost 2–6x more. → retitle the note *"a small, informal test"*, add *"Token cost only — I didn't score accuracy"*, and → *"Claude processes each page as **both** extracted text **and** a rendered image — so you pay twice."*
- [ ] **C15 · Lines 1889–1893** — *"Practically **every** decision … the agent is **simply carrying out the LLM's bidding**"* → the LLM *proposes*; the harness *disposes*. Permission prompts, allowlists, plan mode, hooks, sandboxing, result truncation, max-turn limits and auto-compaction are all agent-side and the model neither makes nor sees them. The eight sub-bullets are fine; the framing isn't, and it undercuts the deck's own safety story. → *"Practically every decision is **proposed** by the LLM. The agent decides what it's allowed to actually do — but within those guardrails, it's carrying out the LLM's bidding."*
- [ ] **C16 · Line 2649** — *"safety classifiers … act as **hard stops** … a **hard veto** at the exit"* → classifiers are themselves probabilistic models with false negatives, aren't present on every provider or endpoint, and evasion is an active research contest. "Hard veto" implies a deterministic guarantee that doesn't exist — awkward given the deck's own correct thesis that nothing here is a hard rule. → *"…separate models sitting outside the LLM, so unlike everything else in this talk they're not just competing instructions. But they're still classifiers: very good, not infallible."*
- [ ] **C17 · Line 2762** — *"Taking notes … boosts reasoning very much (eg 3x)"* → no study supports a 3x general figure; a 2026 pre-registered replication across five memory substrates found **no** accuracy improvement on novel problems. A bare "3x" invites a challenge from the floor. → drop the number.

<details>
<summary><strong>Smaller Tier-C items (click to expand)</strong></summary>

- **Line 319** — *"vocabulary of 200,000 tokens"* → 200k is the top of the range, not typical: cl100k is 100,277, Llama 3 is 128,256. → *"100,000–200,000"*.
- **Line 548** — *"find a synonym by simply finding the closest embeddings"* → nearest neighbours are *related* words, and **antonyms are famously among the closest** (hot/cold, always/never). Someone will build a broken semantic search on this. → *"…to find related meanings — careful, 'related' includes opposites."*
- **Lines 441–443** — *"that is, in fact, what it is. A 'direction'"* → an embedding is a vector: direction **and** magnitude. Contradicts your own line 379 ("a list of numbers… a vector"). → *"a direction, plus a length. The direction carries most of the meaning, which is why we compare by angle and ignore the length."*
- **Lines 383, 434** — calling every embedding component a **"weight"** collides with the standard meaning used everywhere else in the talk. Defensible for the input embedding table (those really are trained parameters), wrong for a sentence/book/chess-position embedding, which is a computed *activation*. → line 383 *"the **value**, or feature, of that dimension"*.
- **Line 361** — *"Spotify really does characterize music using 80 dimensions"* → Spotify's *named* features number ~a dozen; the 80-dim vectors that exist are learned playlist-co-occurrence embeddings with no readable "tempo" axis. The slide claims 80 labelled traits. → *"…80-dimensional vectors per track — though those 80 numbers are learned, not hand-labelled. Nobody can say what dimension 43 means. Hold that thought."*
- **Line 932** — *"in the order of 1-5% of Google's index"* → unsupported, and the false precision invites a question you can't answer. → *"a large slice of the public web, plus books, code and licensed data — tens of trillions of tokens."*
- **Line 862** — *"Transformer's superpower: all tokens at once"* → true for training and prefill, **false for generation**, as the deck itself says 120 lines earlier. → *"reads all tokens at once… Reading the context is parallel. Writing the answer is still one token at a time."*
- **Line 1131** — *"They run on different hardware"* → Haiku/Sonnet/Opus differ in size, training and cost; same class of accelerator, just more or fewer. → *"They're different sizes — so a bigger one needs more GPUs and more time per token."*
- **Line 1212** — *"But not harder math"* → reasoning models reached IMO gold-medal level in July 2025. The honest point is *reliable arithmetic on arbitrary long numbers*. → *"Simple arithmetic gets memorised as patterns. Long, exact arithmetic doesn't — that's what `calc()` is for."*
- **Lines 1186, 1234** — *"The model can only reason about the context"* → the context is the only *input*, but the weights carry enormous parametric knowledge. As stated, the audience concludes a model can't answer anything not in the prompt. → *"The context is the model's only input — but it answers using the knowledge baked into its weights, steered by that context."*
- **Line 1168** — *"Just math: no lookup, search, humans, if-then code"* → true of a forward pass, false of what the audience uses. Humans shaped it via RLHF; deployed services do search and do run classifier code (your own line 1461 says "safeguards"). → retitle *"The **model itself**, at answer time: no lookup, no search…"* and add *"The service around it does all of that."*
- **Line 1355** — *"always lives in **their lab's** data center"* → frontier models are widely served from third-party clouds (Claude on Bedrock/Vertex/Foundry, OpenAI on Azure). → *"always runs in a datacenter — the lab's own, or a cloud partner's. Never on your laptop."*
- **Line 1401** — *"Run **open-weight full LLM** on your pc"* → what runs on a PC is a smaller, usually quantised model; "full LLM" hides the gap. And "eg for training" → in practice you **fine-tune** (LoRA/QLoRA). → *"Run a smaller open-weight model: full control and privacy, and you can fine-tune it — but it won't match a frontier model."*
- **Line 1544** — *"The dimension of a multimodal embedding is typically smaller than for text"* → Nova defaults to 3072, same as Gemini's flagship text embeddings; both use Matryoshka truncation, so dimension is a knob, not a modality property.
- **Line 1846** — *"the tool-training is **commonly done** using Toolformer"* → Toolformer (2023) is a landmark *research* result, accurately described — but not how frontier models are trained today (SFT on tool-use traces + RL on agentic tasks). → *"the idea was pioneered by a paper called Toolformer."*
- **Lines 1945–1949** — *"If the agent's tool fails silently … **this is why**"* → silent failure is *a* cause; the more common one is plain confabulation (the model reports the intended outcome without ever emitting the `tool_use` block). → *"Sometimes the tool failed silently. Other times it simply predicted the words 'I wrote the file' without ever asking for it. Both happen — which is why you verify."*
- **Lines 1951–1955** — *"Ask the AI: what tools do you have?"* → models routinely **confabulate** tool inventories, and this is now structurally guaranteed by the deferred-loading world the deck describes: if definitions aren't in context, the model *cannot* enumerate them and will guess. The slide quietly violates the deck's own "the context is ALL the LLM can respond to" rule. → add *"Caveat: it can only list tools actually in its context — with deferred loading they often aren't, and it will happily invent a plausible list. Trust the agent's `/mcp` screen, not the model's word."*
- **Line 1996 / 2054** — *"does not itself bring new functionality into the world"* → true for the facade case you demo, but memory, sqlite, filesystem and browser-automation servers *are* the implementation. MCP also exposes **resources** and **prompts**, so "just tool-calls" undersells. → *"usually a middleman to a service that already exists — though some do the work themselves."*
- **Lines 2043–2045** — *"authenticated with **your personal API key**"* / *"you must **always** be a user"* → remote MCP standardises on **OAuth 2.1**, which is what your own "authenticate on first usage" slide shows. Plenty of servers need no account. → *"…using whatever credentials you gave it — usually an OAuth login, sometimes an API key."*
- **Line 2193** — *"all other models … **saw right through** the presumed urgency"* → one informal attempt is evidence about that prompt, not about model robustness; every frontier model remains jailbreakable, which is your own (correct) point at 2185. → *"…didn't fall for **this** attempt. Which tells you it's a strong bias — not that it can't be done."*
- **Line 2257** — *"When you use Copilot in Word, **this is** the system prompt"* → from an unsourced, undated community leaks repo, never confirmed by Microsoft. → *"This is what someone got Copilot in Word to spit out about its own instructions. Unverified and undated — but it rings true, and it's the only view we get."*
- **Lines 2266–2270** — *"Completely visible"* → only half. ChatGPT has *saved memories* (listed, editable) **and** *reference chat history* (insights from past conversations) — the second has **no list view and is not auditable**. → *"…But there's a second layer — 'reference chat history' — that you can't inspect. You can only switch it off."*
- **Line 2461** — *"With a handful of MCP servers you would fill up an entire 1M context"* → at your own 500 tokens/tool that's ~2,000 tools; a handful of servers is ~25k–75k tokens. Two orders of magnitude off. The Siteimprove 500-tool example carries the point alone. → *"…could easily cost you tens of thousands of tokens before you type a word — and one server like this demo would eat a quarter of a million."*
- **Line 2648** — temperature-0 nondeterminism → the dominant cause isn't raw GPU parallelism but **batch-size-dependent kernel reductions** (your request is batched with others differently each time, changing summation order). That also makes it *fixable* — batch-invariant kernels give bit-identical output — so "simply cannot guarantee" is too strong. → *"…your request gets batched with other users' differently each run, changing the floating-point summation order. Solvable in principle — just not how shared inference is served."*
- **Line 2688** — *"Output tokens are typically 5 times as expensive"* → 5x is the Claude ratio; GPT-5 is 8x ($1.25/$10), Gemini Pro ~6x. → *"5–8 times"*.
- **Line 66** (opening bread analogy) — *"enzymes continue to work on building flavor and **gluten**"* → proteases *break down* gluten; cold-rest strength comes from hydration and slow fermentation. Three-second fix on the talk's opening metaphor. → *"…while the enzymes keep working on flavour, and the dough quietly relaxes and strengthens."*

</details>

---

## Tier D — the deck contradicts itself

These are invisible to a chunk-by-chunk review but an attentive audience member will spot them. Each needs *one* side changed, not both.

- [ ] **D1 · Line 2325 vs 2467** — #6/11 says *"only the tool's **description** may be included"*; #8/11 says *"only the tool **name**"*. Two different stories twenty slides apart. **Line 2467 is closer to right** (see A9) — align 2325 to it.
- [ ] **D2 · Line 1512 vs 1622** — *"A screenshot of text can easily result in **10x more** context than the raw text"* vs *"Gemini … 258 tokens per page — **3-18x fewer** tokens than converted markdown"*. Directly opposed, 110 lines apart. → make 1512 provider-dependent: *"Depending on the provider, a screenshot can cost several times more context than the raw text — or, as we'll see with Gemini, far less."*
- [ ] **D3 · Line 2056 vs 2141** — *"MCP servers are **no longer expensive** to include"* vs *"Every added MCP server brings the **entire list of tool-names** into every chat"*. Both can't be the mechanism. → 2141 *"Big MCP servers no longer flood every chat — their tools are searched for on demand"*; 2056 *"much cheaper to include than they used to be"*.
- [ ] **D4 · Line 1677/1735 vs 1719/1799** — *"The full chat is **always, always** sent"* vs `/compact` replacing the conversation with a summary, and thinking blocks being dropped after the turn. Also stateful endpoints (OpenAI Responses API with `previous_response_id`) mean the *client* sends only the new message. The true invariant is about **the context the model sees**, not what the client transmits. → keep the punchy heading, adjust the note: *"every turn, the whole conversation has to be back in the context. Some APIs let the server keep it for you, but it's still all there in front of the model — nothing is remembered between calls."*
- [ ] **D5 · Line 2218 vs 2264–2270** — *"An agent will **not include** earlier chats … not unless you explicitly ask"* vs the memory section two slides later. ChatGPT's reference-chat-history and Claude.ai memory pull from previous conversations **automatically**; "implicitly via a tool" doesn't cover it, nothing was invoked. → *"An agent will not dump your old chats, browser history or emails in wholesale. The one exception is memory: ChatGPT and Claude pull distilled bits of earlier chats in automatically — that's the next section."*
- [ ] **D6 · Line 1289 vs 1345** — *"The AI service itself knows **nothing** about you"* vs the later hedge that it's changing. For consumer products the memory store lives **server-side at the lab** and follows your account across web/desktop/mobile. The silo is real between *installations*, not between clients of one hosted account. → *"The AI **model** knows nothing about you. Consumer products do keep memory on their servers — but it's the product's, not the model's, and it doesn't follow you to a different agent."*

Related but not a contradiction: **line 1702** *"Total: 1+2+3+…N = O(N²) messages"* — the math is right (and it's tokens, not messages), but the **billed** cost isn't quadratic once prompt caching charges the repeated prefix at 0.1x. Line 1731 defers this ("more on that later"), which softens it, but the speaker note still asserts the naive model out loud. → add *"…so token **usage** grows quadratically. What you actually pay grows much slower — the repeated part is cached at a tenth of the price."*

---

## Verified correct — don't touch these

Checked and sound. Several of these *look* shaky, so they're worth knowing you can defend:

**Tokenizer numbers** (verified empirically with `tiktoken`, not from memory):
- "hello" = **24912** in o200k_base (gpt-4o) ✓ and **15339** in cl100k_base ✓
- token **97957** is `" Flam"` **with a leading space** ✓ — matches your vocabulary screenshot
- `" Flamsholt"` really is **3 tokens** ✓ · `"h e l l o   w o r l d"` really is **11 tokens** ✓ · `"hello world"` = 2 tokens, second is `" world"` ✓
- ≈4 characters / ¾ of a word per token for English ✓

**Cost and hardware:**
- **B200 at 4.5 PFLOPS** ✓ — that's dense FP8, the honest non-marketing number (FP4 is 9 dense / 18 sparse). Consider saying "at FP8" out loud; someone will ask.
- **Claude Opus at $25/MToken output** ✓ (Opus 5: $5 in / $25 out) — and consistent with your "output ≈ 5× input" claim
- **$27/MToken ballpark** ✓ — the arithmetic works out to ~$25–30/MTok. Defensible.
- **Harry Potter ≈ 100,000 tokens** ✓ · **pre-training $200M–$1000M / 4–8 months** ✓
- **KV-cache**: 5-minute default TTL, cache reads at 0.1x, max 4 `cache_control` breakpoints ✓. The "~10x" expiry penalty is fair rounding (0.1x read vs 1.25x write ≈ 12.5x).
- **Attention: ~1M × 1M for a 1M context** ✓ · **N² context scaling** ✓

**Names, products, claims:**
- **"Vibe" by Mistral** ✓ — Le Chat really was renamed Vibe in 2026
- **Claude Code does not read `AGENTS.md`, only `CLAUDE.md`** ✓ — confirmed as of Aug 2026; Anthropic said "not planned for now" in May 2026. The whole agent-files slide (2549–2557) checks out.
- **Anthropic removed 80%+ of Claude Code's system prompt** ✓ — claude.com blog, 24 July 2026
- **J-Space / J-lens** ✓ — real, and correctly described. Anthropic's "Verbalizable Representations Form a Global Workspace in Language Models" (July 2026).
- **Matt Pocock's grilling skill** ✓ — person, repo and path all real, correctly attributed
- **Skills mechanics** ✓ — open standard, mandatory `SKILL.md`, name+description the only required frontmatter, loaded on demand. `disable-model-invocation: true` is a real field and your hedged "seems to be a bug" is fair.
- **Claude's Constitution priority ordering** ✓ — matches the published document
- **$1B/year per lab on human data (TIME 2025)** ✓
- **Rovo, Rufus, Claude Desktop** ✓ all correctly named and described
- **Gemini's 258 tokens/page and the arithmetic** ✓ — 258 = 16×16 patches + 2; 16 patches of 24×24px = a 384×384 render. Self-consistent. Dosovitskiy and PaLI-3 citations are apt.
- **nanoGPT line counts and Karpathy video titles** ✓
- **Siteimprove demo** ✓ — "531 tools" used consistently, 64-char limit is the real constraint, 500 × 500 = 250,000 ✓

**Well-argued as written — no change needed:**
- **"True, the system prompt *is* obeyed more"** (2175–2185) — unusually well put. Correctly framed as a trained bias in the weights, explicitly denies hard enforcement, doesn't imply architectural separation. *Optional only:* you could note labs train this deliberately (OpenAI publishes it as an "instruction hierarchy"), which makes the bias sound less accidental.
- **"A penny for your thoughts"** (1794–1799) — correct including the non-obvious bit: thinking blocks are billed as output then input within a turn, and prior-turn blocks *are* stripped.
- **Chain of Thought mechanics** (1751–1762) · **the tool-call walkthrough** (1812–1877) · **backpropagation** (942–962) · **"a trained model = embeddings + weights"** (974)
- **"It's just a fancy autocomplete"** (1144–1166) — the "'just a fancy' is doing a lot of heavy lifting" note is exactly the right correction
- **The agent/service/model decomposition** (1264–1301) — correct and clearly put
- **"We don't know how the AI works"** · **"I included all of…"** · **"I told it earlier… forgotten"** · **"Soon we'll run out of training material"** (the accumulate-vs-replace distinction is stated correctly) · **"Caveman"** (the Wenyan critique checks out — ~4.6% token savings, lower success rates) · **"You are xxxx…"** · **"Ask it why it did that"** (Anthropic's introspection work finds ~20% and "highly unreliable" — supports your "don't trust that") · **"Make no mistakes"** · **"YOU MUST NEVER DO xxx!"** · **"All AI models are the same"** · **"Does it understand?"**

---

## Suggested order of attack

1. **Tier A** (12 items) — do these no matter what.
2. **C1–C7** — the rest of the myth-busting section. Wrong debunks are the most quotable failures.
3. **Tier D** (6 items) — cheap, and they're what a sharp audience member notices.
4. **Tier B** (14 items) — mechanical find-and-replace.
5. **C8–C17** and the collapsed list — polish.

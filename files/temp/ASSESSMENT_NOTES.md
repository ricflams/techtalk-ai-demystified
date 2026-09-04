# Assessment notes — AI Demystified (text + images)

## Hygiene pass (done, whole deck)
- **Image refs: clean.** 262 unique `images/...` refs in slides.md, 262 files on disk, zero missing, zero orphans.
- **Placeholders: clean.** No TODO/FIXME/xcvx. The 5 grep hits for trailing `...` are all intentional rhetorical ellipses in headings.
- **Em-dashes: 13 total. 7 are a real house-style violation.**
  - Lines 997-1003 (slide `### Same facts, different values and behaviors`) are the ONLY em-dashes in slide body text in the entire deck. 7 bullets, all using ` — `.
  - Line 1001 additionally has a double space after the em-dash (`European* —  compliant`).
  - Other 6 (804, 928-930, 1122, 2690) are inside `####` speaker notes, which don't render on slides. Lower priority / arguably fine.
- **Demystifications section (2525-2724, 200 lines) contains zero images.** Longest fully text-only stretch in the deck, and it lands late in a 1h15 talk.

## Section notes

### Intro + "Keep it simple" (12-187, 17 imgs)
STRONG:
- Yeast/bread analogy is the best framing device in the deck. It earns the thesis (mechanistic understanding -> agency) without being cute about it, and `bread/science.webp` + the cold-ferment note land the "steer it deliberately" point concretely.
- `intro/journey/rabbit-holes.webp` is a genuinely good image: all ~20 sign labels are legible real terms (transformer, embeddings, mcp, agents.md, harness, temperature, ...). Duplicated labels (context/tokens/skill/thinking x2) read as deliberate.
- `bread/ai.webp` right half is a useful structural preview of the whole deck (agent box vs AI-service box).

ISSUES:
- **`intro/journey/overview.webp` is full of garbled AI-generated text.** Legible gibberish labels include CPENCLAW, SODNVLOWS, MACOONGROOWS, NEUNAL EEMS, SCALING STERS, DEEP LEARNINS, SOA3NVNG LAWS, SCALING LANRHING, VECTO CLUSTERS, GEMINA. Several labels also repeat (CLAUDE x3, SCALING LAWS x3, DEEP LEARNING x3). In a talk whose whole argument is "understand the machine properly", visibly broken machine output as the opening scene-setter is self-undermining. Also "GPT-4" as a landmark label is stale for an Aug-2026 talk. Compare with rabbit-holes.webp, which is clean - the quality gap between the two adjacent slides is noticeable.
- `bread/ai.webp` right-hand diagram is titled "how tokens work in the LLM" but actually diagrams the whole agent/service architecture. Title doesn't match the drawing.
- Light-background images (`overview/full.webp` cream, `bread/ai.webp` white) on a dark deck. Probably deliberate illustration style, but flagging to confirm against the stick-figure diagrams later.
- Speaker note says "only one hour"; talk actually ran 1h15 without Bonus.

CONVENTION CHECK (deferred):
- `overview/full.webp`, the deck's flagship architecture image, uses NO stick figures: a full-colour cartoon woman (human), steampunk telephone rig (AI Agent), black silhouette head w/ brain (AI Service+LLM). No cap / bowtie / mustache / glasses. Need to see the real stick-figure diagrams before judging whether this is a deliberate hero-art exception or a genuine break.
- `journey/route.webp` map route visits AI-service -> Context -> Guidance -> Myths -> X, matching deck order. But "Agent" sits off-route despite AI Agents being a full h1 chapter. Map legend + "The LLM Cave" subtext are AI-gen scribble (small at presentation scale).

CONTENT:
- `temperature` appears in the deck ONLY in a speaker note (line 2345, "The final parts") - not on any slide. That note is excellent and accurate, including the point that even at temperature 0 GPU float non-determinism prevents guaranteed identical output. But the deck spends ~20 slides on "how the next token is decided" and the actual knob controlling that decision never reaches a slide. Candidate for promotion.

### The `overview/*` chapter-opener series (12 slides) - BIGGEST VISUAL FINDING
The deck's recurring "you are here" device: `overview/full.webp` (the master illustration)
dimmed to a grey wash, with a bright rectangular window over the region under discussion.
Used at lines 174,197,222,324,524,1053,1186,1231,1391,1514,1588,1734.

Measured % of pixels brighter than 230 (i.e. the size of the lit spotlight window):

| file | chapter | bright% | mean lum | verdict |
|---|---|---|---|---|
| full.webp      | overview      | 67.4 | 195 | undimmed master |
| agent.webp     | AI Agents     | 27.6 | 138 | good |
| service.webp   | AI Service    | 24.2 | 132 | good |
| tools.webp     | Tools + MCP   | 13.1 | 115 | over-broad, also swallows the head/brain |
| chatting.webp  | Chatting      | 11.5 | 116 | good |
| files.webp     | Files         |  7.3 | 109 | good, boxes the files/images cloud |
| llm-intro.webp | "LLM is brain"|  4.6 | 105 | correct, boxes the brain |
| tokens.webp    | Tokens        |  2.4 | 101 | small but on the token bubble - ok |
| **embeddings.webp** | **Embeddings** | **0.8** | 99 | **box sits over near-empty bubble area** |
| **llm.webp**   | **The LLM**   | **0.5** | 99 | **BROKEN: box is over blank background, does NOT cover the brain** |
| **thinking.png**| **Thinking** | **0.0** | **53** | **BROKEN: no spotlight at all; uniformly dimmed, and ~2x darker than every sibling** |

- The three weakest/broken openers are for **The LLM**, **Embeddings** and **Thinking** - three of
  the deck's most conceptually central chapters. `llm.webp` in particular opens the deck's single
  biggest chapter with a spotlight on empty space, next to the brain rather than on it.
- `thinking.png` will read on screen as a conspicuously darker slide than every other chapter
  opener (mean luminance 53 vs 99-138). It also uses a different highlight technique entirely
  (slight colour retention on the brain, no window) and is the only PNG in an all-WebP series.
  Note: 45,956 colours, so `shrink_images.py` correctly leaves it as PNG - the low colour count is
  itself a symptom of the uniform dimming, not a format bug.
- `tools.webp` is reused for BOTH the Tools chapter (1588) and the MCP servers chapter (1734), so
  the "you are here" map does not advance for MCP - a 173-line, 20-image chapter.
- Spotlight windows are plain axis-aligned rectangles that ignore the artwork: several bisect the
  head or clip the thought bubble's tail mid-shape. Reads as a quick mask, not a designed callout.

**CONVENTION CONFLICT:** the stated house rule is "no dimming of non-highlighted elements", but
this series dims the entire frame on 12 slides and is the deck's most-repeated visual device.
Either the rule is stale or the series is a deliberate exception - worth settling explicitly,
because it also means the stick-figure convention (cap/bowtie/mustache/glasses) is NOT what the
deck actually uses for its architecture art. `full.webp` uses a cartoon woman, a steampunk
telephone rig and a black silhouette head instead.

### The LLM + Tokens (188-321, 15 imgs)
STRONG:
- `overview-tokens.png` -> `overview-embeddings.png` is the best progressive-disclosure pair in the
  deck: the unlabeled green box in the first becomes "Embed / IDs -> vectors" with a real matrix in
  the second, and the labels are colour-coded (tokens red, embeddings blue). Clean and correct.
- The "I fart" Danish/English elevator gag is a genuinely good teaching device for
  "tokens know nothing about language", and the screenshot proves it (both occurrences = id 121583).
- Tokens recap slide is tight and correct.

ISSUES:
- **Model mismatch across the whole Tokens section.** Slide 237 is titled "ChatGPT 3.5's token
  vocabulary" and its image states 100,261 tokens. But EVERY Tiktokenizer screenshot in the section
  is set to **gpt-4o** (visible in the dropdown), which uses the ~200k o200k_base vocabulary. The
  token IDs on screen prove the switch: 121583 ("fart"), 191888, 123704 - all impossible in the
  100,261-token vocabulary the slide just showed. Nothing on the slides acknowledges the change.
  Cheapest fix: retitle to "ChatGPT's token vocabulary" and/or add a line noting the demos use 4o.
- "the four letters `fart` are always the same token" (line 282 note) is overreach. It is true for
  both occurrences shown *because both are space-prefixed*. Capitalised or string-initial "fart" is
  a different token - and the deck established exactly this two slides earlier with " world".
  Slight self-contradiction; soften to "the same token in both languages here".
- "Notice how the English sentence is longer than the Danish sentence below it, but uses fewer
  tokens" (line 288 note). The two sentences are 44 and 43 characters - essentially identical
  length, not "longer". The token-count point (6 vs ~9) stands on its own; the length claim is
  the weak part and invites a nitpick from the audience. Reword to "about the same length".
- "A token is practically **a word**" - the standard rule of thumb (~0.75 words per token for
  English) never appears anywhere in the deck, even though the Bonus cost section leans hard on
  token counts. Cheap, useful, and it inoculates against the oversimplification.

HOUSE-STYLE (em-dash) LEAK VIA IMAGES:
- The deck's canonical example answer - "No magic — just pattern matching at enormous scale" -
  contains an em-dash, and it is baked into `overview-tokens.png`, `overview-embeddings.png` and
  `what-is-an-llm-tokens.png`. So the no-em-dash rule is broken in rendered slide content that no
  grep of slides.md can catch. This text recurs throughout the deck.

### Embeddings (322-521, 20 imgs)
STRONG - this is the best-taught section in the deck:
- The Spotify -> "essence of anything" -> kitten-vector -> direction-in-space ladder is genuinely
  well built. `20d-kitten.png` is dark-themed, legible, on-palette.
- Numbers check out: GPT-3 = 50,257 tokens x 12,288 dims. Correct.
- The mechanistic-interpretability paragraph is well calibrated for 2026 ("possible to extract
  interpretable features, but how features compose is still largely unsolved"). Accurate, not oversold.
- Genuine intellectual honesty on king/queen: the deck says outright it's "the weakest of the
  examples" AND links Nissim et al.'s "Fair Is Better than Sensational", which is the actual
  critique paper. Credit for citing the debunk rather than the hype.
- `germany-japan.png` (Sushi+Germany-Japan ~ Bratwurst) is a real, well-chosen result.

ISSUES:
1. **"weight" is used for two different things, and the deck itself contradicts it.**
   Line ~365: "Each number is called the **weight** of that dimension." But line 857 is a slide
   titled "A trained model = embeddings + weights", which treats embeddings and weights as
   *separate* things. In ML, "weight" means a learned model parameter; the numbers inside an
   embedding are components/feature values. Fix the earlier one; the later usage is the correct one.
2. **The "direction for X" sequence silently escalates from evidence to invention.**
   sadness -> whimsical -> spatula are shown in identical 3Blue1Brown visual language to the real
   man/woman/king/queen result. `direction-spatula.png` is an edited frame - there is no such
   published result; it's a gag. Nothing on the slides marks where the evidence stops. The overall
   impression left is "every concept has its own clean linear direction", which overreaches: linear
   representation is well supported for *some* features, not arbitrary ones.
   **Structural note:** the correction to this overreach is the Bonus section "Dimensionality by
   superposition" - which is exactly the material that got cut for time. As delivered, the deck
   asserts clean orthogonal directions and never walks it back.
3. **The Chomsky claim is stated far more confidently than the evidence supports.** (note, line 487)
   "deeply shaken", "The overwhelming opinion now is that yeah, apparently language can be learned
   that way." The standard rebuttal is data efficiency: a child sees ~10^8 words by age 10, an LLM
   ~10^13. Poverty-of-the-stimulus is an argument about learning from *sparse* input, so LLM success
   doesn't straightforwardly refute it. The three sources cited are all polemics on one side
   (a Medium post, a 2:30 clip titled "This CRAZY Man at MIT called Chomsky", and "Chomsky was
   wrong. They taught me a lie."). This is the weakest-sourced substantive claim found so far.
   One clause would fix it: "though note an LLM sees vastly more language than any child ever does".
4. **"Spotify really does characterize music using such 80 dimensions"** is an unsourced hard
   number, on a slide that has no link, in a deck that cites generously everywhere else. Spotify's
   public audio-features API exposes ~12-13 features; the 80 figure appears to refer to something
   internal. Either source it or soften to "dozens of dimensions". ("defiant outsider energy" is
   obviously a joke label and reads fine as one.)
5. Minor: "Because that is, in fact, what an embedding is: a 'direction'." A vector has direction
   *and* magnitude, and the norm carries real information. "You can think of it as a direction" costs
   nothing and is not wrong.
6. Minor: "An embedding can express ... Any *sentence* that exists" sits on a slide whose own title
   is "1 token's meaning is represented by 1 embedding". Sentence embeddings are a real thing but
   they are not what this section is describing. Slight conflation.
7. Attribution: ~8 images in `embeddings/space/` are frames lifted from 3Blue1Brown, and one
   (`direction-spatula.png`) is an edited 3B1B frame. 3B1B is linked generally elsewhere in the deck
   but not on these slides. Fine internally; the deck is published publicly on GitHub Pages, so a
   per-slide credit would be cheap insurance.

### The Transformer (522-781, 22 imgs)
STRONG - the strongest technical exposition in the deck:
- The recap's closing argument is genuinely excellent and is the intellectual spine of the whole
  talk: "Without [being able to do math on language], all that nudging would be pointless because a
  direction learned for one word would mean nothing for any other." That closes the loop from
  Embeddings to Transformer properly, and few popular explanations bother.
- The "no hard rules, only influencing" -> "'You MUST' is still just two single tokens" landing is
  the best practical payoff in the deck. It converts architecture into an actionable intuition, and
  it is correctly framed as an architectural constraint rather than a training artifact.
- Numbers verified correct: GPT-3 = 96 attention layers; context windows 200k-1M is right for 2026;
  1M context -> ~1M x 1M attention pair calculations (O(N^2)) is right and nicely foreshadows the
  O(N^2) chat-history point later.
- Correctly notes that picking the token is "strictly speaking, outside the LLM" - a distinction
  most explainers skip. Good.

ISSUES:
1. **"Each token requires a full pass of the growing context through the LLM" is not how inference
   works, and the deck's own Bonus math assumes otherwise.** Production inference uses KV caching:
   each new token attends against cached keys/values and does NOT recompute the whole context.
   Note the internal inconsistency: the Bonus quotes ~1.2e12 multiplications for one output token,
   which is ~2 x parameter count - i.e. exactly the KV-cached per-token cost, NOT
   2 x params x context_length. So the Bonus arithmetic is right and this prose contradicts it.
   Occurs at line 733 ("85 roundtrips") and 742.
2. **The slide "Tokens are really generated one by one" links a source that refutes its framing.**
   The linked DeepSeek DSpark post (verified live) is about *speculative decoding*: a draft model
   proposes several tokens and the target model verifies them in parallel, ~6.6x throughput with
   identical output. That is precisely the technique that breaks "each token = one completely
   independent pass". Either move that link to a "but modern inference cheats" caveat, or drop it.
3. **J-space is mis-characterized.** Deck: "the *weights* that seem involved in such 'thoughts about
   future planning' are dubbed **J-Space**." I verified the cited Anthropic page: J-space is a set
   of neural *activity patterns* (named for the Jacobian technique used to find them) acting as a
   global workspace for deliberate reasoning and self-report - not weights, and not a forward-planning
   mechanism. The latent-planning claim itself is well supported, but by the circuit-tracing /
   poetry-planning work, not by J-space. Both citations are real; only the description is wrong.
4. **Third instance of the "weights" terminology error** (line 534): "each of these lists of 12288
   numbers, the *weights*, represents the core meaning". Same confusion as in Embeddings. Three
   occurrences now, plus the contradicting slide "A trained model = embeddings + weights".
5. "over 200,000 citations" - plausible for 2026 (Google Scholar was ~60k in early 2023 and has
   accelerated) but I could not confirm it. It's a headline number that drifts; worth a 30-second
   re-check before the next delivery.
6. "5 x more expensive" for output tokens is a good typical figure (Claude 5x, GPT-4o 4x,
   Gemini 2.5 Pro 8x). But the stated *cause* is wrong: output costs more because decoding is
   sequential and memory-bandwidth-bound and cannot be batched the way parallel prefill can - not
   because each output token re-runs the whole context.

### Training (782-1046, 20 imgs)
STRONG:
- Pre-training vs post-training split is clean and correctly framed: pre-training = capability,
  post-training = values/personality. The "pre-trained models are just autocomplete" slide is the
  right setup for the Bonus "fancy autocomplete" section.
- "Once training is completed, the embeddings and weights are frozen, never to be changed again."
  Correct, and load-bearing for the later myth-busts about memory and learning.
- Claude's Constitution priority ordering (broadly safe > broadly ethical > Anthropic's principles >
  genuinely helpful) is quoted correctly.
- Using the Constitution/Model Spec/Gemini principles side by side to answer "are models the same?"
  is a genuinely original framing. Most talks answer this with benchmarks; answering it with
  *published values documents* is better suited to this mixed audience and ages far better.
- nanoGPT "600 lines, 300 train.py + 300 model.py" - accurate.

ISSUES:
1. **Category error on "Same facts, different values and behaviors" (line 993-1003) - and it breaks
   the deck's own core distinction.** "Mistral wants **Vibe** *capable, open, and European*". Vibe is
   real (Le Chat was renamed Vibe in May 2026) but it is Mistral's **agent product**, not a model -
   its models are Medium 3.5 / Small 4 / Large 3. Every other entry on this slide names a model or
   model family. The deck spends an entire chapter ("The parts and their many confusing names")
   teaching agent vs model vs service, then conflates them on a slide about *training values*.
   Same slip in the post-training personality list: "Meta AI - Powerful engineer" (Meta AI is the
   assistant; Llama is the model), and the slide's own bullet correctly says "Llama" two lines later.
   Cheapest fix: "Mistral wants its models ..." / "Llama - Powerful engineer".
2. **This is also the em-dash slide** - the only 7 em-dashes in slide body text in the whole deck
   (lines 997-1003), plus a double space after the dash on line 1001.
3. **"findings by such groups have not found behavior that is inconsistent with the constitution"
   is too strong, unsourced, and load-bearing.** A successful jailbreak *is* constitution-inconsistent
   behavior, and Anthropic's own system cards - which this deck links two slides later - document
   sycophancy and alignment failures. This claim is the evidence base for the later myth-bust
   "The AI just wants to please you", so its weakness propagates. Soften to something defensible,
   e.g. "no evidence that the stated principles are merely cosmetic".
4. **Unsourced hard numbers** (the deck cites generously elsewhere, so these stand out):
   - "in the order of 1-5% of Google's index" for the training corpus. Frontier corpora are ~15-30T
     tokens (~50-100TB of text); Google's index is far larger. 1-5% looks high by an order of
     magnitude or more, and there is no link. Either source it or drop the percentage.
   - "$1 billion per year on human-generated training data, according to a 2025 Time investigation"
     - attributed but not linked. Add the link.
   - "Outlier alone runs a network of 700,000+ contractors" - unsourced.
   - $200M-$1000M / 4-8 months for a frontier pre-training run is defensible for 2026.
5. "Haiku, Sonnet, and Opus ... run on *different hardware*" is stated as fact; Anthropic does not
   disclose this. Different sizes is safe, different hardware is speculation.
6. Post-training is described purely as pairwise preference comparison with the reward signal applied
   directly to weights. That skips the reward model entirely (classic RLHF trains one, then does PPO).
   Acceptable simplification for this audience, and it maps well onto DPO/RLAIF - flagging only so
   it's a known simplification rather than an accident.

### AI Agents (1047-1173, 15 imgs) + AI Service intro (1174-1228)
**STICK-FIGURE CONVENTION: CONFIRMED AND CONSISTENT.** `roles.png` / `ai-service.png` /
`user-agent-ai.png` all use it correctly - cap=user, bowtie=agent, mustache=Muscle (browse, read
docs, run tools, safeguards), glasses+brain-in-jar=Brain/LLM. The "AI service" brace correctly spans
Muscle+Brain. `roles.png` is the single most useful diagram in the deck: it puts every confusing
synonym (AI client / AI harness / AI assistant / agentic loop; LLM / AI model) in the one place the
audience will actually look them up.

**BUT the other two stated visual rules do not describe this deck.** There are four coexisting
visual systems:
  1. white-background hand-drawn stick figures (`agents/`, `service/`) - the real convention
  2. light cream cartoon illustrations, uniformly dimmed with a spotlight window (`overview/`)
  3. black-background 3Blue1Brown frames (`embeddings/space/`)
  4. app screenshots, mixed light and dark
"Dark backgrounds, plain white text" describes only #3 and the Marp theme itself. "No dimming of
non-highlighted elements" is contradicted by #2 on 12 slides. Recommend restating the identity
rules to match what the deck actually does, rather than treating these as violations to fix -
the stick-figure system is worth protecting, the other two rules are already dead letters.

ISSUES:
- **Typo in a slide heading (line 1109): "Google's agy, in the terminal/CLI".** Should be
  "Antigravity" - the image is `antigravity.png` and the link is antigravity.google. Headings are
  the most-read text on a slide; this one is a visible stumble.
- **Em-dashes baked into `user-agent-ai.png`**, twice: "I'm Claude — what can I do for you today?"
  appears in both the red speech text and the JSON blob. Same leak as the tokenizer screenshots -
  the no-em-dash rule holds in slides.md but not in image content. If the rule matters, the images
  need a pass; if it doesn't, drop the rule.
- `roles.png` / `ai-service.png`: "You and an agent **controls** the AI" - subject-verb agreement,
  should be "control". Also a double space in "The only part that  can think". Both are baked into
  the images, so they need a redraw rather than an edit.

CONTENT - strong, no substantive errors found:
- "claude.ai is not actually the AI service as such, but in fact just an agent" is one of the best
  demystifications in the deck, and the explanation of why skills don't follow you between claude.ai
  and Claude Code makes it concrete and immediately useful.
- Correctly disambiguates "agent" (client) from "agent" (autonomous entity) and flags the collision.
- Hamlet ~30k words vs "about 28,000 words" - fine.

### Files / Multimodal (1229-1388, 18 imgs)
STRONG - and the handoff's earlier read is confirmed, this is now one of the best sections:
- **The PDF experiment is the single most valuable slide-group in the deck.** Original primary
  research, counter-intuitive result, and it overturns a widely repeated piece of folk wisdom
  ("always extract the text yourself first"). Nobody gets this from the 10,000,000 videos. The
  per-provider verdicts (ChatGPT converts to markdown anyway; Gemini renders at a flat 258
  tokens/page; Claude renders but costs 2-6x markdown) are exactly the actionable shape this
  audience needs.
- "To the LLM, it's all just embeddings" - correct and well set up by putting Files *before*
  Chatting, so the embedding machinery does double duty.
- "A screenshot of text can easily result in 10x more context than the raw text" - good, practical.
- Gemini's flat 258 tokens/page is a real, correct figure.

ISSUES:
1. **The 258-token explanation misuses its own citation.** Deck: "sliced up in 24x24 pixel squares,
   16 patches per side ie 256 patches in total". The cited paper, "An Image is Worth 16x16 Words",
   uses 16x16-**pixel** patches - the 16x16 in that title is the patch size, not the grid size. The
   deck has swapped patch size and grid dimension, and 24x24 px x 16 per side implies a 384x384
   input which is asserted, not sourced. The 256+2=258 arithmetic is fine and the headline number is
   right; only the mechanism is muddled. Since the deck cites the paper right there, an audience
   member who follows the link will see the mismatch.
2. **"a unified embedding space ... is a very recent functionality (from spring, 2026)" is wrong
   about the concept and right only about the product.** CLIP put text and images in a shared
   embedding space in 2021; ImageBind covered text/image/audio/video in 2023. What arrived in 2026 is
   the productised multimodal *embedding API* (Gemini Embedding 2, Amazon Nova 2 - both correctly
   cited). Mis-dating a five-year-old foundational idea sits badly in a deck whose pitch is
   "fundamentals that are still relevant in a year". Fix: "commercially available since spring 2026".
3. "The dimension of a multimodal embedding is typically smaller than for text" compares multimodal
   embedding dims against the LLM's internal 12,288 - but dedicated *text* embedding models are also
   ~1-3k dims. Apples to oranges as stated.
4. "I ran a **rigorous** experiment" on n=10 PDFs with no stated methodology. The result is good
   enough that it doesn't need the adjective; "systematic" would be safer in front of engineers.

### Chatting (1389-1511, 13 imgs)
STRONG - no substantive errors. Probably the highest practical-value-per-minute section:
- "The LLM is completely *stateless*" plus "the context is ALL the LLM can respond to" is the
  cleanest statement of the idea in the whole deck, and it is the load-bearing fact for at least
  four later myth-busts. Correctly framed as an architectural constraint, not a training artifact.
- The Option A/B "what is actually sent?" beat is good live-teaching structure - it makes the
  audience commit before the reveal.
- 1+2+...+N = N(N+1)/2 = O(N^2): correct.
- The sub-agent note (200k tokens spent, only "42" returns to the main context) is a genuinely
  useful detail that most people get wrong.
- "even though it should be needless to say: that means information is thrown away" - good, this is
  the bit people miss about /compact.

MINOR:
- "Claude has `/btw` to send a message out-of-band" - I could not verify this command. Worth a
  30-second check; a wrong slash-command in front of engineers is the kind of thing that gets
  corrected from the audience.

### Thinking (1512-1585, 7 imgs)
STRONG:
- The three-way "what could thinking mean?" setup (tweak the LLM? a bigger model out back? or is it
  just... more tokens?) is good pedagogy - it eliminates the two intuitive-but-wrong answers first,
  and the first one correctly reuses the earlier "weights are frozen" fact as the reason.
- **"thinking-blocks are (typically) not included in the context after this turn"** is correct for
  Claude and is a genuinely useful cost detail almost nobody knows. "They cost you, but not 'keep on
  costing you'" is a good line.
- The Haiku failure is a well-chosen demo: syllable counting is exactly what tokenization hides.
- Correctly notes thinking "can possibly also strengthen a misbelief" rather than selling it as a
  pure win.

MINOR:
- "Inject a special `<let me think about that>`-token, known from training" is a fair description of
  DeepSeek-R1-style `<think>` tags but is not how every provider does it (budgets//structured
  thinking blocks). Fine as a simplification; noting it as deliberate rather than accidental.
- "added back in, in Claude Code v2.1.68" - a very precise version number I can't verify. Worth a
  check; if it's wrong it's the kind of detail an engineer in the room will know.
- Chapter opener image `overview/thinking.png` is the broken one (no spotlight, 2x darker) - see the
  overview series section above.

### Tools (1586-1731, 11 imgs)
STRONG - the most intellectually sophisticated section in the deck:
- **"The LLM is in control - via tools"** with the eight-decision list (which tool, ask vs attempt,
  plan vs do, orchestrate subagents, parallel vs sequential, what to remember, whether to trust a
  result, when to stop) is the best idea in the talk and one most people get exactly backwards. The
  per-item speaker notes are accurate, including "end_turn is its call".
- The Toolformer summary is genuinely accurate: propose call sites, execute them, keep the insertion
  only if it reduced loss on later tokens; usefulness defined mathematically, not by human judgment.
- Correctly explains that tool definitions must be in the context to be usable, so "tools take up a
  fair chunk of the context" - which sets up the MCP lazy-loading point later. Good sequencing.
- Correctly distinguishes server-side tools (Python, web fetch) from agent-side (local files).

ISSUES:
- **"the tool-training is commonly done using a process called *Toolformer*"** overstates it.
  Toolformer (Schick et al. 2023) is the seminal self-supervised idea, but frontier tool use today
  is trained mainly via supervised fine-tuning on tool-use traces plus RL. Describe it as the origin
  of the idea, not as current practice.
- "The home-field advantage" is asserted without evidence ("Models are trained on their own lab's
  tools"). It's a plausible and widely shared practitioner observation, and "can feel more smooth"
  is appropriately hedged - but the opening claim is stated flatly. Low priority.

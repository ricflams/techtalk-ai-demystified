
---
---

# The Cutting Floor

####
Parts that didn't make it because it would stretch beyond one hour.

## Effort and Cost

####
Let's briefly talk about the amount of work that's involved in producing tokens and the cost of it.

### It's one token, what could it cost?

<img src="images/llm/cost/one-banana.jpg">

### Harry Potter ~ 100,000 tokens

<div class="cols fit">
<div><img src="images/llm/cost/harry-potter-front.png" /></div>
<div><img src="images/llm/cost/harry-potter-page-1.jpg" /></div>
</div>

####
Let's say we tokenized and fed Harry Potter through the LLM, and had it produce the next expected token. What would that entail?

Specifically for Harry Potter: People have tried that and the resulting stories are incredibly bizarre hybrids. The AI might invent a plot where Harry returns to Hogwarts, but it will subconsciously add in details from the Chamber of Secrets anyway; like renaming the Basilisk to something else but keeping the exact structural cadence of the original sequel.

### 100,000 context tokens in, 1 token out
<img src="images/llm/cost/harry-potter-transformer.png"> 

### How much math does one "token out" really need?
<img src="images/llm/cost/dr-evil-one-million-flops.jpg"> 

### Actually, about 1,200,000,000,000 multiplications
<img src="images/llm/cost/dr-evil-teraflops.jpg"> 

**FLOP** is short for Floating-Point Operation: a multiplication of two numbers

### Enter: the NVidia B200 GPU

The NVidia B200 GPU is not your grandma's GeForce graphics card, for sure.

<img src="images/llm/cost/nvidia-jensen-b200.png"> 

### 4,500,000,000,000,000 FLOPS/sec

####
The NVidia B200 GPU does 4500 trillion FLOPS/sec.

### Pedal to the metal
<div class="cols">
<img src="images/llm/cost/nvidia-b200-focus.png"> 
<div class="col-4">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1,200,000,000,000 FLOPS to produce **1 token**

4,500,000,000,000,000 FLOPS/sec is B200 capacity
<br>
One 8 x B200 cluster with Claude Opus can output serve 40 tokens/sec.
</div>
</div>

####
Or rather, it depends on the length of the context:

- 4,000 token context: 50 users at 60 tokens/sec
- 100,000 token context: 10 users at 40 tokens/sec
- 1,000,000 token context: 1 user at 15 token/sec

### Ballpark cost per output token (June 2026)
<div class="cols">
<img src="images/llm/cost/cost-per-token.png"> 
<div class="col-2">

One 8 x B200 cluster costs $500,000

- Ballpark running cost, all-included: *$27/MToken out*
- Claude Opus is priced at $25/MToken
&nbsp;

<img src="images/llm/cost/claude-pricing.png"> 
</div>
</div>

####
The business cost estimation, all included, was rather surprisingly close to the sales price.

### The B200 cluster
<img src="images/llm/cost/b200-cluster.jpeg">

####
The NVidia B200 GPU comes in clusters.

### Clusters comes as trays
<img src="images/llm/cost/b200-clusters.jpg"> 

### Trays goes into racks
<img src="images/llm/cost/b200-rack.jpg"> 

### Racks goes into aisles
<img src="images/llm/cost/b200-rack-aisle.jpeg"> 

### Now you have a datacenter
<img src="images/intro/datacenter.jpg"> 

### Why Graphics Cards (GPU)?

### Transformer's superpower: all tokens at once
<img src="images/llm/transformer-vs-sequential.png">

### GPU: master of parallel computations
<img src="images/llm/cost/red-dead-redemption.webp">

####
That's why Mac Mini and Mac Studio are so sought after: their GPU can use the full on-board RAM.

### NVidia stock price
<img src="images/llm/cost/nvidia-stock-5y.png"> 

####
And why NVidia's stock price has soared.

####
Links:
- [The World's Most Important Machine - Veritasium](https://www.youtube.com/watch?v=MiUHjLxm3V0)




## A mental model for the LLM

####
I'd like to present a mental model for the LLM that I myself have found useful in thinking about how it works, and therefore how best to handle it.

### "Once upon a ..."

### "It's just a fancy autocomplete"

<img src="images/llm/core/once-upon-a-time.svg" />

####
Yes, saying that the LLM is "just a fancy autocomplete" is objectively 100% correct. It really is. It completes and it does so automatically. Ergo, it's an autocomplete.

Buf "just a fancy" is doing a lot of heavy lifting in that sentence. Not unlike saying humans are "just a fancy mix of cells".

### Think "most probable continuation", not "answer"

- You give the model a **context**, which is practically just a text.

- The model can do *just one thing*: it has seen so much text that it can *produce next-word-probabilities* for any given context. Meaning, it can *continue the context*.

- That means *the context is everything*. It is *the only thing* the model sees. Every word in the context *nudges the model's continuation* in some direction, all based on trained patterns.

- So you don't "tell the model what to do": you give it a context so that *what you want to come next* becomes the model's *most likely continuation*.

<br>
<img src="images/llm/core/once-upon-a-time.svg" />

### So "context → next", not "question → answer"
<img src="images/llm/core/context-continuation.svg" />

####
Words go into context with the intent of steering the next prediction toward what's useful for you. That's the whole game.

The model has no other input to go by for dealing with your tasks than the context you give it.

### Predictions from seen patterns
<img src="images/llm/core/coffee.svg" />

####
The neural network is really good at making predictions based on patterns, even combinations of patterns.

### Context determines the "likely next text"
<img src="images/llm/core/knock-knock.svg" />

####
Is it just the two words "Knock knock" or does it look like a conversation? These are different patterns.

### Some "reasoning" is maybe "just a pattern"
<img src="images/llm/core/expert-advice.svg" />

####
What might look like "reasoning" is really "pattern matching"

### Even math is a pattern
<img src="images/llm/core/math.svg" />

####
Even simple math can be trained to be recognized.

But not harder math. So what's up with this "calc()" method call? We'll get to that next.

### What "a pattern-prediction machine" implies

- *Plain language with regular words* will steer it in the desired direction via pure pattern-matching of similar conversations seen during training
<br>
- *Adding examples* often gives way better output
<br>
- *Be descriptive and straightforward*, so the prediction has something to work with

####
The Transformer architecture is an incredibly impressive feat, no doubt about it.

Mechanically though, it truly is "just" a prediction machine.

But hey, maybe we humans are also just prediction machines?

## More Demystifications

### It's just autocomplete
<p class="verdict yes">Absolutely yes</p>

- And it turns out that "autocomplete" is a much bigger deal than anybody expected
- Are we humans also, at our core, "just autocomplete", made up of cells and chemicals?

### Context is "Lost in the middle"
<p class="verdict maybe">Real effect, but smaller than earlier</p>

- Models handle simple retrieval of facts from the middle really well. But less well when dealing with harder tasks and longer contexts.
- Still, it's good advice to *keep facts close to where they're used*. There's no harm done in reiterating some specific demand like "remember to use upper-case" right before relevant work, even though you already stated it 20 pages of context ago.

### Soon we will run out of training material
<p class="verdict maybe">Partly true, but less so</p>

- Yes, models are actually now trained on a reasonably large (say, 10%) fraction of public human-generated text.
- However, *non-public content, books, transcripts, and video* is a vast potential.
- Studies show that replacing real data with synthetic data does tend toward "model collapse", but accumulating the synthetic data alongside the original avoids it. So yes, we can *train on synthetic data* too, in specific ways.

####
Links:
- [Will we run out of data? Limits of LLM scaling based on human-generated data](https://arxiv.org/abs/2211.04325)
- [Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413)

### Mispellings doesn't matter
<p class="verdict yes">Yes, don't worry about misspellings</p>

- All kinds of misspellings are taught via training, so don't worry
&nbsp;
- However, *precision* matters: it's more efficient to for example refer to a file by the corrrect path and name so the LLM don't have to spend tokens searching for that file

## Tokens

### In gpt-4o, "hello" is token number 24912

<img src="images/llm/tokens/tokenize-detokenize-hello.png">

####
AI models have specific token vocabularies.

### "h e l l o   w o r l d"
<img src="images/llm/tokens/h-e-l-l-o-w-o-r-l-d.png">

####
"h e l l o   w o r l d" spelled out is 11 tokens.

This shows one advantage of the tokenization into chunks: it's simply fewer parts to work on.

### Token for "Flam" is 97957
<img src="images/llm/tokens/vocabulary-flam.png">

####
Look, there's token "Flam", in dubious company of rather inflammatory tokens.

### Tokenization saves space and let traits emerge
<img src="images/llm/tokens/wonderful-tokenization.png">

####
Another advantage of tokenization is that it allow identifying common linguistic "traits".

For example "ization", which is about "doing" or "producing" something.

### Same text, same token - always
<img src="images/llm/tokens/present.png">

####
The many meanings of "present" also are all the same token.

## Embeddings

### More of "anything imaginable"

<div class="cols">
<div>

- The concept of the number 7
- Loneliness in a crowded place
- The entire first _Harry Potter_ book
- A single chess position mid-game
- The smell of rain on hot asphalt
- A user's purchases on a website
- A protein's amino acid sequence

</div>
<div>

- The grammatical role "indirect object"
- The concept of sarcasm _(yeah, right)_
- What "London-ness" feels like
- A function's behavior in a codebase
- A legal precedent in criminal law
- The notion of "almost, but not quite"
- What 3 a.m. feels like

</div>
</div>

### The direction for "rainbow"
<img src="images/llm/embeddings/space/direction-rainbow.png" />

####
And "rainbow-ness".

### "<em>___</em> is to Italy, what Hitler is to Germany"
<img src="images/llm/embeddings/space/germany-italy.png" />

####
The math works so well that if you add up the directions for "Hitler plus Italy minus Germany" then you land near Moussolini.

### Context-free probabilities for words following "you"

"That which does not kill you only makes _you can_" - hm, that won't work
<br>

<img src="images/llm/next-token-after-you.svg">

### Let's see how that works - here's the input again
<img src="images/llm/find-the-next-token.png">

####
Let's pretent there's one token per word. Every token in the input sentence starts out as exactly one specific embedding that express the meaning of that specific token. The meaning of "Please", and "tell", and so on.

(Note: Positional information (1, 2, 3, ...) is added into each individual embedding, typically using *RoPE* (Rotary Position Embeddings) which "rotates" the vector in 2D spaces in each layer.)

### Now do this again, and again, ...
<img src="images/llm/attention-head-2.png">

### Gradually molding the meaning of the final "you"
<img src="images/llm/attention-space-seek.png">


### 175 billion small "weights" are involved
<img src="images/llm/170-billion-weights.png">

### The LLM recap

- It makes predictions about the input (context) you pass to it
<br>
- It's really good at patterns; "this looks like that".
<br>
- A successor for Transformer-technology is not around the corner, but work in ongoing on optimizations like e.g. **Mix of Experts, MoE**


### Frontier Labs and Models
The big players are called **Frontier Labs** and their models are called **Frontier Models**

<div class="cols">
<img class="col-2" src="images/agents/parts/ai-service-house.png">
<div class="col-6">

<img class="logo" src="images/llm/logos/logo-openai.svg"> **ChatGPT** by OpenAI
<img class="logo" src="images/llm/logos/logo-gemini.svg"> **Gemini** by Google
<img class="logo" src="images/llm/logos/logo-claude.svg"> **Claude** by Anthropic
<img class="logo" src="images/llm/logos/logo-grok.png"> **Grok** by xAI *(Elon Musk)*
<img class="logo" src="images/llm/logos/logo-meta.svg"> **Meta AI** by Meta *(Facebook)*
<img class="logo" src="images/llm/logos/logo-mistral.svg"> **Vibe** by Mistral AI *(French)*
<img class="logo" src="images/llm/logos/logo-deepseek.svg"> **DeepSeek** by DeepSeek *(Chinese)*

<br/>

<img class="logo" src="images/llm/logos/logo-perplexity.svg"> **Perplexity** is an *AI Wrapper*, not its own AI Service
<img class="logo" src="images/llm/logos/logo-copilot.png"> **Copilot** by Microsoft is also an *AI Wrapper*

</div>
</div>

### Pre-trained answers are pure "auto-completions"

No judgement, no reasoning.

It's just a statistical word-prediction.
<br>

<img src="images/llm/training/pre-training-is-like-autocompete.png">

## AI Service

### Remember the LLM loop?
<img src="images/llm/next-token-until-stop.png">

### Docs and images recap
<img src="images/service/overview/files.png">

####
By the time the LLM goes to work, everything in the context has been converted into a big pile of embeddings, small bits of meaning.

### Your prompts goes into the context
<img src="images/service/overview/chat-messages.png">

####
Prompt, instructions, message - many names for the same thing.

A context has many parts. Here we'll focus on just the messages you send the response you get.

Everything you send - text, documents, images - is shipped as these user-messages. Binary stuff is base-64 encoded.

### The full chat is sent to the AI
<img src="images/service/chat/chat-turn-3.png">


### The context after 10 prompts
<img src="images/service/chat/tokens-turn-10.png">

## Think harder

- Thinking could mean the LLM plan better when asked to think harder?<br>*No wait, the transformer is pure math, acting the same way for the same input.*

### A math-example
<img src="images/llm/core/math.svg" />

####
In this example, the LLM produced not a text but some mysterious "calc" code call. What's up?

### "I did the thing" No, you didn't?
Sometimes the AI will say "I did the thing". For example, "I wrote the file".<br>
But nothing was written. Why does it lie? "Oh you, silly AI"<br>
But remember, the LLM just ask for the file to be written. If the agent's tool somehow fail silently then the LLM will not know about it.<br>
It seems to rarely happen anymore but when it does, this is why.

### MCP servers recap
- An MCP server is a slim facade to some service somewhere.
<br>

<img src="images/service/mcp/mcp-simplified.png">

### MCP server takeaways
- An MCP server "just" gives the AI access to tools on *some service, somewhere*
&nbsp;
- Every added MCP server bring the entire list of tool-names into every chat
&nbsp;
- Powerful, sure, but still "just" tool-calls

### Example system prompt from VS Code
<img src="images/service/system/prompt/json-system-vscode-nowrap.png">

####
Here's an example of the Copilot system prompt in VS Code.

### It's pretty big
<img src="images/service/system/prompt/json-system-vscode-wrap.png">

####
Here it is, expanded.

### Of course, all agent prompts have been "leaked"
<img src="images/service/system/prompt/leaks-home.png">

####
Links:
- [system prompts leaks](https://github.com/asgeirtj/system_prompts_leaks)

### The Microsoft agent prompts
<img src="images/service/system/prompt/leaks-microsoft.png">

### Here's the CLAUDE.md file for this presentation
<img src="images/service/system/agent-files/claude-md-ai-talk.png">

### Every token influence all others - it's just math
<img src="images/llm/attention-space-seek.png">

####
Remember, the LLM is pure math. No "LLM code" exist to deliberately demand the text `<skills>` to appear in order to recognize the list of skills. It may help, but it's not required.




### Write your own agent
Claude.ai add lots of info:

<img src="images/service/system/my-agent/who-am-i-claude.png">

My own agent is a clean slate

<img src="images/service/system/my-agent/who-am-i-agent.png">

####
If you speak directly to the AI service, writing your own agent client code, then you have complete control and responsibility for everything in the system prompt and you start with a clean slate. If you're making some crafty AI tool then circumventing the cli agent entirely is likely preferable.

### This simple agent was simple to write
<img src="images/service/system/my-agent/my-agent-source-code.png">

####
And it's really simple to do.

Links:
- [my-agent](https://github.com/ricflams/techtalk-ai-demystified/tree/main/demo/my-agent)



### AI Service recap

- It's all just text, competing for attention. No hard rules.
&nbsp;
- Adding anything to the context is expensive so rest assured that the agent does its best to add as little as possible - no older chats, no hidden files
&nbsp;
- Adding *barely enough hints of useful info* for the LLM is the challenge, and the approaches are constantly evolving



### Context recap
- The context is all the LLM see
<br>
- No special backchannels, no place for "important instructions"
<br>
- The context is finite, so it's all about keeping it lean

####
A former CTO of mine used to say this he took someone's photo, which may sound obvious but still was surprisingly useful:

"If you can't see the camera, you aren't in the picture".

"If it ain't in the context, the AI can't reason about it"



---
marp: true
html: true
theme: demystified
paginate: true
headingDivider: 3
---
<style>
h4, h4 ~ * { display: none; }
</style>

# AI Demystified

Richard Flamsholt · 2026

####

Links to the most interesting bits.

tokenspree
etc


# Intro

## Why
Everybody's using AI

You sort of know how it works and can do.

And yet - there's a lot of AI mysticism at play, right?

You hear this very often:

* Just feed the entire codebase the AI and let it figure it out
* Point it to Confluence
* Install an MCP server - or a skill, or write an agent.md file
* "Don't say place" - or "Do say please"
* It's very useful to convert your PDFs to markdown before handing it to the AI
* I think it somehow knows to ...
* I think it doesn't know...

I'm here with the grand goal of demystifying the AI.

Now, originally I planned to giving an overview of the entire landscape of available AI tools. But it's vast and constantly moving so instead I decided to hone in on the much simpler parts: just the core steady inner parts. Which of course turned out to be filled with big rabbit holes.

So, I am not going to talk about workflow of the week, or openclaw, or that latest new command.

Instead my GOAL is that you will all become more confident with the terms and the fundamental principles of how the AI works so you're all better equipped to work with AI. Not the math, don't worry. I'll focus on facts that are useful for grasping the principles - which very often are surprising too.

After this talk you'll know much better what exactly these are: tokens, embeddings, LLM, context, AI-models, modes, thinking, agent-files, skills, tools, MCP-servers - and more.
Everything is still going to revolve around tokens and llm for the freseable future. And the constraints they bring with them also isn;t gong away. 
Anthropic just released Fable. If you look back at this talk in a year then you'll think, oh yeah, Fable, old hat now - but the underlying principles are still valid and useful to know about> Well, prove me wrong in a year. Even with progress in computing and cloud etc it's still useful to know about .... how a computer works? Fable has quantitatively become better at reasoning, it's way of juggling tools have improved, but the underlying principles and costs remain.
On that note, one caveat. I'll simplify some parts. Some AI services may do some part a bit differently. But it's been thoroughly vetted to hold up in principle and overall in practice.

Who's the intended audience? Ambitiuosly, everybody. Tech and non-tech.

There's a lot to take in. You may be thinking "hang on, that can't be right" or "I don't get it!". Feel free to ask questions during the talk. And afterwards, go checkout the slides which are on github and has links to related materials. And not least: ask me or other colleagues if you've got questions. I can elaborate on everything I'm presenting here today.

I feel like a kid in a candy store. Like when I first learned about Java and C# and bytecode.

I've learned a lot. But much more than what I could tell [big puzzle].
Prepping for this talk has helped me refine my understanding: sharpening and checking up on the fcts, ant not least extract those subconscious mental models I'd formed and figure out how to convey them in a way that can feels relevant and useful to you so you actually understand the significance, leading you to become better at wielding AI. Nothing would be easier than just walking through a jungle of facts like some misguided tour-guide - I'm trying to flesh it out in a story our caveman brainss can latch onto - hmmm.

This has been a super-challenging tech-talk to make. Because you all know about the subject, some know some parts better than me likely, and "everybody" is interested. There's just a ton to talk about, and I shouldn't tell you anything wrong, and and and.

Maybe a bit like hearing about how a car works when all you want to do is take a camping-trip to Italy. But this can help you understand why the engine overheats in that slow queue up the mountain.


### 10,000,000 AI videos... +1
<div class="cols tight">
<img src="images/intro/youtube-intro-1.png">
<img src="images/intro/youtube-intro-2.png">
<img src="images/intro/youtube-intro-3.png">
<img src="images/intro/youtube-intro-4.png">
</div>

#### Why this presentation?

What can I possibly say that hasn't already been said in the 10,000,000 existing AI-related videos?
Why is one more presentation about LLMs useful?

I guess for the same reason that you ask an AI about any topic instead of reading some of the 10,000,000 webpages about that topic: you get a personal, curated presentation that tells the story in a way I find insightful - hopefully presenting **just the good bits** from those 10,000,000 videos. Also, you can ask any questions you have.

What you're in for:

The tech part: A walkthrough of the AI-car and its parts
The driver part: advice on driving that AI-car

Strap in.


# The full picture

## Full overview
<img class="full" src="images/overview/full.png" />

You, the **human**, use an **AI Client** to communicate with an **AI Service** that turn your messages into **tokens** and feed it through an **LLM**. The service and agent can use **tools** and the agent also has **memory**.

### The clients and the AI services

### Biased for Claude

## Focus on the AI service first

## AI Service is a big backend service
Just like any big SaaS-company's services, it runs on some data center somewhere.

### The AI service, after Richard Attenborough

* The AI Service Lives in a huge airconditioned area that is ripe with cheap, reliable power, often near water.
* It's very intelligent but speak in a simple language, called JSON
* Maybe somewhat surprisingly, it really only does one thing: when you speak a sentence to it, it can predict how that sentence should continue.
* It has aqcuired that impressive skill by intensely studying and absorbing everything written in every language at an unfathomably large scale.

Let's take a peek into the brain of that little fellow. It takes its name after that capability: the Large Language Model, the LLM.

## AI Data center

<img src="images/intro/datacenter.jpg">

####
The commercial **AI Services** run in massive data centers.

### Frontier AI Foundation Models (FM)

<div class="cols tight">
<div>

<img class="logo" src="images/intro/logo-claude.svg"> **Claude** by Anthropic

<img class="logo" src="images/intro/logo-openai.svg"> **ChatGPT** by OpenAI

<img class="logo" src="images/intro/logo-gemini.svg"> **Gemini** by Google

<img class="logo" src="images/intro/logo-grok.png"> **Grok** by xAI *(Elon Musk)*

<img class="logo" src="images/intro/logo-meta.svg"> **Meta AI** by Meta *(Facebook)*

</div>
<div>

<img class="logo" src="images/intro/logo-deepseek.svg"> **DeepSeek** by DeepSeek *(Chinese)*

<img class="logo" src="images/intro/logo-mistral.svg"> **Vibe** by Mistral AI *(French)*

<br/>

<img class="logo" src="images/intro/logo-copilot.png"> Copilot by Microsoft is *not a model*

<img class="logo" src="images/intro/logo-perplexity.svg"> Perplexity AI is *not a model*

</div>
</div>

# The LLM

## LLM is the generative AI
<img class="full" src="images/overview/llm-intro.png">

## The Core Idea

### AI model ⩵ LLM

Our focus is on **AI models** that generate text. Not images, audio, etc.

All such modern AI models are built as a **Large Language Model**, aka an **LLM**.

In practice the words are synonymous: **AI Model ⩵ LLM**

<br>
<img class="half" src="images/core/ai-model.svg" />

####
 I tend to often use the word "LLM" when pointing to a specific box on a diagram or technical details and "the AI model" when talking about its behavior, but it varies.

If we're nitpicking the synonym-claim then yeah, it more correct to say that "an LLM is an AI model" and "all the current AI models used for generating text (ChatGPT, Claude, Gemini, etc) are LLMs".

### "Just a fancy autocomplete" is ...true
<img class="full" src="images/core/calculator-once-upon.png" />
<br>
<img class="half" src="images/core/ai-model-in-out.svg" />

### Not answers; "most probable prediction"

- The LLM can do *just one thing*: it has seen so much text that it can *predict the most likely next word* in any context.

- That means *the context is everything*. It's the only thing the model sees, and every word in it *pulls the model's prediction* in some direction based on trained patterns.

- So you don't "tell the LLM what to do": you build the context so that *what you want to come next* becomes the model's *most likely prediction*.
<br>
<img class="half" src="images/core/ai-model-in-out.svg" />

### Not "question→answer", but "context→next"

<br>
<img class="full" src="images/core/example-context-continuation.svg" />

### Predictions from patterns seen, even math

<br>
<img class="full" src="images/core/example-patterns.svg" />

### Context determines the "likely next text"

<br>
<img class="full" src="images/core/example-knock-knock.svg" />

### Some "reasoning" is maybe "just a pattern"

<br>
<img class="full" src="images/core/example-expert-advice.svg" />

### Not easy - human brain

That doesn't mean that it's easy to produce such a machine, or that what it does is not a great feat. It only speaks about what it actually does - how it operates, not just "at its core" but at all.

None of this means LLMs are simple to build, or that what they do isn't remarkable. It's a description of what they do — not just "at their core," but at all.

I'm not saying this is "earth shattering revelations" but I can sense that often this knowledge grounds me in a better understanding of how to shape the context.



### Steering the context

 Words go into context with the intent of steering the next prediction toward what's useful for you. That's the whole game.
 
 The model has no other input to go by for dealing with your tasks than the context you give it. So how do 



"Everything we just looked at — the social script, the authority register, the thinking trigger — is the same trick from a different angle. Tokens go into context with the intent of steering the next prediction toward what's useful. That's the whole game. The model has no other input, no other lever, no other faculty. Which means if you understand what's in the context and why each piece is there, you understand what the model is going to do. And if you understand that, you understand why prompt injection works, why agents need careful prompting, why thinking helps, why long contexts degrade — every interesting property of these systems flows from the same fact: the only knob is the tokens in the window, and somebody is always deciding which ones go in."




### "Please tell me: what is an LLM?"
<img class="full" src="images/example/claude.png">

### The LLM is all statistics: math on numbers
<img class="full" src="images/llm/overview-just-the-numbers.png">

## Tokens

### Tokens goes in, tokens comes out
<img class="full" src="images/llm/overview-tokens.png">

### A token is

* A token is practically **a word**, like "hello"
<br>
* More precisely: it is the **chunks of text** the LLM works on
<br>
* Therefore what you ultimately **pay for**
<br>

<img class="full" src="images/llm/overview-tokens.png">

### "hello" has token number 24912

* In the token vocabulary gpt-4o
* AI models typically have specific token vocabularies
<br>

<img class="full" src="images/token/tokenize-detokenize-hello.png">

### ChatGPT 3.5's token vocabulary
<img class="full" src="images/token/vocabulary-full.png">

####
* [ChatGPT’s entire vocabulary](https://emaggiori.com/chatgpt-all-tokens/)
https://emaggiori.com/chatgpt-vocabulary/

### "hello"
<img class="full" src="images/token/hello.png">

####
Tokenizers:

* [Tiktokenizer](https://tiktokenizer.vercel.app/)
* [OpenAI's tokenizer](https://platform.openai.com/tokenizer)


### "hello world"
<img class="full" src="images/token/hello-world.png">


### "hello" in the vocabulary
<img class="full" src="images/token/vocabulary-hello.png">

####
Notice that "hello" in the gpt-4o tokenizer is #24912 and in the ChatGPT vocabulary it's 15339. Vocabularies change from model to model. The concrete numbers doesn't matter outside of the AI service so you shouldn't rely on them.


### "h e l l o   w o r l d"
<img class="full" src="images/token/h-e-l-l-o-w-o-r-l-d.png">

####
This shows one advantage of the tokenization: simply fewer tokens than if everything was spelled out.

### "hello world from ..."
<img class="full" src="images/token/hello-world-from-richard.png">

####
The first four words are common and have each their own token, but "Flamsholt" isn't worthy of getting its own token so it's made up of 3 parts.

### Token for "Flam" is 97957
<img class="full" src="images/token/vocabulary-flam.png">

####
Look' there's "Flam", in dubious company of inflammatory tokens.

### Tokenizing help identify word-features
<img class="full" src="images/token/wonderful-tokenization.png">

####
Another advantage of tokenization is that it allow identifying common linguistic "traits", such as "ization" which is about "doing/producing something". Works for other languages too.


### A danish elevator "in motion"
<img class="full" src="images/token/elevator-i-fart.jpg">

####
Another advantage of tokenization is that it allow identifying common linguistic "traits", such as "ization" which is about "doing/producing something". Works for other languages too.


### I fart poetry
<img class="full" src="images/token/i-fart-marked.png">

####
Another advantage of tokenization is that it allow identifying common linguistic "traits", such as "ization" which is about "doing/producing something". Works for other languages too.


### The English advantage
<img class="full" src="images/token/five-sentences.png">

####
Examples in English, Danish, Korean, Classical Chinese, and C#.

### Revisit the example
<img class="full" src="images/token/what-is-an-llm-tokens.png">


### Tokens, summarized

* A **token** is the **chunk of text** the AI service can reason about
* Models typically have a **vocabulary** of 200,000 tokens
* For English, 1 token is roughly 1 word
<br>
And last, but not least:
<br>
* AI services **charges per token**, since tokens are the unit the LLM works on
* A ballpark figure: you pay **$1 for 100,000 output tokens**
* 100,000 tokens amounts to _"Harry Potter and the Philosopher's Stone"_

####
For English, one token generally corresponds to about 4 characters. For a text the number of tokens will typically be 30% higher than the number of words, ie 1000 words means 1300 tokens - broadly speaking.


## Embeddings
<img class="full" src="images/overview/embeddings.png">

### One more basic part: embeddings
<img class="full" src="images/llm/llm-embeddings.png">


### ⚠️ Warning ⚠️ 

This will sound confusing

Stay with me.


Computers don't understand the word "cat." They understand numbers. So we need a way to turn "cat" into numbers in a way that preserves its meaning. That's what an embedding does.

<img class="half" src="images/embedding/confused.png">

### An "embedding" is a thing, not an action
<img class="full" src="images/embedding/bicycle-tree.jpg" />

#### Notes
In everyday English, "embedding" sounds like something you do: the act of placing something into something else.

In AI, it means the concrete vector of numbers that _somehow_ represent the characteristics of something. It's a noun, not a verb. It's a "thing", not something that "happens".


### The Big Five test (OCEAN)
<img class="full" src="images/embedding/analogy_bigfive.svg" />


### Specialty Coffee Association (SCA)
<img class="full" src="images/embedding/analogy_coffee.svg" />


### Spotify's 80-dimensional characteristics
<img class="full" src="images/embedding/analogy_spotify.svg" />


### The meaning of ... "anything"?
<img class="full" src="images/embedding/20d-blank.svg" />


### Yes, the meaning of "anything"
<img class="full" src="images/embedding/20d-with-tokens.svg" />


### Embedding: a meaning's characteristics

<div class="cols">
<div>
	<img src="images/embedding/20d-kitten.png" />
</div>
<div class="col-6">

An **embedding** is a list of numbers (also called a **vector** or **tensor**) that _somehow_ characterises _something_.

The number of nuances, characteristics, we decide to use is called the embedding's **dimension**. If "kitten" is described by 20 characteristics then the embedding of "kitten" has 20 dimensions. Each number is called the **weight** of that dimension.

Embeddings can be: Any *word* you know. Any *sentence* there exist. Any *feeling* you can have. Any *concept*, including e.g. *a curious yet mildly confused audience*.
</div>
</div>

<img class="full" src="images/embedding/20d-with-tokens.svg" />


####

Also called _tensor_ in python, or _hidden state_ when speaking about the LLM.

_"Somehow"_, because we don't know what "features/traits/aspects" the dimensions corresponds to. We can't say where the "heavy" dimension is and the numbers themselves also only make sense to the LLM.


### More of "anything imaginable"

<div class="cols">
<div>

* The concept of the number 7
* Loneliness in a crowded place
* The entire first _Harry Potter_ book
* A single chess position mid-game
* The smell of rain on hot asphalt
* A user's purchases on a website
* A protein's amino acid sequence

</div>
<div>

* The grammatical role "indirect object"
* The concept of sarcasm _(yeah, right)_
* What "London-ness" feels like
* A function's behavior in a codebase
* A legal precedent in criminal law
* The notion of "almost, but not quite"
* What 3 a.m. feels like

</div>
</div>

### This would be embeddings for all words
<img class="full" src="images/embedding/vocabulary-a-z.png" />

####
Conceptually, every word has an embedding that captures its meaning. This is not entirely correct because we are of course always dealing with tokens, not words - so the vocabulary of an LLM has embeddings for every token instead of words.

### In reality, an embedding for every token
<img class="full" src="images/embedding/vocabulary-gpt-3.png" />

ChatGPT 3 has *50,257 tokens*, each described by *12,288 dimensions*

## The embeddings, where do they come from?

We'll get to that later

### The example's embeddings
<img class="full" src="images/embedding/embedding-matrix.png" />

####
Also sometimes called as "features", as each value in the vector encodes some learned semantic trait of the token. Like eg "catness" or "largeness".

In practice though we simply don't know what those dimensions mean. They don't map crisply to existing human concepts. Dimension 847 might contribute a little to formality, a little to temporal reference, a little to something related to food, and a lot to some abstract statistical regularity that doesn't map to any word in English.

There's a research field called mechanistic interpretability that tries to decompose these representations into interpretable directions. They can extract interpretable features, but understanding how features compose to produce behavior is still largely unsolved.

* [Scaling Monosemanticity and Feature Steering](https://learnmechinterp.com/topics/scaling-monosemanticity/)
* [Emotion concepts and their function in a large language model](https://www.anthropic.com/research/emotion-concepts-function)
* [How might LLMs store facts | Deep Learning Chapter 7 (3Blue1Brown)](https://www.youtube.com/watch?v=9-Jl0dxWQs8)


### The LLM is all about math on embeddings
<img class="full" src="images/llm/overview-embeddings.png" />


## The LLM
<img class="full" src="images/overview/llm.png">

### The LLM

The LLM is all about **math** and **statistics**.
<br>
It does **inference** by running the embeddings in the **context** through a giant **neural network**. After billions of calculations the result is: _"what token likely comes next?"_
<br>
Because surprisingly: on a *very large scale*, you can **do math on language**.
<br>
The LLM is really the only part of the AI that can *"think"*. When you hear *"it decides"* or *"only what is needed"* then yes, the LLM is what produced that decision.

---
<img class="full" src="images/llm/no-math.jpg">

### Recap our example xxxxx

The **context** is the input given to the LLM - here, 10 tokens
The **context window** is the longest input the LLM can handle; 200K-1M
<br>

<img class="full" src="images/llm/what-is-an-llm-example.png">

####

Two things to note here:

Why only `An`? Why not the full answer? Yeah, hold your horses just a bit longer, because: the LLM only deals with producing one next token. That's all it is concerned about: figuring out with which *probablility* any of the tokens is the vocabulary has for being the next token.

That's the second thing to note: the LLM itself actually just produce this set of probabilities. The mechanism that actually *picks that next token* is strictly speaking outside the LLM. Let's include it here to convey that the outcome eventually is a token, namely `An` in this case.

####
[Large Language Models explained briefly - 3Blue1Brown](https://www.youtube.com/watch?v=LPZh9BOjkQs)

### A neural network
<img class="full" src="images/llm/neural-network.webp">

### "The capitol of France is ..."
<img class="full" src="images/llm/neural-network-paris.webp">

### The LLM's objective: what's the next token?
<img class="full" src="images/llm/find-the-next-token.png">

####
The very observant reader may spot something unexpected. I claimed that each token's embedding was a fixed vector. But why do the two instances of "you" then not have the same embedding-values?

That's because the transformer initially instill some positional information (1, 2, 3, ...) into each individual embedding, typically using *RoPE* (Rotary Position Embeddings) which "rotates" the vector in 2D spaces in each layer.

Surprisingly, changing the vector values does not remove any of the embedding's "meaning" in the high-dimensional space. It retains its core conceptual meaning, only nudged a little bit.

### Probabilities for tokens following "you"

"That which does not kill you only makes you _can_" - hmmm, hang on

<img class="full" src="images/llm/next-token-after-you.svg">


### Enter: The Transformer, in 2017
<img class="full" src="images/llm/the-transformer.png">

### "Attention is all you need"
<div class="cols">
<img class="full" src="images/llm/attention-is-all-you-need.png">
<img class="full" src="images/llm/attention-transformer.png">
</div>

####
The 2017 paper "Attention Is All You Need" by Vaswani et al. is arguably the most consequential piece of computer science research published in the 21st century.

Today, the paper sits at over 200,000 citations, making it an absolute statistical anomaly in scientific literature.

It is the Genesis block of modern AI. Without it, there is no GPT-4, no Gemini, no Claude, no Stable Diffusion, and no AlphaFold. It transformed AI from an academic field of hyper-specialized, rigid pipelines into a unified era of generalized foundation models.


[Attention Is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

### The Transformer can figure this out:
<img class="full" src="images/llm/what-we-want.png">

### Let's begin - here's the input again
<img class="full" src="images/llm/find-the-next-token.png">

### First, all embeddings "pay attention"
<img class="full" src="images/llm/attention-head.png">

####
Every embedding gets influenced by every embedding token before it. They "absorb" the meaning of all those other embedding, influenced also by the position. So the first "you" and the second "you" come from the same token, yes, but by virtue of their position they don't carry the same meaning, i.e. they don't start out as the same embedding-values.

For a full 1M context-window this means that up all 1 million embeddings pays attention to every other of the 1 million embeddings before it. That's the order of a million times a million calculations.

### A neural network let training kick in
<img class="full" src="images/llm/multiplexer-perceptron.png">

####
This is where the model's built-in training shapes the meaning of the embeddings.

### Focus on the strong signals
<img class="full" src="images/llm/relu.png">

####
Dial up the contrast, in a way: boost the strong signals and suppress the noise.

### Now do this again...
<img class="full" src="images/llm/attention-head-2.png">

####

### Slowly molding the last embedding for "you"
<img class="full" src="images/llm/attention-space-seek.png">

####

### In fact, let's do it 96 times
<img class="full" src="images/llm/attention-96-layers.png">

####

### 175 billion small "weights" are involved
<img class="full" src="images/llm/170-billion-weights.png">

### Final embedding: the desired next "meaning"
<img class="full" src="images/llm/final-embedding-all-absorbed.png">

####

### Find next token by similarity-comparison

Also known as "cosine similarity"

Score all tokens in the vocabulary (1-200,000 tokens)

<img class="full" src="images/llm/next-token-prediction.svg">

####

The cosine similarity of 0.97 is computed in isolation — it's purely a geometric measurement between two vectors, with no knowledge of the other 127,999 tokens. The 91% is a different kind of number entirely: it's the result of a competition. Softmax takes all 128,000 similarity scores simultaneously, exponentiates each one, and divides by their sum. Every token competes against every other token at once. "Stronger" claimed 91% of the total probability mass — not because 0.97 is intrinsically high, but because it pulled far enough ahead of the field. A high cosine similarity is the evidence. The probability is the verdict.

### Choose the final output token
<img class="full" src="images/llm/final-output-token.png">

### Let's go back to our example

### The context will produce token "An"
<img class="full" src="images/llm/what-is-an-llm-example.png">

### For a full sentence: repeat until LLM says stop
<img class="full" src="images/llm/next-token-until-stop.png">

####
### 58 roundtrips for 58 tokens
<img class="full" src="images/llm/next-token-until-stop.png">
<br>
<img class="full" src="images/llm/final-output-full-tokenized.png">


### Tokens are really generated one by one

That's why output tokens are typically *5 x more expensive* than input tokens.
<br>

<img class="full" src="images/llm/tokenized-output.png">

####
This is what really boggles my mind. Each token is generated completely independently, only by choosing the most likely next word to come after what has already been seen now. There is no planning.

There's no plan to "bold" a word by emitting `** something **`. Instead at one point an ` **` is emitted and later on another `**` is emitted.

There's no planning of emitting an itemized list. At one point a `1` is emitted and then a `.` and that cause the likelyhood pattern-wise of a later `2` and `.` to occur to rise significantly. But it happens independently without any overall grand design or planning.

### It's one token, what could it cost?

<img class="full" src="images/cost/one-banana.jpg">

### Harry Potter ~ 100,000 tokens

<div class="cols fit">
<div><img src="images/cost/harry-potter-front.png" /></div>
<div><img src="images/cost/harry-potter-page-1.jpg" /></div>
</div>

####
Because the AI has access to the full text of book 1 in its active memory, but its underlying weights are deeply biased toward the real book 2, the resulting "original" stories are incredibly bizarre hybrids. The AI will invent a plot where Harry returns to Hogwarts, but it will subconsciously map the beats of Chamber of Secrets anyway—often renaming the Basilisk to something else but keeping the exact structural cadence of the original sequel.

### 100,000 context tokens in, 1 token out
<img class="full" src="images/cost/harry-potter-transformer.png"> 

### It's one token, how expensive could it be?
<img class="full" src="images/cost/dr-evil-one-million-flops.jpg"> 

### Actually: 1,200,000,000,000 multiplications
<img class="full" src="images/cost/dr-evil-teraflops.jpg"> 

**FLOPS** is short for Floating-Point Operations: a multiplication of two numbers

### Enter the NVidia B200 GPU

Not your Gaming Grandma's GeForce graphics card

<img class="full" src="images/cost/nvidia-jensen-b200.png"> 

### 4,500,000,000,000,000 FLOPS/sec

### Pedal to the metal
<div class="cols">
<img src="images/cost/nvidia-b200-focus.png"> 
<div class="col-4">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1,200,000,000,000 FLOPS to produce **1 token**

4,500,000,000,000,000 FLOPS/sec is B200 capacity
<br>
The output of one 4 x B200 cluster serving a Claude Opus tier model depends on the length of the context:
<br>
* 4,000 token context: 50 users at 60 tokens/sec
* 100,000 token context: 10 users at 40 tokens/sec
* 1,000,000 token context: 1 user at 15 token/sec
</div>
</div>

### Cost per output token
<div class="cols">
<img src="images/cost/cost-per-token.png"> 
<div class="col-2">

Price of 4x B200 cluster: $500,000

* Ballpark cost, all-included: *$27/MToken* out
* Claude Opus is priced at $25/MToken (June 2026)
&nbsp;

<img src="images/cost/claude-pricing.png"> 
</div>
</div>

### The 4x B200 cluster
<img class="full" src="images/cost/b200-cluster.jpeg"> 

### Clusters goes into trays
<img class="full" src="images/cost/b200-clusters.jpg"> 

### Trays goes into racks
<img class="full" src="images/cost/b200-rack.jpg"> 

### Racks goes into aisles
<img class="full" src="images/cost/b200-rack-aisle.jpeg"> 

### Now you have a datacenter
<img class="full" src="images/intro/datacenter.jpg"> 

### Why Graphics Cards (GPU)?

### Transformer's superpower: all at once
<img class="full" src="images/llm/transformer-vs-sequential.png">

### GPU: master of parallel computations
<img class="full" src="images/cost/red-dead-redemption.webp">

### NVidia stock price
<img class="full" src="images/cost/nvidia-stock-5y.png"> 

### 🇳🇱 All chips produced by ASML, btw 🇳🇱
<img class="full" src="images/cost/asml.jpg">

####
[The World's Most Important Machine - Veritasium](https://www.youtube.com/watch?v=MiUHjLxm3V0)

## Training

### Are all AI models the same?
<img class="full" src="images/training/chatgpt-lingo.png">

####
Admittedly I coached ChatGPT into dialing up its "chatgppt-ness" to the max before asking this question. And honestly? It worked.

### How models are trained
<img class="full" src="images/training/training.png">

####

* Base training - the "auto-complete" _facts_
* Alignment learning - the _values_
* Fine-tuning / RAG - the _specialization_

Pretraining is where the model learns language itself. Fed vast amounts of text, it learns to predict the next token — nothing more. The result is a powerful but raw capability: it knows how language works, how facts relate, how arguments are structured. It has no personality, no values, no sense of what a "good" response looks like.

Supervised Fine-Tuning (SFT) and Reinforcement Learning is where the model learns what good means to its creators. Humans or AI (RLHF or RLAIF) evaluators compare outputs and rank them. The model is iteratively shaped toward preferred behavior — this is where values, tone, refusal behaviors, and personality get baked in.

### Pre-training on "all sentences in the world"
<img class="full" src="images/training/training-corpus.png">

####
Putting the **Large** in the *"Large Language Model (LLM)"*

### Pre-training shapes network and embeddings

<div class="cols">
<div class="col-2">
	<img class="full" src="images/training/training-example.png">
</div>
<div>

**Backpropagation**:

1. Run tokens through the network like at generate
2. Boost the target token
3. Adjust both the network and the embeddings
4. Causal masking trains all sub-strings, too
5. Train on a gazillion texts

</div>
</div>

### Backpropagation is ...ok, let's move on...
<img class="full" src="images/training/backpropagation.png">

### Pre-training: model = embeddings + weigths
<img class="full" src="images/training/pre-trained-model.png">

### Pre-training cost

* From scratch for a new model
  * it costs **$200M-$1000M**
  * it takes **4-8 months**
<br>
* From an existing model
  * it costs 1-10% of full training
  * it takes weeks or months

### Pre-trained models are quite similar
<img class="full" src="images/training/pre-training.png">

### Pre-trained answers are "auto-completions"

The pre-trained model has no real values, no persona, doesn't refuse anything.

It just predicts - statistically, mechanically, like an auto-complete.
<br>

<img class="full" src="images/training/pre-training-is-like-autocompete.png">

### Post-training is what shapes the model
<div class="cols">
<img class="col-3 full" src="images/training/post-training.png">
<div class="col-2">

**Different personalities:**

ChatGPT – Structured explainer

Gemini – Diligent researcher

Claude – Honest advisor

Grok – Radical truth-seeker

Meta AI – Powerful engineer

Mistral – Efficient European

DeepSeek –  Censored thinker

</div>
</div>

### Post-training: reinforce the desired outcomes
<img class="full" src="images/training/reinforcement-learning.png">

### Reinforcement Learning by Feedback

**RLHF** - Reinforcement Learning from *Human Feedback* (declining)
**RLAIF** - Reinforcement Learning from *AI Feedback* (growing)
<br>

<img class="full" src="images/training/reinforcement-training-trend.png">

####

Frontier labs almost universally outsource the bulk of RLHF annotation rather than hiring raters directly. The main intermediaries:

* Scale AI / Outlier — the dominant player, operating as an end-to-end data engine. Outlier handles LLM annotation, Remotasks handles visual/multimodal work. Scale is OpenAI's preferred fine-tuning partner and has also worked with Meta, Google DeepMind, and others. Taskmonk AI
* Surge AI — Anthropic's primary RLHF provider, with ~50,000 expert contractors. Also used by OpenAI and Meta. Taskmonk AI
* Invisible — shifted from executive VA services to RLHF work for labs including Microsoft, Cohere, and Mistral. Routes model outputs through trained raters who score completions and rank outputs. Sacra

Outlier alone runs a network of 700,000+ contractors globally. The work is heavily gig-economy in structure.

Pay ranges from $15/hr for generalist annotators up to $500+/hr for domain experts like medical fellows and legal professionals. Invisible charges labs $30–45/hr for annotation work while paying raters $15–20/hr.

Each major frontier AI lab spends approximately $1 billion per year on human-generated training data, according to a 2025 Time Magazine investigation.

### Example: Claude's Constitution
<img class="full" src="images/training/claudes-constitution.png">

####
[Claude’s Constitution - Anthropic](https://www.anthropic.com/constitution)
[OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)

### Describes Claude’s core driving principles
<img class="full" src="images/training/claudes-constitution-example.png">

### "New model is 36% more ..."
<img class="full" src="images/training/system-cards-opus48.png">

####
[Model system cards](https://www.anthropic.com/system-cards) - System cards document the capabilities, safety evaluations, and responsible deployment decisions for Claude models.

### ChatGPT - rules over principles
<img class="full" src="images/training/openai-spec.png">

### ChatGPT spec example
<img class="full" src="images/training/openai-spec-example.png">

### Gemini et al - no public training guidelines
<img class="full" src="images/training/gemini-ai-principles.png">

### Are models different? Yes

<br>
<img class="full" src="images/training/model-behavior.png">
<br>

* Anthropic wants Claude to *reason from principles* — no rulebook needed
* OpenAI wants ChatGPT to *follow their spec* — rules written down explicitly
* Google wants Gemini to *behave correctly* — but via unpublished rules
* Meta wants Llama *powerful and open* — open weights, few restrictions
* Mistral wants Vibe *capable, open, and European* —  compliant, not principled
* DeepSeek wants its models *helpful and harmless* — as defined by the state
* xAI wants Grok to *tell the truth* — no censorship, no moralizing, no wokeness

### Models have variations

Haikku, Sonnet, and Opus are three actually different models
<br>

<img class="full" src="images/training/claude-family.png">

####
For example, the Claude family are physically three different models: different size, training, speed, cost, strengths.

## LLM recap

### 

TODO: a soft mental schematic

The purpose, recapped: You give it a string of tokens, aka the *context*, and it will produce a response based on the model's baked-in training by running that context through the Transformer. Pure math and trained knowledge. The LLM can only reason about what's in the context.

That is *all* it can do. It can't browse the web, multiply two large numbers, read a file, remember anything about you, no nothing. It can only - let's repeat: run the context through the Transformer to produce a response.

It's static, constant, and fixed on the day it was completed. The weights never changes. As a user you can't make it think differently or think "harder" or learn it something new or train it or have it remember anything. It only knows what was known the day its training was concluded.

A successor tech for LLMs is not around the corner. There's work being done with "X of experts" but generally the work continue to be N^2 for N context-length because of all the attention, so 1) we can't just keep cranking up the context window (source?) and 2) the cost will likely stay somehow "per token". So if we want to do more with the same toolset (context window) then we need to explore smarter ways of managing the context and those tokens.

Called a Foundation Model because it can be used for all kinds of things without further specializing. You can fine-tune a FM but it's not all that simple - much much simpler and safer to simply give it a prompt.

####
When you hear somebody say "then we can just fine-tune the model" you should pack a fair amount of skepticism because you can only do that for certain models and it's not as easy as it might seem. TODO: Who would fine-tune a model?





### Takeaways

It's all statistics: All the words influence each other, absorb meaning from each other.

No dictionaries, no lookup of facts, no language translations. No learning.

No strict rules. Just statistical math. This means no guarantees (actually you can't even run the same input and be guaranteed to get the same output), not enforcement, no rules. whatever text is most convincing or authoritative wins. the most probable continuation given the training distribution. It's not a battle but a likelihood contest

"no secret modes or unlock codes". No unlocking. Just. Math.

What's it good at:

Pattern recognition and analogy — "this looks like that" .

Arithmetic and counting — no calculator inside; "17 × 23" is answered by what such answers usually look like.
the model answers "what does text about counting r's in strawberry usually look like?" — not "how many r's are there?"

Anything that requires understanding the content or meaning of what's in the context is the model's decision. Anything that can be evaluated against a fixed rule without understanding content is the client's. The client enforces; the model decides. And the system prompt is the interface between them — it's the client telling the model what decisions it's responsible for making, expressed in natural language because that's the only channel available, which is also why it's not a hard guarantee.


### The context

TODO: recap what the context and context window is





### Any questions?

I know I have some: how does it browse the web, know what today is, add two numbers, understand a pdf document?

### Most Important Takeaways

* The LLMs knowledge itself is fixated after training
* The LLM can only reason about what's in the context

---
<img class="full" src="images/llm/nerdflix.png">

####
2 hours of Andrej Karpathy building a small GPT model, fully.

Only 600 lines of Python code: 300 for `train.py`, 300 lines for `model.py`.

[Let's build GPT from scratch (2 hours)](https://www.youtube.com/watch?v=kCc8FmEb1nY)
[Let's reproduce GPT-2 (4 hours)](https://www.youtube.com/watch?v=l8pRSuU81PU)
[Github repo for nanoGPT](https://github.com/karpathy/nanoGPT)
[Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)

# The AI Service
<img class="full" src="images/overview/service.png">

## What can it do?

Beyond *chatting* the functionality is surprisingly lean:
<br>
1. It can *"think harder"*, if you ask for it
2. It can read *documents*: files, images, some even video and audio
3. It can use *tools*
<br>
4. Choice of model, creativity, caching, safeguarding

####
Call internal tools; run python, produce images
Call external tools via MCP servers
Ask the caller to use tools or MCP servers

## What can't it do?

- Quite notably: *it has no memory*.
- It doesn't know you
- It can only produce text.

###

TODO: you'll find that everything is about putting things into the context, have the LLM chew on it, deal with the output from the LLM, refine, repeat.

"Everything we just looked at — the social script, the authority register, the thinking trigger — is the same trick from a different angle. Tokens go into context with the intent of steering the next prediction toward what's useful. That's the whole game. The model has no other input, no other lever, no other faculty. Which means if you understand what's in the context and why each piece is there, you understand what the model is going to do. And if you understand that, you understand why prompt injection works, why agents need careful prompting, why thinking helps, why long contexts degrade — every interesting property of these systems flows from the same fact: the only knob is the tokens in the window, and somebody is always deciding which ones go in."

### But, but, but - what about...?


* all those *agents.md* files you hear about?
* skills, gems, projects, workflows?
* your preferences of language and tone?
* modes, like planning, yolo, autopilot?

### Top-level
TODO: image of "{json question}" goes into "AI service", out comes "{json response}"

### All the parts
<img class="full" src="images/ai-service/service-blank.png">

<br>
This is the general engine room in every AI service and how to speak to it.

## Chatting

### Chatting involves just the LLM
<img class="full" src="images/ai-service/service-llm.png">

####
Feed it a context and it will produce the next expected output.

####
The purpose, recapped: You give it a string of tokens, aka the *context*, and it will produce a response based on the model's baked-in training by running that context through the Transformer. Pure math and trained knowledge.

That is *all* it can do. It can't browse the web, multiply two large numbers, read a file, remember anything about you, no nothing. It can only - let's repeat: run the context through the Transformer to produce a response.

### Chatting: bring a context, get a response
<img class="full" src="images/ai-service/service-chat.png">

####
A context has many parts. Here we'll focus on just two: the system prompt and the messages.

### Your prompts/messages are sent in the context
<img class="full" src="images/ai-service/messages/request-messages.png">

### Messages format
TODO: sent as User, Assistant - image
Also image of json

### The example, continued
<img class="full" src="images/example/chat.png">

### User message #1 and the LLM response
<img class="full" src="images/ai-service/messages/chat-turn-1.png">

### User message #2 - now what?
<img class="full" src="images/ai-service/messages/chat-turn-2-question.png">

### User message #2: what do we send to the AI?
<img class="full" src="images/ai-service/messages/chat-turn-2-choice.png">

### For user message #2: re-send the full chat
<img class="full" src="images/ai-service/messages/chat-turn-2.png">

### For user message #3: re-send the full chat
<img class="full" src="images/ai-service/messages/chat-turn-3.png">

### For every user message: re-send the full chat
<img class="full" src="images/ai-service/messages/chat-turn-goodnight.png">

### Why? The LLM need the full context

The LLM always reasons about *the full context*.
It does not, it cannot, know and reason about *anything else* than what is in the context.
You want it to know about X (beyond its training)? Then X must be *in the context*.
No links, no docs, no agents: the context is *ALL* the LLM knows about you and this chat.
<br>

<img class="full" src="images/ai-service/messages/chat-through-transformer.png">

####
If the answer needs thinking, the thinking happens in the context — so your job is to get the facts into the context. The model brings the reasoning; you bring the facts. It cannot supply what you didn't put there, and it will never tell you that's why it failed.

So the decisions that require semantic understanding are all the model's:
Clearly the LLM:

Whether to call a tool at all, and which one
Whether the task is "done" or needs another iteration
Whether to ask a clarifying question vs. proceed
What to put in a tool call's arguments
How to interpret a tool result and what to do next
Whether to flag a potential prompt injection in a tool result

### The chat after 3 prompts
<img class="full" src="images/ai-service/messages/tokens-turn-3.png">

### The chat after 10 prompts
<img class="full" src="images/ai-service/messages/tokens-turn-10.png">

### The chat after 50 prompts
<img class="full" src="images/ai-service/messages/tokens-turn-50.png">

### Total tokens spent after 50 prompts
<img class="full" src="images/ai-service/messages/tokens-turn-50-total.png">

### The System prompt

### There's more than just your messages
<img class="full" src="images/ai-service/system/request-system.png">

### System prompt
TODO: Show system prompt

"Uh, _system prompt_, sounds very special and magical".

Well, yes and no.

* A **system prompt** is *just text*
* The AI client combine "whatever is useful to tell the LLM" into system prompt(s)
* You could have *written this text yourself* and just sent it as a message

### Except - the system prompt is special
TODO: images of LLM continuations for Doctor, Parent, Teacher - and System

### So it's special, but only through training, not by rules

It doesn's do anythihg, it doesn't kickstart anything. It's just text being inserted into the context.

### All the things that goes into it
		Model
			Haikku, Sonnet, Opus - 3 concrete different models, eg Haikku probably has 1/3 of the attention layers
		Claude Code system prompt: https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html
		Chat personality
		Language preferences
			Claude has no "Italian mode" at the architecture level; language behavior is entirely emergent from training data and conditioning
			"Respond in Italian. Use Italian for all responses regardless of the language the user writes in."
		claude.md / gemini.md / agents.md etc
			Eg tell what claude /init does: produce a compact overview of things that are useful to say about this folder
		personalization, memories, ...
		[current file, selected text, terminal output, etc]
		Also, the difference between plan and agent mode
		How big is it? Show some examples.
		There’s no privileged channel; system prompt and user messages are all just tokens by the time the model sees them


### Example 1..N

### The Chat Template

Everything comes in as structured json, but end up appearing as text to the LLM

The flat-sequence fact explains a lot. Because system prompt, user input, and tool results are all just tokens in one sequence, the "authority" of a system prompt is a training artifact — RLHF conditioning — not a hard architectural boundary. That's the same fact that makes prompt injection possible.

### The full picture with tokens etc
Hammering in the notion of special tokens to steer the LLM

## Think harder

### The think harder options
TODO: screenshots en masse

### What could "think harder" mean?

Can the model's billions of weights *be tweaked on the fly* to somehow "think better"?
No, they're absolutely frozen.

Do you get *more CPU or memory* or that *"bigger AI"* they surely keep in the back room?
No, the hardware and model is fixed.

Does the LLM *plan better* or *reconsider* when asked to think harder?
No, the LLM never "plan" far ahead and always simply produce one token at a time.

Hmm. So *what is thinking* really?


### Thinking: "ponder", append, and re-process
<img class="full" src="images/ai-service/service-thinking.png">

### Let's zoom in
TODO: zoomed in

- Thinking is an autoregressive loop wrapped around the LLM: generate a "thought"-mode output, append it to the context, run the forward pass again, repeat.
- The name is **Chain of Thought**, aka, **CoT**.

####


### Some screenshot examples
TODO screenshots

### Refined output is higher quality

TODO: The haiku

Thinking generally produce a better result and the model can catch itself if it's going down the wrong path. It can however also strengthen a misbelief.

### A penny for your thoughts

TODO: tokenspree thinking, 2 x with/without keepnig the blocks

- Quite important: you also **pay for those output thinking tokens**, just like they were final output tokens.

For reasoning-heavy tasks, thinking tokens can multiply your effective output costs by 3-10x.

### Hold that thought

TODO: screenshot of heavy thinking

But many/most AI Clients do not permanently add those thinking-blocks to the context: it was a temporary step, it lead to a better

### How to control thinking
- AI Clients have all sort of names for it but it ends up as thinking, as  a thinking budget

Legend has it thatthis was how Claude controlled the thinking in early days:

There used to be The keyword hierarchy was "think" < "think hard" < "think harder" < "ultrathink"

const thinkingBudget = prompt.includes("ultrathink") ? 31999 : 0

## Files

## Documents, images ... video, audio
<img class="full" src="images/ai-service/service-files.png">

### Images (video, audio)

You simply have a magic algorithm that can convert images into snippets og meaning, ie embeddings.

Modern Multimodal LLMs (like GPT-4o, Gemini, and Claude) generally do not use a separate, traditional OCR engine (like Tesseract or Google Vision OCR) in their standard workflow. Instead, they treat text recognition as a purely visual task.

Using a ViT, a Visual 

The Vision Encoder (the Transformer "eyes") identifies patterns of lines and curves in image patches as "text-like" features.  The model has been trained on millions of images of text (screenshots, menus, handwritten notes) alongside their transcriptions.It "recognizes" a letter $A$ just like it recognizes a "cat"—it's simply a visual feature that triggers a specific concept in its latent space.

An ear, etc.

An image of text is typically 10x larger in context than the text would be.

		Images - not likely OCR, split up into patches, each turned into an embedding, then 

### Documents

Take your doc and feed it through whatever it can: word, pdf, text, images.

### "Save $$$ by not uploading PDFs"
A myth
My research

####
The LLM works on tokens so how can it understand images.
Ahh, that's because it *does not* work on tokens: it works on *embeddings*, which are crystallised "meaning-vectors". So in order to understand images we "just" have to turn the images into embeddings that represent the meaning of the different parts.

This landscape is constantly changing, but as of now the predominant approach is to divide the image up into small patches, 16x16 pixels, and then map them to embeddings. Together an "ear", "nose", and "whiskers" form a cat, so to speak.

Image → divided into tiles (512×512 px each), 1,601 tokens per tile
Each tile → divided into patches (~14×14 px each)
Each patch → becomes one token


### 4: Use tools
<img class="full" src="images/ai-service/service-tools.png">
an MCP server is a "Standardized Wrapper" for an API.
https://gemini.google.com/app/65287c836e4e8a94?hl=da

MCP is from client to some service
Not Agent to Agent

Lazy Schema Loading

MCP example: github mcv vs git cli

### MCP
<img class="full" src="images/ai-service/mcp/sticks-1-add-server.png">

### MCP
<img class="full" src="images/ai-service/mcp/sticks-2-explain.png">

### MCP
<img class="full" src="images/ai-service/mcp/sticks-3-request.png">

### MCP
<img class="full" src="images/ai-service/mcp/sticks-4-tool-search.png">

### MCP
<img class="full" src="images/ai-service/mcp/sticks-5-tool-use.png">

### MCP
<img class="full" src="images/ai-service/mcp/sticks-6-response.png">


### MCP example - Siteimprove


<div class="cols">
<img src="images/ai-service/mcp/tool-in-docs.png">
<img src="images/ai-service/mcp/tool-in-openapi-spec.png">
<img src="images/ai-service/mcp/tool-in-mcp.png">
</div>


### 5: A bit more - caching, safeguarding
<img class="full" src="images/ai-service/service-misc.png">

### "Now I have the full picture"
<img class="full" src="images/ai-service/service-full.png">


### The full monty


####
Your diagram is the undisputed Common Core of the modern LLM runtime. For standard open-weight architectures (like Meta's Llama series or Mistral) and classic chat endpoints, this blueprint captures the system flawlessly.

Your diagram captures the Canonical Engine Blueprint. It cleanly outlines the immutable data flow, boundary gates, and structural contracts of modern AI. Leaving the vendor-specific bells and whistles off the page isn't an omission—it's good engineering discipline.


"Everything we just looked at — the social script, the authority register, the thinking trigger — is the same trick from a different angle. Tokens go into context with the intent of steering the next prediction toward what's useful. That's the whole game. The model has no other input, no other lever, no other faculty. Which means if you understand what's in the context and why each piece is there, you understand what the model is going to do. And if you understand that, you understand why prompt injection works, why agents need careful prompting, why thinking helps, why long contexts degrade — every interesting property of these systems flows from the same fact: the only knob is the tokens in the window, and somebody is always deciding which ones go in."

### Token spree

<style scoped>
section { padding: 0; display: flex; flex-direction: column; }
h3 { display: none; }
iframe.game { flex: 1; width: 100%; border: none; }
.github-fallback { display: none; }
</style>

<iframe class="game"
  src="https://ricflams.github.io/techtalk-ai-demystified/tokenspree/"
  allowfullscreen>
</iframe>

<div class="github-fallback">

[![Token spending game preview](https://ricflams.github.io/techtalk-ai-demystified/tokenspree/preview.png)](https://ricflams.github.io/techtalk-ai-demystified/tokenspree/)

*[▶ Open interactive version](https://ricflams.github.io/techtalk-ai-demystified/tokenspree/)*

</div>

# The AI Clients

## Two kinds

## How do AI Clients work nowadays


## The challenge
Fable 5 stays focused across millions of tokens in long-running tasks and improves its outputs using its own notes. When we had the model play the deck-building game Slay the Spire, giving it access to persistent file-based memory improved its performance three times more than for Opus 4.8; Fable also reached the game’s final act three times more often.

## Managing the context

https://gurusup.com/blog/agent-orchestration-patterns
https://gurusup.com/blog/moe-vs-multi-agent-systems


# Reflections

## How to level up

### Level 0: Use the basic controls: modes (plan, agent), thinking, individual chats

### Level 1: give it specific general instructions

### Level 2: give it task-specific instructions: in web, use projects or gems etc; on CLI use agent.md files

### Level 3a: Skills

https://www.youtube.com/@mattpocockuk/videos

Skills look like a smart routing system — describe what a skill does, and Claude figures out when to use it. But the routing isn't magic, and it isn't symmetric.
There's an instruction baked into Claude Code's system prompt that says roughly: before writing code or creating files, check whether any skills are relevant. That instruction is what makes skills feel reliable for those task types. It's a forcing function — the model is explicitly told to look before it acts.
For everything else — answering questions, explaining concepts, responding to anything conversational — there's no forcing function. The model might still invoke a skill if your description matches strongly enough, but it's relying on the description alone to catch its attention during the forward pass. That's a much weaker signal.
The practical consequence: if you write a skill for a task type that isn't file creation or code writing — say, a skill for how your team handles incident postmortems, or tone guidelines for executive communication — and you wonder why it's not triggering reliably, this is why.
The fix is simple: add an explicit instruction to your CLAUDE.md that names the trigger condition and the file path. "Before responding to any question about incidents, first read this skill." That gives you the same forcing function the built-in instruction provides, but for your task type.
Skills aren't self-activating. The description is a hint, not a contract. If you need guaranteed activation, you need an explicit instruction.
### Level 3b: Tools

### Level 3c: MCP

my mcp poc example

### Level 4: Go crazy with subagents, agent-specific commands, openclaw, etc

### Level 5: Go beyond the Agent: speak directly AI API, setup RAG vector database, control temperature and sys prompt, etc

### Level 6: run your own AI


## Advice

### How I use AI now

Small nudging words
Planning
Like a partner
wh

## Myths

"Lost in the middle was real in 2023, is largely solved for simple retrieval in 2026, persists for complex tasks — and the reason it ever existed is still being worked out. so my suggestion is: stop worrying about the middle, and start worrying about the load. "Keep your facts close and your context lean."

### Hallucinations
for most models, including the latest GPT and Gemini iterations, deeper reasoning actually lowers the success rate at detecting nonsense — the "Reasoning Paradox." So the slide-safe version: CoT re-rolls the dice; it doesn't load them with truth.
https://claude.ai/chat/a3c1720b-17f5-46b4-8f93-93b22926f713

# Embeddings, revisited

## Similarity examples


# "In summary, in 3 paragraphs..."

---
https://github.com/seifghazi/claude-code-proxy#option-1-local-development
http://localhost:5173/
export ANTHROPIC_BASE_URL=http://localhost:3001

One big generated image of tokens/embeddings going into the LLM, etc etc

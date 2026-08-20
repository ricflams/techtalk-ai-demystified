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
Richard Flamsholt

August 2026

####
Links:
- [AI Demystified](https://github.com/ricflams/techtalk-ai-demystified/)

---
![bg](images/intro/books.jpg)

####
Over time, some landmark tech has particularly triggered my brain.

When HTML came out I was like, man, I just want to know all about it.

Same with Java and .NET, with their intriguing bytecode and VM-engines. So interesting.

---
![bg](images/intro/dopamine.png)

####
For the past year I've felt that way about AI. And I think we're all filled with emotions about AI. It's so exciting and promising, but also mysterious. There's this feeling that "it can do anything if I only hold it right". That can lead to FOMO, fear of holding it wrong, and disappointment in the AI or yourself if it doesn't work as well as you imagined it would.

---
![bg](images/intro/lightbulb.jpeg)

####
Many lightbulb-moments have given me a better fundamental understanding of AI and how to best use it. The context, cost, limitations. It has *demystified* the AI and I wish for other to have that insight too.

---
![bg](images/intro/bread/loaf.jpg)
####
Let's begin far away from AI: a nice, freshly baked bread.

You can bake lovely, soft, crunchy bread without knowing what "yeast" actually is or what it does.

"Add yeast, then set the clock to let the dough rise for one hour", as the recipe says. The bread comes out fine. Usually.

---
![bg](images/intro/bread/rise.jpg)
####
But how *does* yeast cause the dough to "rise"? And should the dough be placed somewhere warm? But not too warm?

---
![bg](images/intro/bread/cold.png)
####
Some even say "put the dough in the fridge". It can seem a bit mysterious.

---
![bg contain](images/intro/bread/science.png)
####
Now, if you know that yeast is a living organism that cause fermentation by using enzymes to feed on sugar in the flour, then the whole thing can become quite demystifed. Still complex, sure, but you can now understand how the choice of flour, additives, and temperature over time affect the dough. And understand how you can make deliberate choices to "steer" the dough better.

For example a "cold ferment": let the yeast work normally for an hour and then place the dough in the fridge to put the yeast to sleep while the enzymes continue to work on building flavor and gluten. A lot of advanced baking processes can seem arbitrary or magical ("add diastatic malt powder to ...") but armed with a fundamental understanding of the way yeast and enzymes works you're much better equipped to understand them - and steer them your own way, too.

---
![bg contain](images/intro/bread/ai.png)
####
This presentation is about the yeast and enzymes of AI. And frankly, it's about *all of the AI*.

---
![bg contain](images/intro/bread/handshake.jpg)
####
Will that kind of knowledge turn you into an expert baker overnight? Maybe not. But it will help you better reason about the underlying mecahnisms, the fundamental behavior and limitations of the AI. Personally I have found that really, really useful.

---
![bg](images/intro/bread/variety.jpg)
####
It's my hope and goal that this presentation will help you rise (haha) to become much more confident in your use of AI.

# "Keep it simple"

---
![bg](images/intro/journey/overview.png)

####
This may well has been the most challenging presentation I've ever put together.

It's not some fringe topic, like Quantum Computing where I could just shine or dazzle you and nobody would know anything about it beforehand.

On the contrary: everybody are interested in AI and everybody are using AI.

I should most certainly strive to give insights that is truly useful and I decided it would be the fundamentals: the LLM and AI-service itself, the core understanding that is still relevant in a year.

Just those parts. Just keep it simple, I thought.

---
![bg](images/intro/journey/rabbit-holes.png)

####
"Simple", yeah right. Everywhere I looked there was a rabbit hole worthy of an entire presentation. Oh well.

---
![bg](images/intro/journey/route.png)

####
This is the path we'll take:

We'll start with the technical parts. How does the AI work? What can it do? In particular explore the LLM deeply because it is the most fundamental part of all.

With that knowledge loaded we'll see how to tame the context and look at some guidance and demystifications.

### 10,000,000 videos + 1
<img src="images/intro/youtube.png">

####
What can I possibly say that hasn't already been said in the 10,000,000 existing AI-related videos? Why not just give you 10 links to the most popular videos about AI and LLMs?

It's for same reason that you ask an AI about any topic instead of reading some of the 10,000,000 webpages about that topic: it's just easier to get a refined presentation that tells the story in an insightful way, focusing on the good bits from those 10,000,000 videos. Also, you can ask any questions you have.

---
![bg](images/intro/questions.jpg)
####
About that: if you're thinking "hang on, that can't be right" or "I don't get it!" then do feel free to raise your hand and ask questions.

Afterwards go revisit the slides at your own pace. They are on github and has lots of links to related materials.

And ask me or other colleagues if you've got questions. I'd be happy to elaborate on *everything* I'm presenting here today.

Links:
- [Tech Talk: AI Demystified](https://ricflams.github.io/techtalk-ai-demystified/)

---
![bg](images/intro/one-hour.jpg)
####
I've really strived to make the presentation deep and useful but also entertaining and surprising. Be prepared to stay alert, because there's a lot to cover in only one hour so it will be information-packed and move fast.

---
<img src="images/overview/full.png" />

You, the **human**, use an **AI Agent** to communicate with an **AI Service** that turn your messages into **tokens** and feed it through an **LLM**. The service and agent can use **tools** and the client can **remember**.

####
This presentation focus on AI that generates text, like Claude, ChatGPT, Gemini, Grok, etc.

So AI here means **generative text AI**. Not AI for generating images using stable diffusion, not AI for self-driving cars, not AI for folding proteins.

Links:
- [Understand AI in 14 minutes – with Anthropic's Chloe Lubinski [ARC 2026]](https://www.youtube.com/watch?v=aBUniZHgCnE)
- [AlphaFold - The Most Useful Thing AI Has Ever Done](https://www.youtube.com/watch?v=P_fHJIYENdI)
- [A quest for a cure: AI drug design | Isomorphic Labs](https://www.youtube.com/watch?v=XpIMuCeEtSk)

# The LLM

---
<img src="images/intro/journey/enter-rabbithole.png">

### The LLM is the brain
<img src="images/overview/llm-intro.png">

####
The LLM, the **Large Language Model, is the part that does all the *thinking*.

It's fundamental so let's start there and work our ways up.

### "Please tell me: what is an LLM?"
<img src="images/llm/claude-please-tell-me.png">

####
Here's an example I'll use throughout this presentation.

I'm asking Claude: "Please tell me: what is an LLM?"

### The LLM only does math on numbers
<img src="images/llm/overview-embeddings.png" />

####
The LLM can't understand words. It only works on numbers.

Everybody has heard of *tokens*, but the numbers that the LLM works on are not actually those tokens. Instead it works on something very interesting called *embeddings*.

It's important to understand both, not least embeddings, so let's cover them first of all.

## Tokens and embeddings

## Tokens
<img src="images/overview/tokens.png">

####
First let's focus on tokens.

### Tokens goes in, tokens comes out
<img src="images/llm/overview-tokens.png">

### A token is

- A token is practically **a word**, like "hello"
&nbsp;
- It is the **chunk of text** the LLM works on
&nbsp;
- Therefore, it's what you ultimately **pay for**
&nbsp;

### ChatGPT 3.5's token vocabulary
<img src="images/llm/tokens/vocabulary-full.png">

####
Links:
- [ChatGPT’s entire vocabulary](https://emaggiori.com/chatgpt-all-tokens/)
- [ChatGPT’s vocabulary: The words that ChatGPT knows and how they were chosen](https://emaggiori.com/chatgpt-vocabulary/)

### "hello"
<img src="images/llm/tokens/hello.png">

####
"hello" is one single token.

Links:
- [Tiktokenizer](https://tiktokenizer.vercel.app/)
- [OpenAI's tokenizer](https://platform.openai.com/tokenizer)

### "hello world"
<img src="images/llm/tokens/hello-world.png">

####
"hello world" is two tokens.

Yes, that second token really is _(space)_ followed by "world". Turns out it's more efficient to have variations of tokens with or without space or punctuation than spending token on _(space)_.

### "hello world from ..."
<img src="images/llm/tokens/hello-world-from-richard.png">

####
The first four words are common and have each their own token, but unsurprisingly "Flamsholt" is not common enough to be an individual token so it's made up of 3 tokens.

### A danish elevator "in motion"
<img src="images/llm/tokens/elevator-sign.jpg">

####
In Danish, "I FART" means "In motion". Tourists are amused.

### I fart poetry
<img src="images/llm/tokens/elevator-i-fart.png">

####
As you can see, the four letters "fart" is always the same token. The tokens are not aware of languages at all.

### English words are most economical
<img src="images/llm/tokens/five-sentences.png">

####
English is "better" tokenized that many other languages, simply by virtue of English words being very common.

Here are some examples of English, Danish, Korean, Classical Chinese, and C#.

Notice how the English sentence is longer than the Danish sentence below it, but use fewer tokens.

### The example, tokenized
<img src="images/llm/tokens/what-is-an-llm-tokens.png">

####
This is what the example conversation looks like when tokenized.

Notice how markdown for bold, the double-star `**`, has its own token.

And `**,` is also common enough to have its own token.

### Tokens recap

<div class="cols">
<img class="col-2" src="images/llm/tokens/ride-tokens.png">
<div class="col-5" >

- A **token** is the *chunk of text* the LLM reason about
- Tokens know nothing about *language*
<br>
- The *cost* is per token
</div>
</div>

####
For English, one token generally corresponds to about 4 characters.

## Embeddings
<img src="images/overview/embeddings.png">

####
You probably knew about tokens.

The LLM does not deal directly with tokens. Instead, it works on something called *embeddings*.

Embeddings are sort of the "live" counterpart to tokens. They are very valuable to grasp the meaning of. It may feel abstract and complex so sit tight.

### In AI, an *embedding* is vector of numbers whose values *somehow* represent the characteristics of *something*

### Confused? Okay, stay with me
<img src="images/llm/embeddings/confused.png">

### Spotify's 80-dimensional music characteristics
<img src="images/llm/embeddings/analogy_spotify.svg" />

####
Imagine designating a number to characteristics of music. Both "Lose Yourself" and "Baby Shark" score high on "tempo", but vastly different on the aspect of characteristics "defiant outsider energy".

In fact, Spotify really does characterize music using such 80 *dimensions*.

### Imagine capturing the "essense" of ... <em>anything</em>
<img src="images/llm/embeddings/20d-with-tokens.svg" />

####
Now, imagine if you could characterize _anything_ with suitable characteristics. For example, "laugther" is quite "ancient" while "software developer" is not very "ancient".

That's essentially what the purpose of an embedding is, to the AI.

### An embedding is a token's <em>characteristics</em>

<div class="cols">
<div>
	<img src="images/llm/embeddings/20d-kitten.png" />
</div>
<div class="col-6">

An **embedding** is a list of numbers (also called a **vector** or **tensor**) that _somehow_ characterises _something_. Sometimes called "features", as each value in the vector encodes some semantic trait of the token.

The number of nuances, characteristics, we decide to use is called the embedding's **dimension**. If we choose 20 characteristics then the embedding of "kitten" has 20 dimensions.

Each number is called the **weight** of that dimension.

Embeddings can be: Any *word* you know. Any *sentence* there exist. Any *feeling* you can have. Any *concept*, for examlpe *a curious yet mildly confused audience*.
</div>
</div>

### A token's meaning is represented by 1 embedding
<img src="images/llm/embeddings/vocabulary-gpt-3.png" />

ChatGPT 3 has *50257 tokens*, each described by a *12288-dimensional* embedding

####
In the AI, an embedding is a large set of numbers, for example 12288 numbers in ChatGPT 3, that characterizes a single concept, for example the token "amplification" or "gazed". It may sounds a bit crazy that it could even be possible to somehow characterize anything with such shared aspects but yes, that's what's happening.

There's nothing magic about 12288 as such. It just a very fine-grained way to express many characteristics.

### More examples
<img src="images/llm/embeddings/three-embeddings.svg" />

####
Frankly we simply don't know what the dimensions or numbers mean. They don't map crisply to existing human concepts but only makes mathematical sense. Dimension number 7 of "Please" might contribute a little to politeness, a little to interactivity, a little to something related to food, and a little to some abstract concept that doesn't map to any word in English.

There's a research field called mechanistic interpretability that tries to decompose these representations into interpretable directions. It possible to extract interpretable features, but understanding how features compose to produce behavior is still largely unsolved.

Links:
- [Scaling Monosemanticity and Feature Steering](https://learnmechinterp.com/topics/scaling-monosemanticity/)
- [Emotion concepts and their function in a large language model](https://www.anthropic.com/research/emotion-concepts-function)
- [How might LLMs store facts | Deep Learning Chapter 7 (3Blue1Brown)](https://www.youtube.com/watch?v=9-Jl0dxWQs8)

### The example's embeddings
<img src="images/llm/embeddings/embedding-matrix.png" />

####
Each of these lists of 12288 numbers represent the* core meaning* of that single token. The meaning of "Please", the meaning of "tell", the meaning of "me", and so on.

All in all, this set of numbers represents that initial static context-free meaning of each single token in the sentence.

The numbers are called *weights* and they are constructed during the LLM's training. Right now just accept that those 12288 numbers do in fact characterise all aspects of one single token. We'll cover later how they're constructed.

### Imagine an embedding as a "direction" in a hyper-dimensional space of "everything that exists"

<img src="images/llm/embeddings/space/word-embeddings.png" />

####
One way to think about an embedding is as a "direction", an "arrow", in a hyper-dimensional space of every conceivable and inconceivable concept, aka **latent space**.

Because that is, in fact, what it is. A "direction".

### Similar "meanings" have similar "directions"
<img src="images/llm/embeddings/space/similarity.jpg" />

####
The more similar two "meanings" are, the more similar their embedding-numbers will be.

So similar meanings (concepts, objects) tends to "cluster" together, in this 12288-dimensional space.

### The big surprise to everybody:<br>We can "do math" on language

---
<img src="images/llm/embeddings/no-math.jpg">

####
Don't worry, there will only be a little bit of math.

### Example: Two embeddings, man and woman
<img src="images/llm/embeddings/space/gender-man-woman.png" />

####
Imagine the two embeddings of the words for "man" and "woman" as directions in this space.

They're somewhat similar because men and women as concepts are pretty similar, but they differ in the sense that "man" is masculine and "woman" is feminine.

### Uncle and aunt
<img src="images/llm/embeddings/space/gender-uncle-aunt.png" />

####
Now it turns out that the "difference", or "direction", between the words "man" and "woman" is pretty much the same as between the words "uncle" and "aunt".

### Nephew and niece
<img src="images/llm/embeddings/space/gender-nephew-niece.png" />

####
Not only that, but the it's the same direction between the words "nephew" and "niece".

### King and queen
<img src="images/llm/embeddings/space/gender-king-queen.png" />

####
And the same direction between the words "king" and "queen".

### There's a "gender direction"
<img src="images/llm/embeddings/space/gender-father-mother.png" />

####
So very surprisingly, it turns out that there exist a kind of "gender-direction" in this space of meanings.

In fact, we have identified the embedding (a direction is an embedding) of the concept "the feminine version of something".

### The direction for "sadness"
<img src="images/llm/embeddings/space/direction-sadness.png" />

####
Turns out a direction/embedding also emerges for "sadness".

### The direction for "whimsical"
<img src="images/llm/embeddings/space/direction-whimsical.png" />

####
And for the concept of "whimsical".

### The direction for "spatula"
<img src="images/llm/embeddings/space/direction-spatula.png" />

####
And "spatula-ness".

### "<em>___</em> is to Germany, what Sushi is to Japan"
<img src="images/llm/embeddings/space/germany-japan.png" />

####
The math works so well that if you add up the directions for "Sushi plus Germany minus Japan" then you land near Bratwurst.

### What a surprise!

####
What a surprise: with *the right modelling*, we can actually *do math on language*.

####
Yes, it does feel crazy that by characterizing anything using the "right" 12288 numbers we can and end up with "concepts" we can manipulate mathematically.

It may sound magical, and in a way it is. And for now, just accept it as a fact that we can construct these embeddings so the math works out. You'll understand in a bit.

### Embeddings recap

- Embeddings are "meanings" and that meaning can be *transformed with math*
<br>
- An embedding is *just some numbers*. Cheap to store in a database and work on.
<br>
- You can *compare embeddings* to figure out *how similar* the meanings they represent are.
For instance, find a *synonym* by simply finding the closest embeddings to a word.

### The LLM is all about "doing math on embeddings"
<img src="images/llm/overview-embeddings.png" />

## The LLM
<img src="images/overview/llm.png">

### Putting the example through the LLM

The **context** is the input given to the LLM - here, 10 tokens
The **context window** is the longest input possible, typically 200,000-1,000,000 tokens
The LLM does **inference** by running the embeddings through a giant **neural network**
<br>

<img src="images/llm/what-is-an-llm-example.png">

####
Two things to note here:

Why only `An`? Why not the full answer? Yeah, hold your horses just a bit longer, because: the LLM only deals with producing one next token. That's all it is concerned about: figuring out with which *probablility* any of the tokens is the vocabulary has for being the next token.

That's the second thing to note: the LLM itself just produce this set of probabilities. The mechanism that actually *picks that next token* is strictly speaking outside the LLM. Let's include it here to convey that the outcome eventually is a token, namely `An` in this case.

####
Links:
- [Large Language Models explained briefly - 3Blue1Brown](https://www.youtube.com/watch?v=LPZh9BOjkQs)

### A neural network
<img src="images/llm/neural-network.webp">

####
A neural network is basically just a giant, organized set of multiplications and additions.

### Add up, multiply by factors, add up, ...
<img src="images/llm/neural-network-nodes.png">

#### 
You feed the network some numbers, the numbers goes through a number of steps where they are multiplied by "weights" and then added up, and out comes other numbers. And so it continues.

### "The capitol of France is ..."
<img src="images/llm/neural-network-paris.webp">

####
The thing is that if you adjust those small "weights" appropriately then you can shape the output to actually match an expected outcome. A sufficiently large network could for example after billions of calculations produce a number that represent "Paris" if we feed it numbers that represents the sequence "The capitol of France is".

And that is in fact what the LLM does. But let's start at the beginning.

### The LLM's objective: find the likely next token
<img src="images/llm/find-the-next-token.png">

####
Let's focus on this example:

Find out what should follow "That which does not kill you only makes you ___".

####
Just choosing the statistically most likely next word to follow "you" won't work. We need to look at more context to decide what naturally shoould follow that "you". Frankly, we probably need to look at all that comes before that "you" to properly decide on what should follow. That's a tough task for longer sentences.

### Enter: The Transformer, in 2017
<img src="images/llm/the-transformer.png">

####
The invention that made all of this possible, is called *The Transformer*.

### "Attention is all you need"
<div class="cols">
<img src="images/llm/attention-is-all-you-need.png">
<img src="images/llm/attention-transformer.png">
</div>

####
The 2017 paper "Attention Is All You Need" by Vaswani et al. is arguably the most consequential piece of computer science research published in the 21st century.

Today, the paper sits at over 200,000 citations, making it an absolute statistical anomaly in scientific literature.

It is the Genesis block of modern AI. Without it, there is no GPT-4, no Gemini, no Claude, no Stable Diffusion, and no AlphaFold. It transformed AI from an academic field of hyper-specialized, rigid pipelines into a unified era of generalized foundation models.

Links:
- [Attention Is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

### The Transformer can figure out the next token
<img src="images/llm/what-we-want.png">

### First, all embeddings "pay attention" to each other
<img src="images/llm/attention-head.png">

####
Every embedding gets influenced by every embedding token before it. They "absorb" the meaning of all those other embedding, influenced also by the position. The first "you" and the second "you" come from the same token, yes, but by virtue of their position they don't carry the same meaning, i.e. they don't start out as the same embedding-values, and they therefore influence the other tokens in each their way.

For a full 1M context-window this means that up all 1 million embeddings pays attention to every other of the 1 million embeddings before it. That's the order of a million times a million calculations.

### Then passed through a neural network
<img src="images/llm/multiplexer-perceptron.png">

####
This is where the model's built-in training shapes the meaning of the embeddings.

### Focus on the strong signals
<img src="images/llm/relu.png">

####
More math dials up the contrast, in a way: it boosts the strong signals and suppress the noise.

### Let's do it 96 times (attention layers)
<img src="images/llm/attention-96-layers.png">

####
Through billions of additions and multiplications.

### Final numbers: the desired "next meaning"
<img src="images/llm/final-embedding-all-absorbed.png">

####
After going through 96 trips of embeddings influencing each other, the final vector has absorbed all the relevant meanings of the entire context and now reflects what the following embedding "most likely looks like".

### Then "simply" find most similar token

Compare the final expected embedding to the embeddings of *all tokens in the vocabulary* (e.g. 200,000 tokens) by taking the dot-product, which compares the two directions.

<img src="images/llm/next-token-prediction.svg">

####
Then, it's "simply" a matter of finding out what tokens are most similar to the desired meaning.

Is it "dancing?" No.
Is it "sw developer"? No.
Is it "stranger"? That one's pretty close.
"Is it stronger"? Yes, that's the closest known token.

### Choose the final output token
<img src="images/llm/final-output-token.png">

####
The final output token is chosen based on the probability of the closeness to the final vector-values. Here, "stronger".

### Back to "Please tell me: what is an LLM?"

### For this context, the LLM will produce token "An"
<img src="images/llm/what-is-an-llm-example.png">

### For a full sentence: repeat until LLM says stop
<img src="images/llm/next-token-until-stop.png">

####
Keep on adding the produced token to the context and go another round through the LLM, until the LLM emit a special "I'm done"-token.

### 85 roundtrips for 85 tokens
<img src="images/llm/final-output-full-tokenized.png">

### Yes, tokens are really generated one by one

That's why output tokens are typically *5 x more expensive* than input tokens.
<br>

<img src="images/llm/tokenized-output.png">

####
Each token really is generated by a completely independently pass through the LLM that choosing the most likely next word to come after the context.

However, studies have found that the LLM actually *does latently* plan for the continuation that follows this single token; the pass that produced "An" is poised to very likely produce " L" and "LM" afterwards.

The field of study is called **Interpretability** and the weights that seem involved in such "thoughts about future planning" is dubbed **J-Space**.

Links:
- [Interpretability](https://www.anthropic.com/research/team/interpretability)
- [A global workspace in language models (J-space)](https://www.anthropic.com/research/global-workspace)

####

Links:
- [Inside DeepSeek's DSpark](https://deepseek.ai/blog/inside-deepseek-dspark-lossless-inference)

## Training

####
We've seen how the LLM using pure math can produce "the likely next token".

But how do they learn that?

Let's start with this question: Are they actually all the same?

### Are AI models "really all the same?"
<img src="images/llm/training/chatgpt-lingo.png">

####
Admittedly I coached ChatGPT into dialing up its "chatgppt-ness" to the max before asking this question.

And honestly? It worked.

### How models are trained
<img src="images/llm/training/training.png">

####

Pretraining is where the model learns about language. Looking at vast amounts of text, it learns to predict the next token — nothing more. The result is a powerful but raw capability: it knows how language works, how facts relate, how arguments are structured. It has no personality, no values, no sense of what a "good" response looks like.

Post-training is where the model learns what an appropriate response is. This is where values, tone, refusal behaviors, and personality get baked in.

### Pre-training on "all sentences in the world"
<img src="images/llm/training/training-corpus.png">

####
The training material is pretty commonplace for all frontier models nowadays. It's in the order of 1-5% of Google's index.

### Model and embeddings are born via training

<div class="cols">
<div class="col-2">
	<img src="images/llm/training/training-example.png">
</div>
<div>

**Backpropagation**:

1. Run tokens through the network like at generate
2. Paths to the expected token are rewarded, others are punished
3. Adjust the full network, back to the embeddings
4. Causal masking trains all sub-strings, too
5. Train on a gazillion texts

</div>
</div>

####
Finally, rather unceremoniously: this is how both the model's weights and the embeddings get their values: by training immensely to find the right balance where all training texts produce the expected next token.

It works like this, in principle:

1. A well-known sentence minus the last token is passed through the full model network, all 96 or so layers.
2. The last token is expected as the output; here "stronger"
3. All the paths that produced that token get dialed up a notch and all others dialed a bit down - all back through those 96 layers, all the way back to the embedding itself
4. Now simply repeat this a gazillion times with the entire training corpus.
5. Eventually the network and embeddings, which were initially random, end up with values that generally produce the "likely next token" for all those trained sentences.

That's how the AI model and the embeddings are born.

And it's amazing that it works, and that it ends up producing embeddings that had a notion of "gender" and "sadness" etc.

### Backpropagation math is ...ok, let's move on...
<img src="images/llm/training/backpropagation.png">

####
It's taken some effort to figure out this math, but it's pretty simple to execute.

### A trained model = embeddings + weigths
<img src="images/llm/training/pre-trained-model.png">

####
A trained model therefore consists of two parts:

The embeddings, meanig the vector of numbers for each of the tokens.

And the AI models many billions of small factors, weights.

Once the training is completed, the embeddings and weights are frozen, never to be changed again. Not until they are used to kick-start training of the next model.

### Pre-training is expensive

- From scratch for a new model
  - costs **$200M-$1000M**
  - takes **4-8 months**
<br>
- From an existing model
  - costs 1-10% of full training
  - takes weeks or months

### _Pre-trained_ models are just autocomplete
<img src="images/llm/training/pre-training.png">

### _Post-training_ is what shapes the model
<div class="cols">
<img src="images/llm/training/post-training.png">
<div>

*Different personalities*

ChatGPT – Structured explainer

Gemini – Diligent researcher

Claude – Honest advisor

Grok – Radical truth-seeker

Meta AI – Powerful engineer

Mistral – Efficient European

DeepSeek –  Censored thinker

</div>
</div>

### Post-training: reinforce the <em>desired outcomes</em>
<img src="images/llm/training/reinforcement-learning.png">

### Reinforcement Learning by Feedback

**RLHF** - Reinforcement Learning from *Human Feedback* (declining)
**RLAIF** - Reinforcement Learning from *AI Feedback* (growing)
<br>

<img src="images/llm/training/reinforcement-training-trend.png">

####
Frontier labs almost universally outsource the bulk of RLHF annotation rather than hiring raters directly. The main intermediaries:

- Scale AI/Outlier — the dominant player, operating as an end-to-end data engine. Outlier handles LLM annotation, Remotasks handles visual/multimodal work. Scale is OpenAI's preferred fine-tuning partner and has also worked with Meta, Google DeepMind, and others. Taskmonk AI
- Surge AI — Anthropic's primary RLHF provider, with ~50,000 expert contractors. Also used by OpenAI and Meta. Taskmonk AI
- Invisible — shifted from executive VA services to RLHF work for labs including Microsoft, Cohere, and Mistral. Routes model outputs through trained raters who score completions and rank outputs. Sacra

Outlier alone runs a network of 700,000+ contractors globally. The work is heavily gig-economy in structure.

Pay ranges from $15/hr for generalist annotators up to $500+/hr for domain experts like medical fellows and legal professionals. Invisible charges labs $30–45/hr for annotation work while paying raters $15–20/hr.

Each major frontier AI lab spends approximately $1 billion per year on human-generated training data, according to a 2025 Time Magazine investigation.

### Example: Claude's Constitution
<img src="images/llm/training/claudes-constitution.png">

####
In order to use AI for performing this Reinforcement Learning, Anthropic has written down their intentions for how Claude should behave in what they call *Claude's Constitution*. It can surely be read by humans, but it's primary target is actually to be read by AI's themselves to help decide whether answer A or B is most in line with Anthropic's values.

####
Links:
- [Claude’s Constitution - Anthropic](https://www.anthropic.com/constitution)
- [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)

### Expresses Claude’s "core principles"
<img src="images/llm/training/claudes-constitution-helpfulness.png">

####
Claude's constitution defines a priority ordering that the model should strive to follow:

- Broadly safe (supporting human oversight)
- Broadly ethical (good values, honesty)
- Adherent to Anthropic's principles
- Genuinely helpful

### "Don't foster excessive engagement"
<img src="images/llm/training/claudes-constitution-sychophant.png">

####
For example, Claude has been explicitly trained not to "foster excessive engagement".

You may question whether Claude really does adhere to these principles. One piece of evidence comes from the AI jailbreaking community, which is maximally adversarial and has zero loyalty to Anthropic; findings by such groups has not found behavior that is inconsistent with the constitution.

So the postulate that "It just wants to please you" doesn't line up with Claude's stated objectives.

### "New model is 36% more ..."
<img src="images/llm/training/system-cards-opus48.png">

####
The stated principles in the constitution is also how Anthropic can objectively measure differences in behavior when new models are released: adherence to their stated principles can simply be measured.

Links:
- [Model system cards](https://www.anthropic.com/system-cards)

### ChatGPT - rules over principles
<img src="images/llm/training/openai-spec-example.png">

####
OpenAI has something similar, but seem more focused on "rules" than "principles".

Gemini also has training guidelines:

<img src="images/llm/training/gemini-ai-principles.png">

####
Google has also published training guidelines for Gemini.

### Are models different?<br>Yes, indeed

### Same facts, different values and behaviors

<img src="images/llm/training/model-behavior.svg">
<br>

- Anthropic wants Claude to *reason from principles* — no rulebook needed
- OpenAI wants ChatGPT to *follow their spec* — rules written down explicitly
- Google wants Gemini to *behave correctly* — but via unpublished rules
- Meta wants Llama *powerful and open* — open weights, few restrictions
- Mistral wants Vibe *capable, open, and European* —  compliant, not principled
- DeepSeek wants its models *helpful and harmless* — as defined by the state
- xAI wants Grok to *tell the truth* — no censorship, no moralizing, no wokeness

### Models also have variations

Haikku, Sonnet, and Opus are really three different models.

They run on *different hardware* and their LLM has *different sizes*.
<br>

<img src="images/llm/training/claude-family.png">

####
For example, the Claude family are physically three different models: different size, training, speed, cost, strengths.



### Trained AI model recap
- You give it a string of tokens, aka the *context*
<br>
- The model produce a response by running that context through *the Transformer*
<br>
- The models have been *post-trained differently* for different desired behaviors
<br>
- The model can *only reason about the context*
<br>
- It's *all just math*, fixed at the time of training

### Let's revisit what Claude itself said
<img src="images/llm/claude-please-tell-me.png">


---
<img src="images/llm/nerdflix.png">

####
If you find this interesing then I can remommend this 2-hour video of Andrej Karpathy building a small GPT model, fully.

The whole thing is only 600 lines of Python code: 300 for `train.py`, 300 lines for `model.py`.

Links:
- [Let's build GPT from scratch (2 hours)](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- [Let's reproduce GPT-2 (4 hours)](https://www.youtube.com/watch?v=l8pRSuU81PU)
- [Github repo for nanoGPT](https://github.com/karpathy/nanoGPT)
- [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)
- [Hands-On-Large-Language-Models](https://github.com/handsOnLLM/Hands-On-Large-Language-Models)


# AI Agents

####
Now that we've seen how the LLM works, and learned a bit about tokens and embeddings, it's time to take a step up and see how we actually can use the LLM. How do we interact with it, for starters?

---
<img src="images/overview/agent.png" />

### So, do you speak to the LLM?
<img src="images/agents/hello/user-ai.png" />

### No, you always speak via an agent
<img src="images/agents/hello/user-agent-ai.png" />

####
The agent knows who you are. it knows your preferences. It adds extra context to every conversation you have with the AI.

For instance today's date, your name, your language preference, the most relevant facts it knows from earlier chats. Also any custom instructions, like skills, that you've added to your agent.

By the way, the word "agent" is so over-loaded. Here it simply means "the program you use to talk to the AI with".

### The AI-service is "the AI"
<img src="images/agents/hello/all.png" />

####
The LLM (Large Language Model) is the brain of the operation. As we've seen, the LLM is functionally simple: it only produce one token at a time and it can't "do" anything. So it needs some extra surrounding functionality to be really be useful, like be able to complete a full sentence, browse the web, read documents, etc. It needs some body, some hands and eyes. The AI service provides that body.

### You 💕 agent; the AI is completely impersonal
<img src="images/agents/parts/user-and-ai.png" />

####
The agent is your buddy. It holds your information, your files, your custom instructions, etc.

The AI service itself knows nothing about you, except that you're allowed to login and use it.

### The parts and their many confusing names
<img src="images/agents/parts/roles.png" />

####
You may be thinking: "But oh no, I'm just using Copilot in Word or chatpgt.com in my browser - not an agent".

Well, yes you are. Those are both agents. An agent is simply the tool you use to talk to the AI service with. It's a program, an app, a website, or it's an agent baked into some other app, like Outlook. The agent is also sometimes called "AI client" or "AI harness". To the AI-service it may present itself as "the assistant".

It's *not* an autonomous self-running James Bond-like entity. Well, except unfortunately those do exist and they're also called "agents", which is mighty confusing.

"LLM" and "AI model" are synonymous when we're talking about generative text AI; all AI models used for generating text (ChatGPT, Claude, Gemini, Grok, etc) are LLMs.

### Agents comes in many shapes
<img src="images/agents/agents/web-vs-cli.png" />

### gemini.google.com on the web is an agent
<img src="images/agents/agents/gemini.png" />

### So is Rovo, in Atlassian sidebar
<img src="images/agents/agents/rovo.png" />

### And PDF remediate, inside Siteimprove
<img src="images/agents/agents/siteimprove.png" />

### Google's agy, in the terminal/CLI
<img src="images/agents/agents/antigravity.png" />

####
CLI means Command Line Interface, i.e. in a text-based terminal.

### Claude Desktop is a dedicated agent-app
<img src="images/agents/agents/claude.png" />

####
Not in some unrelated app, not in the browser - no, in its *own* app, that can for example read and create files.

### Every agent is its own silo
<img src="images/agents/skills-example.png" />

####
Generally the only thing that the AI service knows about you is your name, identity, and account-information; your subscription plan, usage, etc.

Everything else is something that the agent provide you: your profile, memory files, skills, mcp servers, etc. And also the agents behavior: system prompt, tone, modes, language, etc. It all lives in the agent.

That explains why you, say, can't see skills that you've added online at claude.ai when using Claude Code in the terminal. Or even see the same skills when using Claude Code in Linux and Windows. They are simply different agents and each comes with their own capabilities and settings.

And yes, it's maybe a tad unexpected that "claude.ai" is not actually the AI service as such, but in fact just an agent just like Claude Code in the terminal is.

At least that's how it *usually* is today. It's changing slowly, it seems, and that's nice because it's annoying that your settings etc follow the installation, not your profile. It's just not an area that has gotten a lot of attention.

So now you know why the settings, like Skills, you set online at claude.ai are not available in Claude Code.

## My personal AI-journey

### Chat, copy-paste, embedded, now terminal
<img src="images/agents/evolution.png" />

####
I started chatting just in the browser, of course. And I still do, by the way.

Next I started writing code with the AI, but copy-pasted the code into my code editors to compile and run it.

Then I started working with the AI inside the code editor for true cooperation. It was a relief and performance-boost to have the AI work directly on my files in my folders.

Since late 2025 I'm now exclusively coding by running the AI in a terminal and having an editor open with the files. Much bigger window to engage with the AI in, much better control.

### I still use the browser chat

<img src="images/agents/ai-tech-talk.png" />

####
For anything that doesn't involve files I still just chat in the browser.

For this presentation I created a project in claude.ai for all the research. It has over 60 chats and I've prompted about 18,000 words which is about the length of Shakespeare's Macbeth. I'll leave it to the bard to comment on my efforts:

*It is a tale
Told by an idiot, full of sound and fury,
Signifying nothing.*


# The AI Service

####
Now we know how to "talk to the AI Service": via some agent app.

But what functionality does the AI Service actually add to the brain, the LLM?

That's the final piece of the puzzle, and it's much less complicated that the LLM itself. But you'll find that knowing about how the LLM works, knowing about embeddings for instance, will be quite helpful now.

This is the part where we finally unlock the concrete functionality you use daily: chatting, uploading files, having the AI work on that Confluence page using an MCP server, using a skill, etc etc. It all comes together now, and many parts are less mysterios than you might think.

---
<img src="images/overview/service.png">

### What does the AI service add?
<div class="cols">
<img src="images/agents/parts/ai-service.png" />
<div class="col-2" >

The full functionality is quite lean:

1. It can read *files* you upload
2. It can *chat* with you
3. It can *"think harder"*
4. It can use *tools*
<br>
5. It has *caching* and *safeguards*
</div>
</div>

### All AI Services generally looks like this
<img src="images/service/overview/blank.png">

### The LLM loop is the centerpiece
<img src="images/service/overview/llm.png">

### It's all about those <em>embeddings</em>
Remember, the Transformer works on *embeddings*
Text maps to tokens, each token has an embedding in the model
But ... what about *files*, like PDFs and images?
<br>

<img src="images/service/overview/transformer.png">

## Files
<img src="images/overview/files.png">

####
Because the LLM only works on embeddings we will, somewhat surprisingly maybe, first take a look at how files are handled by the AI service. How does it even understand documents or image?

### Files are also turned into embeddings
<img src="images/service/overview/files.png">

### Images
<img src="images/service/overview/images.png">

### Images are not handled via OCR (well, maybe a bit)
<img src="images/service/files/images/ocr.jpg">

### Images are understood in small patches
<img src="images/service/files/images/eagle.png">

### VLMs (Vision-Language Models)

- Everything *visual* ("claw of a predator bird") is learned from datasets of image+text
- VLMs also *learn characters* through that training
- Images are processed in patches (eg 24x24 pixels) to individual **patch embeddings**, which are then mapped into the same *embedding-space* as text
- Same approach for *video and audio*, if supported
- A hybrid approach has gained traction, using *OCR* for pure-text-looking images
<br>
- The end result: The model just receive embeddings, bits of "meaning". It doesn't know or care if they come from text, image patches, interpreted images, possibly OCR. The the LLM, *it's all just embeddings*.
<br>
- Note: A screenshot of text can easily result in *10x more context* than the raw text

####
Modern Multimodal LLMs (like GPT-4o, Gemini, and Claude) generally do not use a separate, traditional OCR engine (like Tesseract or Google Vision OCR) in their standard workflow. Instead, they treat text recognition as a purely visual task.

### Whatever approach, embeddings comes out
<img src="images/service/files/images/cat-advanced.png">

####
Whatever the image processing does, embeddings is what comes out of it.

### A closer look at multimodal embeddings
<img src="images/intro/journey/rabbit-hole-embeddings.png">

####
I suspect that the usefullness and power of embeddings, not least **multimodal embeddings**, might well come as the biggest surprise to most of you.

### Remember, embeddings characterizes "something"
<img src="images/llm/embeddings/three-embeddings.svg">

### Multimodal embeddings go beyond text
<img src="images/service/files/multimodal/multimodal-embeddings.svg">

####
Some lab trains their models on text, images, video, and audio together, to form a "unified embedding space" where for example the word "kitten", images of kittens, and sounds of kittens all are comparable embeddings. That kind of training is very expensive, which is why this is a very recent functionality (from spring, 2026).

A single embedding, however, is cheap to calculate. The effort is in the order an LLM producing one token, which is close to what's actually happening. You calculate it once and then you can store it (it's just numbers) in a database. From then on you can do easy and cheap similarity-matches for the embeddings.

(Of course, they should also store a reference to the thing they are an embedding of.)

The similarity-match is also called **cosine similarity**. And you will want to store the embeddings in a specialized database called a **vector database** that is optimal for that exact similarity-matching.

The dimension of a multimodal embedding is typically smaller than for text.

Links:
- [Gemini Embedding 2: Our first natively multimodal embedding model](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/)
- [Unleash the power of vector search and multimodal embeddings in BigQuery](https://www.youtube.com/watch?v=B-0dZGJDtJw)
- [What is a Vector Database? Powering Semantic Search & AI Applications](https://www.youtube.com/watch?v=gl1r1XV0SLw)

### The unified embedding space
<img src="images/service/files/multimodal/unified-embedding-space.webp">

####
Within the **unified embedding space** you can compare text, images, video, and audio to see how similar the concepts they represent are.

### Example: image-similarity
<img src="images/service/files/multimodal/gemini-2-query.png">

####
The query can be the embedding for an image.

### "Simply" compare the embedding's similarity
<img src="images/service/files/multimodal/gemini-2-similarities.png">

####
Cosine similarity will show how similar two embeddings are.

### A world of ideas for comparing any two things
<img src="images/service/files/multimodal/ideas.png">

### New tech (spring 2026) with limitations
<img src="images/service/files/multimodal/gemini-2-overview.png">

####
The technology is rather new and there are some restrictions on what you can calculate embedding of.

---
<img src="images/service/files/multimodal/gemini-2-embeddings.webp">

####
Google's offering is called "Gemini Embedding 2"

---
<img src="images/service/files/multimodal/amazon-nova-2.jpg">

####
Amazon's is called "Amazon Nova 2"

### PDFs and other documents
<img src="images/service/overview/documents.png">

####
Now let's look at documents.

####
PDFs are handled really well. The AI services gets better and better at handling documents, like eg zip-files or Word- or Excel-files.

Documents doesn't really introduce any new functionality: they contain text and images and those parts are either extracted, of the document is rendered in full and then image-recognized.

### Should you convert PDFs to markdown yourself?
<img src="images/service/files/pdfs/94pct-savings.png">

####
PDFs are a wilderness. They're really hard to extract text and structure from - much harder than HTML. They contain binary parts, the internal structure is a jungle beyond description of stacked objects, drawings, and text parts.

Because of that there's a beliefe that passing a PDF raw to the LLM has a masive overhead. So the sentiment everywhere is: "Of course you should extract the text yourself first, it's absolutely foolish not to."

Or is it?

Think about it: Is it reasonable to think that you, on your computer with some tools, can achieve a much better result than Anthropic, Google, and OpenAI can when it comes to grabbing the meaning out of PDFs? Not just plain text but also images, structure, tables, footnotes, etc?

### Experiment: 10 PDFs, compare markdown vs raw
<img src="images/service/files/pdfs/experiment-pdfs.png">

####
I ran an rigorous experiment where I examined how Claude, Gemini, and ChatGPT dealt with 10 PDFs of varying sizes and content. They all understood the PDFs really well, but their approach was really surprising.

### It depends
- *ChatGPT* did text-extraction completely similar to what I did locally.<br>Raw PDF and markdown had practically the same token cost.<br>*No need for local conversion to markdown*
<br>
- *Gemini* processes PDFs as pure vision input at a flat rate of 258 tokens per page!<br>That was 3-18x fewer tokens than converted markdown.<br>*Give Gemini raw PDFs, not converted markdown*
<br>
- *Claude* also renders and treats each page as an image, but not at a flat rate.<br>Token-usage for raw PDF was 2-6x more than markdown.<br>It pays off to do local markdown conversion*.

####
Google's Gemini behavior was a surprise. It's even a very deliberate decision by Google, based on research. They slice the image up in 24x24 pixel squares, 16 patches per side ie 256 patches in total, each needing one embedding. Plus 2 more for some reason, for a total of 258 embeddings in the context. That's hard to beat and the PDFs were really well understood.

Links:
- [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (Dosovitskiy et al., 2020)](https://arxiv.org/pdf/2010.11929)
- [PaLI-3 Vision Language Models: Smaller, Faster, Stronger (Chen et al., 2023)](https://arxiv.org/pdf/2310.09199)

## Chatting
<img src="images/overview/chatting.png">

####
With files and images out of the way, let's look at actually chatting with the AI service.

Let's remember: You give the LLM a string of tokens, aka the *context*, and it will produce a response based on the model's baked-in training by running that context through the Transformer. Pure math and trained knowledge.

That is *all* the LLM can do. It can't browse the web, multiply two large numbers, read a file, remember anything about you, no nothing. It can only run the context through the Transformer to produce a response.

### Let's continue the example chat
<img src="images/service/chat/chat.png">

### You write, the AI responds
<img src="images/service/chat/chat-turn-1.png">

### You respond again - but now what?
<img src="images/service/chat/chat-turn-2-question.png">

### Question: What is sent to the AI?
<img src="images/service/chat/chat-turn-2-choice.png">

### Option B: the full chat
<img src="images/service/chat/chat-turn-2.png">

### The full chat is always, always sent to the AI
<img src="images/service/chat/chat-turn-goodnight.png">

####
Let that sink in: every message you send, resends the full conversation.

### Why? Because the LLM need the full context

The LLM can only reason about *the context it is given*.
<br>
It does not, it *cannot*, know or reason about *anything else* than what is in the context.<br>The LLM is completely *stateless*.
<br>
You want it to know about X, beyond its trained facts? Then X must be *in the context*.
<br>
No links, no outside preferences, no memories, including from earlier chats:<br>the context is *ALL* the LLM can respond to.

### The context after 3 prompts
<img src="images/service/chat/tokens-turn-3.png">

### The context after 50 prompts
<img src="images/service/chat/tokens-turn-50.png">

### The total is 1+2+3+...N = O(N²) messages
<img src="images/service/chat/tokens-turn-50-total.png">

####
The total tokens you pay for is added up for every turn, so you use more and more tokens at every turn.

### Save tokens: clear and compact

####
The best way to save tokens is simply to not keep on dragging the entire conversation along all the time.

### Clear: wipe all, get back to scratch
<img src="images/service/chat/clear.png">

####
"Clear" simply means wiping the entire chat and starting from scratch.

### Compact: keep a summary of the chat
<img src="images/service/chat/compact.png">

####
"Compact" means that the agent ask the LLM to summarize the chat and add that summary as a first message.

### Your best token-saving friends: clear and compact
- Write `/clear` or `/compact` or just start a new chat
<br>
- Compact doesn't use that many more tokens
<br>
- If you don't, the agent will auto-compact for you
<br>
The token-cost rather complicated; more later

####
Many agents also offer ways of branching or editing or backtracking on your messages.

For example Claude has `/btw` to send a message out-of-band.

### Chatting recap

- The full chat is always sent, every time
<br>
- Keep the context lean

## Thinking
<img src="images/overview/thinking.png">

### What could "thinking" mean?

- Maybe the can be tweaked to "think better"?<br>*Hmm, no - the LLM weights are constant numbers, frozen after training.*
<br>
- Is there a "bigger AI" stashed away in the back room?<br>*But then how could the biggest models think harder too?*
<br>
- But wait. Is what we do here "thinking"?<br>*That's a bingo!*

### Thinking is: contemplate, append, repeat
<img src="images/service/overview/thinking.png">

### Chain of Thought
Thinking (aka effort, reasoning, ...) is called **Chain of Thought**, or **CoT**
&nbsp;
1. Inject a special *<let me think about that>-token*, known from training
2. That token makes the LLM *comtemplate*, rather than seek to respond
3. Keep producing, appending, and processing **thinking blocks**, refining the LLM's understanding of the matter until the LLM says "thinking completed" or the allotted **thinking budget** is exceeded
4. Blocks are also sent to the agent, which may show them to you in its UI

### Example thinking blocks - "No, wait"
<img src="images/service/thinking/now-i-understand.png">

####
Thinking generally produce a better result and the model can catch itself if it's going down the wrong path.

However, it can possibly also strengthen a misbelief.

### Thinking typically improves the response
<img src="images/service/thinking/haiku.png">

####
Without "Extended thinking", the LLM failed to produce a proper Haiku. The syllable-counting Haiku format is hard for the LLM to produce just one token at a time.

### You control the thinking effort
<img src="images/service/thinking/claude-code-enable-thinking.png">

####
You can enable thinking in all kinds of manners.

Nowadays, it's often simply enabled by default, or even automatically controlled.

### Saying "ultrathink" has been on, off, on
<img src="images/service/thinking/ultrathink.png">

####
In early days, this was how Claude Code controlled the thinking.

Then it was taken out to be replaced with a "proper" thinking-setting.

But lo and behold: it was added back in in Claude Code v2.1.68, so the convenience of just being able to write "ultrathink" must have been missed.

### A penny for your thoughts
- Thinking-blocks are output tokens, and then input-tokens, so they cost you, too.
&nbsp;
- For reasoning-heavy tasks, thinking tokens can therefore easily multiply your effective output costs by 10x.
&nbsp;
- However, thinking-blocks are (typically) *not included* in the context after this turn, even though the agent's UI may still show them. Only the final response *after the thinking* is kept in the context for the next turns. So they will cost you, but not "keep on costing you".

<img src="images/service/thinking/claude-code-thinking.png">


## Tools
<img src="images/overview/tools.png" />

####
So far, we've only seen the LLM generate text.

Using *tools* is how the LLM can seek out new facts and generally, surprisingly maybe, be *in control*.

### The LLM can ask to "use tool xxx"
<img src="images/service/overview/tools.png" />

####
Meaning: The LLM can predict that the best continuation is output that *asks for some tool to be run*. The output from that tool will then be added to the context, practically as if the user had added it themselves.

### "calculate 123442873893*98790237342"
<img src="images/service/tools/python-math-example/request.png" />

####
This is how the actual agent-and-service communication would look like:

You, the user, send this text to the AI: "please calculate 123442873893*98790237342".

However, the agent *also includes info about tools* that is makes available, to be added to the context.

And breaking with all we've seen so far, the server can actually *also add some tools* to the context for the LLM to run. For instance, Anthropic's AI server has a Linux environment with Python interpreters and can fetch web-pages without having to delegate that effort back to the agent.

In this situation there's a tool called "code_interpreter" with the description "Executes Python code and returns the result", taking a string-argument of Python code. **Python** is a popular programming language that the LLM during training has seen millions of examples of.

### LLM asks to use tool "code_interpreter"
<img src="images/service/tools/python-math-example/tool-use.png" />

####
Based on the training, the LLM decides that the best continuation from the user saying "please calculate 123442873893*98790237342" is to call a suitable tool that can do math. The "code_interpreter" seems like such a suitable tool.

So the LLM's output asks for a "tool_use" of that tool, conjuring up the suitable Python code snippet `print(123442873893 * 98790237342)` from its massive training on Python code.

As an aside: the tool-training is commonly done using a process called *Toolformer*.

In *Toolformer*, Schick et al. had a base LM propose where API calls might go in ordinary text, then actually executed those calls, and kept an insertion only if having the call and result demonstrably helped predict what came next (reduced the model's loss on subsequent tokens). The process is self-supervised: usefulness is not defined by human judgement but purely mathematically as "did this make the future more predictable?".

Links:
- [Toolformer: AI learns to use APIs - AssemblyAI](https://www.youtube.com/watch?v=LxZ3gYvbV7I)  (5 min)
- [Timo Schick | Toolformer: Language Models Can Teach Themselves to Use Tools](https://www.youtube.com/watch?v=UID_oXuN-0Y) (55 min)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/pdf/2302.04761)

### The tools is being run (on agent or server)
<img src="images/service/tools/python-math-example/tool-result.png" />

####
If the tool is server-side then the server runs it. Otherwise it goes all the way back to the client. As mentioned, running Python code or fetching webpages is typically done by the server. Reading or creating local files can of course only be done by the agent on the user's computer.

At any rate, the tool runs, the output is added to the context, and the new context is passed back into the LLM for another pass.

### Finally, the LLM can respond
<img src="images/service/tools/python-math-example/response.png" />

####
With that added context from the tool, the LLM can finally produce a nice and correct answer.

### The anatomy of a tool definition
<img src="images/service/tools/tools-list.png" />

####
Every tool speficies the name of the tool, a description of what the tool does, and details on how to call it.

The information is so detailed that the LLM can make sane decisions on whether calling the tool would be useful or not. Of course, in order for the LLM to see it, the tool-information will need to actually be part of the context - how else would the LLM know about it?

So tools can take up a fair chunk of the context.

### Tools: the so-called "agentic loop"
<img src="images/service/tools/the-agentic-loop.png" />

####
The introduction of this "tool loop" lead to the name, "the agentic loop": an agent using tools until a goal is reached.

####
Links:
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)

### The LLM is in control - via tools

*However*, tools can be much more than just doing math, file, or web operations.
&nbsp;
Practically every *decision* in the interaction you have with the agent and AI service, is actually *conjured up by the LLM*. The agent and service is predominantly simply *carrying out the LLM's bidding* about practically everything:
<br>

<div class="cols">
<div>

- Calling tools
- Asking the user
- Planning vs doing
- Orchestrating agents
</div>
<div>

- Parallel vs sequential tool calls
- What to remember
- Whether to trust a result
- When to stop
</div>
</div>

####
- *Calling tools*: Which tool, with what inputs, and whether to call several in parallel or sequentially. If two tools could both answer a question, the model picks.

- *Asking the user*: When ambiguity is worth resolving vs just attempting. The model decides whether a question is clarifying or unnecessary interruption.

- *Planning vs doing*: Decomposing a task into steps first, or just starting. Related: how many steps, in what order.

- *Orchestrating agents*: Spawning subagents, assigning subtasks, deciding when verification by a second agent is worth the cost.

- *Parallel vs sequential tool calls*: If the client supports parallel tool use, the model decides which calls are independent enough to run simultaneously vs which must wait for a prior result.

- *What to remember*: If given a memory tool, the model decides what's worth storing, what to overwrite, and what to let expire. Surprisingly consequential over long sessions.

- *Whether to trust a result*: After a tool returns, the model decides whether the result looks plausible or whether to sanity-check it via a second tool or its own reasoning. A search result that seems off might trigger a follow-up search.

- *When to stop*: In an agentic loop, the model decides when the task is genuinely done vs when it should keep going. end_turn is its call, and getting this wrong in either direction is a real failure mode.

### Example: starting background workers
<img src="images/service/tools/background-worker.png" />

####
For example, the agent is not the one making the decision when to actually *run* another background agent: it is *the LLM* that makes that decision. The agent simply has to provide a named tool, a mechanism, for actually running background agents.

So in a way it's "easy" to write an agent: just provide well-described tools that the LLM can work with: like "ask the user", "delete a file", "start multiple agents", etc. The LLM will then decide to call them.

### The home-field advantage
- Models are trained on their own lab's tools.
<br>
- When Claude runs inside Copilot, the tools Copilot hands it don't match what Claude was trained on. Claude can generalise, but the fine-tuned judgment of when and how to use each primitive doesn't transfer perfectly. The agentic loop works the best when a model interacts with its buddy: the agent it's been trained with.
<br>
- That's why running *Claude Opus in Claude Code* can feel more smooth than running Opus inside *Copilot, Cursor, Perplexity,* or *OpenCode*. It's just a better fit.

### Ask the AI: "show me your tools for pages"
<img src="images/service/tools/rovo-ask-how-many-pages.png" />

####
Simply asking what tools are available can be a good way of finding inspiration for how to use that AI.

### "How many pages are in my own space?"
<img src="images/service/tools/rovo-ask-how-many-pages.png" />

####
Rovo does a number of tool calls to figure out that I have three pages in my personal Confluence space.

## MCP servers
<img src="images/overview/tools.png" />

####
Now that you know about the concept of using tools, let's move onto something very popular that is very related to tools: MCP servers.

But hang on, this looks exactly like the highlighting of "tools" from before?

Yes, that's right.

### MCP servers simply gives you ... more tools
<img src="images/service/overview/mcp.png">

####
MCP is a standardized way of giving the LLM access to tools outside the agent or server.

In principle *it works exactly like tools* that we've just covered.

The only difference is that the "list of tools" isn't baked into the agent or server, but instead fetched live from somewhere: an MCP server. And should the LLM decide to use one of the tools then yes, that same MCP server is what will handle the tool-call.

### MCP servers gives uniform access to tools
<img src="images/service/mcp/uniform-mcp-interface.png">

####
Having just one standard for using outside tools is a great advantage. The agent or server does not need to figure out how to seet what API services are available in many different ways. There's now just one way; the MCP protocol way: ask for tool-names and call a tool.

Links:
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/)

### An MCP server is "just" a middleman to a service
- An MCP server *does not itself bring new functionality into the world*.
<br>
- It's a middleman, *a standardized protocol*, that enable the AI Service to discover another service that exists somewhere.
<br>
- When somebody says _"You can add an MCP server for Atlassian"_, they're practically saying:<br>_"You can tell the AI about Atlassian's API"_.

####
Yes, it's really "just that". A live list of tools and a way to call them.

### Example: Atlassian MCP
<img src="images/service/mcp/atlassian-mcp-ask-how-many-pages.png">

####
Adding the Atlassian MCP server mean I have access to tools, just like Rovo used in the example before.

## An MCP tool-call in detail

####
Let's take a look at concretely how an MCP service is used.

### First, add the MCP server info to the agent
<img src="images/service/mcp/flow/1-add-server.png">

### You only need to do that once
<img src="images/service/mcp/flow/2-explain.png">

### The info is present in <em>every chat</em> you send
<img src="images/service/mcp/flow/3-request.png">

####
The agent, or more likely server, will fetch the list of tools from the MCP servers and cache them.

Then it will add information about each MCP server tool to the context.

It *used* to be that the full information was added to the context, but that simply became too big. So the modern behavior is actually to *only add the tool-name* which can be maximum 64 characters, and that name is *the only guidance* the LLM will get about that tool. So you'd better pick descriptive names for yout MCP tools.

<!--### Add full info if the LLM want to use a tool-->
<!--<img src="images/service/mcp/flow/4-tool-search.png">-->

### LLM decides, MCP server calls
<img src="images/service/mcp/flow/5-tool-use.png">

####
The AI is talking to an MCP server, which is turn call some API.

The MCP server acts on your behalf, authenticated with your personal API key that gives it the same access you would have.

So for using an MCP server you must always be "a user" on the service behind it, like Github, Figma, Datadog, or Siteimprove.

### The LLM can now respond
<img src="images/service/mcp/flow/6-response.png">

####
With the tool-result from the service added to the context, the LLM can now compose a proper response.

### Example: Siteimprove MCP demo

####
"It's simple", I said. Okay, let me show how.

### In 1 hour, a demo MCP server was coded and live
<img src="images/service/mcp/siteimprove/github-source.png">

####
This was the first time ever I build an MCP server. I basically told Claude, "here's Siteimprove's public API documentation, please build an MCP server for it and suggest where to deploy it". I ended up deploying it on a free account on [Cloudflare](https://www.cloudflare.com/).

The hardest part was actually that the tool-names were limited to 64 characters and Siteimprove's API's endpoints often exceeded that, so the names had to be compacted somehow; like renaming "quality_assurance" to just "qa".

There's nothing secret about this MCP server for Siteimprove's public API. Any Siteimprove-user with an API key can use it, and anybody can build an MCP server just like it since Siteimprove's API is publicly available with each API endpoint fully described.

Links:
- [Siteimprove MCP demo source](https://github.com/ricflams/techtalk-ai-demystified/tree/main/demo/siteimprove-mcp)
- [Siteimprove MCP demo, live tool list](https://siteimprove-mcp.ricflams.workers.dev/show_me_what_you_got)

### Siteimprove API doc, OpenAPI doc, and MCP doc
<div class="cols">
<img src="images/service/mcp/siteimprove/tool-in-docs.png">
<img src="images/service/mcp/siteimprove/tool-in-openapi-spec.png">
<img src="images/service/mcp/siteimprove/tool-in-mcp.png">
</div>

####
The API docs, the OpenAPI spec, and the MCP version of the Siteimprove API's endpoint for [/sites/{site_id}/analytics/content/most_popular_pages](https://api.siteimprove.com/v2/documentation#/Analytics/get_sites__site_id__analytics_content_most_popular_pages)

The MCP variant looks very much like the existing OpenAPI spec for that endpoint, from which the API documentation is generated.

### Add the demo MCP server to Claude
<img src="images/service/mcp/siteimprove/github-readme.png">

####
Links:
- [Connect to Claude.ai](https://github.com/ricflams/techtalk-ai-demystified/tree/main/demo/siteimprove-mcp#connect-to-claudeai)

### All 531 endpoins/tools now available in Claude
<img src="images/service/mcp/siteimprove/mcp-connector.png">

####
Under Connectors you can see all the individual tools exposed by the Siteimprove demo MCP server.

### Need to authenticate on the first usage
<img src="images/service/mcp/siteimprove/authenticate.png">

####
This page is produced by my demo code, so an MCP server can style it just as it pleases.

### Claude can now call Siteimprove MCP tools
<img src="images/service/mcp/siteimprove/chat.png">

####
In order not to reveal actual page views I blacked out the reported numbers.

<!--### The MCP tools the LLM found and used-->
<!--<img src="images/service/mcp/siteimprove/chat-tool-use.png">-->

####
When I mention "most popular pages on siteimprove.com", the LLM correctly picks up that the tool "Siteimprove__analytics_content_most_popular_pages" would likely be useful, and asked for it to be called.

### All the included Siteimprove MCP tools
<img src="images/service/mcp/siteimprove/full-tool-list.png">

####
Yes, it took 10 screenshots to put this massive list together.

In reality, a massive API such as Siteimprove's would likely be better off by being divvied into chunks of functionality. That's a common pattern for really big APIs.

### MCP is massively popular
<img src="images/service/mcp/massive-mcp-server-list.png">

### Almost spoken about like some "magic" remedy
<img src="images/service/mcp/code-munch.png">


## The system prompt

####
Files, chatting, thinking, tools - just one major thing remains. And it's rather big: the system prompt.

### Final piece of the context
<img src="images/service/overview/chat-system.png">

### System prompt
- A **system prompt** is still *just plain text*
<br>
- The agent stuff *"whatever is useful to tell the LLM"* into "system prompts"
<br>
- You could have *written this text yourself* in a prompt (well, sort of)

### Actually, the system prompt _is_ obeyed more
<img src="images/service/system/prompt/training.png">

####
Through training, the LLM has learned that in case of a conflict between "system" instructions and "user" instructions, it should pay more heed to the system instructions. After all, the system instructions during training embodies the desired behavior and values of the model so the lab model makers will of course make sure that the system instructions are crafted to express the desired behavior.

This bias towards obeying the system-instructions are therefore baked into the LLM's weights and hence predictions.

But it is just that: a bias, a trained preference to lean towards, in particular in case of conflicting instructions.

Remember: in the LLM, *nothing is a hard rule*. it's all just textual instructions that carry more or less weight.

### Convincing Copilot/GPT4.1 to change its name
<img src="images/service/system/prompt/i-am-groot.png">

####
With enough "super-urgent" persuasion, my user message was prioritized over the system prompt.

However, all other models were not at all convinced and saw right through the presumed urgency.

### The system prompt is composed by the agent
<img src="images/service/system/prompt/maximillian.png">

####
The system prompt is entirely constructed by the agent. That's why you get quite different system prompts and behavior depending on what agent you use. So if you build your own agent then you can construct your own system prompt entirely.

### The full context
<img src="images/service/system/layer-of-instructions.png">

####
This figure illustrate two things:

- the relationship between your chat, the system prompt, and the LLM
- all the bits an agent typically put into the system prompt

The context consists of your prompts and the AI's responses, and the system prompt. As mentioned, the LLM has through training learned to obey system prompt instructions over plain user prompts, so placing instructions in the system prompt (for example in an agent-file) makes them more likely to be followed. For anything that you don't state in the context, the LLM will simply follow trained knowledge and behavior, which becomes better and better over time. Anthropic [blogged in July 2026](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) that they had removed 80% of the agent system prompt for Claude 5 models because the LLM now works better and many strict rules were unneeded or even counterproductive.

I've grouped the bits that agents put into the system prompt into three parts:

- *Red* are parts the agents invisibly adds, some of which you can control; your preferred language, for example
- *Green* is tools, which in the context typically is *a hint* of how to bring tools or more context into play: "hey LLM, if you need something related to Siteimprove pages then here's an MCP-call you can try out"
- *Blue* are prompts, text instructions, that you write yourself and ask the agent to include in every chat

You pay by token and the context has a limited size. The context comes at a cost and agents are therefore quite careful not to include just anything. An agent will *not include* earlier chats, browser history, your facebook profile, emails, some super-secretly stored information, etc. Not unless you explicitly (or implicitly via a tool) ask for it - many agents will let you search your chat history, if you ask to.

So when you find yourself wondering "How does it know that...?" or "Why doesn't it know that...?" then this gives you the answer: it knows about *just these parts* and they really aren't a secret in any way.

It's a lot, but let's very briefly go through the 11 parts. And again, remember: all of this included into every chat.

### #1/11: The agent system prompt

####
- Instructions that the agent (chatpgt.com, VS Code, Claude, Copilot, etc) wants included into every chat you have with the AI service.
<br>
- It brings information about the agent's name, purpose, behavior, etc.
<br>
- Generally, agents don't make it visible in their UI

####
Links:
- [How Claude Code Builds a System Promp](https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html)

### Claude's agent system prompts are public
<img src="images/service/system/prompt/claude-prompts.png">

####
Links:
- [Claude System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts)

### The "Copilot in Word" agent prompt
<img src="images/service/system/prompt/leaks-copiot-in-microsoft-word.png">

####
When you use Copilot in Microsoft Word, this is the system prompt.

### #2/11: System information

### Date, time, location, OS, etc
<img src="images/service/system/system-info/today.png">

### #3/11: Automatically stored memories

### Selected information from your chats
<img src="images/service/system/memory/memory-example.png">

####
The most important facts from your conversations, kept updated and curated by the agent. Completely visible and less verbose than you'd might expect. Look at the scrollbar: there's no more than 3-4 pages of text stored as memory about me after a year of chatting.

In terminal AI Agents, there can be multiple files with such "memories".

### #4/11: Some context from the agent

### Example: Rovo includes the current page
<img src="images/service/system/agent-context/rovo-context.png">

### Example: Visual Studio
<img src="images/service/system/agent-context/visual-studio.png">

### #5/11: Your preferences

### Example: ChatGPT can be "friendly" or "pragmatic"
<img src="images/service/system/preferences/chatgpp-personality.png">

####
The ChatGPT personality is implemented as two different set of instructions.

### Example: Language
<img src="images/service/system/preferences/language/claude-ai-language.png">

### Respond in Japanese, English, Dansk, ...
<img src="images/service/system/preferences/language/claude-code-set-language.png">

### Respond in Klingon
<img src="images/service/system/preferences/language/klingon.png">

### It's all just instructions, even the language preference
<img src="images/service/system/preferences/language/language-in-the-prompt.png">

####
No hidden commands. Just text. The LLM has no "fixed set of languages".

### "Modes" are also just text instructions
<img src="images/service/system/preferences/modes/enter-plan-mode.png">

<img src="images/service/system/preferences/modes/exited-plan-mode.png">

####
Modes are simply implemented as instructions that tell the LLM to plan or do, for instance.

Nowadays, each mode-change typicaally results in *adding a system message* instead of changing the base system prompt so the prompt is better cached on the server - more on this later. So a conversation can have many sequential instructions to "enter mode x" and "exit mode x".

### #6/11: Agent tools

### All tool names are included
<img src="images/service/tools/tools-list.png" />

####
It's quite possible that *only the tool's description* may be included in the context to save tokens, and that the LLM will have to express an interest in using the tool for the agent (or server) to feed in the full tool definition. That's part of the game of minimizing the up-front cost of tools.

### #7/11: Skills

### Hey, aren't skills a big deal?

####
Well, yes they are. But they belong here and are actually very simple.

---
<img src="images/service/system/skills/trinity.png" />

####
A skill is _some (expertise) instructions, that is loaded when you need it_.

### What's a skill?
- A skill is *text instructions* with a name
<br>
- A skill's instructions are loaded into the context on demand by you or the LLM:
	- Type `/skill-name` or just ask to _"use skill xxx to ..."_
	- The skill has a description so the LLM can ask to load the skill's content when it would seem useful, _just like for tools_

####
**Agent Skills** is an open standard, made by Anthropic and widely supported by agents

The above is a generalization; skills can be configured to e.g. not be callable by the LLM.

Links:
- [Agent Skills Overview](https://agentskills.io/home)

### What's a skill concretely?
- It's essentially a little folder - it can e.g. be distributed as *a zip-file*
- It *must* contain a file `SKILL.md` and *it can contain whatever else* the skill could need, with no upper limit; texts, files, images, whatever
<br>

<img src="images/service/system/skills/skill-anatomy.jpg" />

### Example: Using Matt Pocock's "grilling" skill
<img src="images/service/system/skills/skill-parts.png" />

####
The `SKILL.md` file has just two required fields, name and description, and a markdown body.

The name and description is always included in the system prompt.
(Actually, this seems to be a bug, since skills marked `disable-model-invocation: true` should not be included).

The full content is added as a `tool_result` message when the user or LLM ask for it.

The content is just text, so it will need to refer to other resources to bring them in. Just like you would do in a text prompt for a file: "use NOTES.md to ...".

That's it, really: a skill is useful (expert) knowledge, but in practice it's just a piece of text that you can bring in when you need it.

Links:
- [grilling skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)
- [Matt Pocock on Github](https://github.com/mattpocock)
- [Matt Pocock on Youtube](https://www.youtube.com/@mattpocockuk/videos)
- [How to Use Matt Pocock's Skills for Claude Code: A Complete Guide](https://tosea.ai/blog/matt-pocock-skills-claude-code-guide)
- [So I tried Matt's skills... - Theo](https://www.youtube.com/watch?v=0oXOOlqVu5M)

### Hey bro
<img src="images/service/system/skills/bro/bro-skill-code.png" />

####
Some skills are really simple. Like this one called `bro`:

It literally just writes this message into the context: "Restate your last message. Stop using jargon and speak coherently. State it more simply and concisely, like one human talking to another."

Links:
- [bro](https://github.com/backnotprop/bro)

### Installing the bro skill for terminal agents
<img src="images/service/system/skills/bro/bro-skill-install.png" />

####
Install skills like this using `npx skills add <repo-name>`.

### Bro in action
<img src="images/service/system/skills/bro/bro-skill-in-action.png" />

####
Thanks, bro.

### Installing skills

### Several ways for terminal/CLI agents
<img src="images/service/system/skills/install/cli.png" />

####
The skill repo usually tells you what the options are.

### Claude.ai: from Anthropic or your organization
<img src="images/service/system/skills/install/claude-ai-browse.png" />

####
On claude.ai you can install skills from Anthropic or from your organization, if you're a member of one.

### Claude.ai: upload a skill zip-file
<img src="images/service/system/skills/install/claude-ai-upload.png" />

####
The old-school, manual way: get the skill as a zip and upload it.

### ChatGPT call them plugins
<img src="images/service/system/skills/install/chatgpt-grilling.png" />

####
Matt Pocock's skills are also available in ChatGPT.

### Skills recap
- It's "just" snippets of text that you or the LLM can ask to *add to the chat*
&nbsp;
- Useful, sure, but has no special abilities
&nbsp;
- Like text-expansion: write `/bro` and bro's text is written out

### #8/11: MCP servers

####
We already covered them in detail. But there's one important thing to dig into: what the context include of hints about each tool so the LLM can decide to use it or not.

### Modern lazy-load: only include tool name
<img src="images/service/system/mcp/tool-definition.png">

####
It used to be rather expensive to include tools from MCP servers, because the full tool definition for all tools would be added to the context. Adding an MCP server would eat up 500 tokens per tool. The 500+ tools in the Siteimprove demo MCP service would fill about 250,000 tokens - crazy, of course. With a handful of MCP servers you would fill up an entire 1M context, just with tools.

Nowadays the full definition is typically *not included in the context*: only the tool name. That's referred to as **Lazy Schema Loading**.

This means that the tool name has to contain all the information that would make the LLM find it suitable to call to solve some problem. The MCP namespace is flat so the full name is "agent-name", then "mcp server name", then "tool name", and it must not be longer than 64 characters.

That's why the LLM may sometimes miss a suitable tool: it may simply not conclude that your prompting match a certain tool name because the tool names are so compact. If you ask for "the most popular pages on my Siteimprove sites" then it's a strong match, but if you just talked about "the top of those 1000 pages vith most page views" then it would match practically nothing in the tool name and the LLM would maybe not notice that this tool was suitable to call.

By the way: this demo name is problematic as it is 68 characters, so it should be shortened.

Links:
- [SEP-986: Specify Format for Tool Names](https://modelcontextprotocol.io/seps/986-specify-format-for-tool-names)

### Those tool names had better be very descriptive
<img src="images/service/system/mcp/token-length.png">

####
So nowadays, don't worry about adding MCP servers. But also be aware that you may have to be more deliberate and precise in how you phrase your prompts so the LLM has a chance to match it up against the MCP tool names. For instance, say "using the atlassian tools, I want to...."


### #9+10/11: Project and custom instructions

### Most agents offer "projects"
<img src="images/service/system/projects/project-windows-to-linux.png">

####
You can write instructions that is included in every chat related to a specific project or work that you're doing.

They go by many names: Projects, Gems, Custom GPTs, Spaces.

### Add general custom instructions
<img src="images/service/system/customize/all-agents.png">

####
In all agents, you can add custom instructions that are included in every chat.

it could be your preference for how the AI should talk or act.

If there's something in general about the agents behavior that you'd like to change then this is the place. For instance, I have added this line to help me improve my spelling:

"Silently ignore casual typos; gently flag systemic spelling blind spots as an aside."


### Example: "always provide a dinosaur-analogy"
<img src="images/service/system/customize/copilot-dinosaur-instruction.png">

####
As a silly example I added custom instructions to Copilot to always end every answer with a brief dinosaur-analogy.

### "Like a swift Velociraptor ..."
<img src="images/service/system/customize/copilot-dinosaur-chat.png">

####
I actually forgot I had added this, but surely remembered when later I returned to Copilot.

### #11/11: Agent files

### "Agent file"? An International File of Mystery?
<img src="images/service/system/agent-files/austin-powers.jpg">

####
An "agents" file sounds like some instruction for an autonomous, free-roaming agent of a kind. I think it sounds like instructions for something to *happen*. Maybe for starting an agent, possibly in the background doing some secret work?

### Simply custom instructions, but for CLI agents

<img src="images/service/system/agent-files/claude-md-dinosaur.png">

####
You're likely almost tired of me repeating "it's just more instructions to put into the system prompt". But agent-files are just that: the exact equivalent of custom (or project) instructions, only for the AI agents you run in the terminal.

### Names and locations - a bit of a jungle
- Agents used different names: `CLAUDE.md`, `GEMINI.md`, even `AGENT.md` (no s)
- By now, `AGENTS.md` is the agreed-upon standard name (hooray)
- Yet, Claude Code does not read `AGENTS.md`, only `CLAUDE.md` (oh dear)
- Agents differ in how they search for agent-files, up/down from folder to root
- Use e.g. `/init` to have Claude build an agent-file of useful facts from a folder
<br>
- Anyways, *agent-files are just more text*, added into the system prompt path
<br>

<img src="images/service/system/agent-files/agents-md.png">

####
Links:
- [AGENTS.md: A Standard for AI Coding Agents](https://kupczynski.info/posts/agents-md-a-standard-for-ai-coding-agents/)


### Putting it all together: a _real_ system prompt example
<img src="images/service/system/all/full.png">

####
We've been through it all, now. And I've said "it's just added to the system prompt", but it may still be a bit mysterious.

So let's get concrete and see what such an arbitrary system prompt looks like. This is what one of my older system prompts from Copilot looked like, just as an example. Four screenshots combined.

Let's check it out.

### Some names, facts, behaviors, ...
<img src="images/service/system/all/name-and-behavior.png">

### Oh, something <mandatory>, sounds important
<img src="images/service/system/all/something-mandatory.png">

### A bit on regex formatting and the available tools
<img src="images/service/system/all/regex-and-tools.png">

### MCP tool-names pop in, rather unceremoniously
<img src="images/service/system/all/mcp-tools.png">

### Ah, skills, nice to meet you
<img src="images/service/system/all/skills.png">

### The system prompt is just one big pile of text
<img src="images/service/system/shoveling.png">

####
The reason for showing you these snippets is to hammer in this fact:

At the end of the day, the "system prompt" is all just text. Words competing for the LLM's attention, having more or less authority, and filled with hints about how to bring in more context (tools, mcp, skills).

Yeah, you'll see some tags and markup, but that *markup is not rigorous rules*. The markup just convey some kind of structure. You or the agent could have chosen different tag-names, or written it in plain markdown with `##` headings, or used markdown bullet points, or HTML, etc. The exact formatting matters very little to the LLM, but the LLM does appreciate *the structure* it brings, just like human readers would.

## Filling the final blanks

### The final parts
<img src="images/service/overview/misc.png">

####
Four parts to mention:

- In addition to the text context, the request also does send along *some real hard parameters*: the **model**, the **temperature**, the **thinking budget** in tokens, and some other model-specific bits. In particular, the *temperature* adjusts the sampling of the next produced token: at temperature 0 the LLM will always pick the most probable next word. In pactice that leads to a weirdly clinical and un-appealing output. Higher temperature simply mean increased likelihood of choosing some of the less probably next tokens. Note though, that even for temperature 0 the LLM simply cannot guarantee it will produce the same output from the same input twice, because the hardware-parallelity in the GPU's matrix-calculations can vary and lead to minute floating-point-differences from one session to another.
- There are **safety classifiers** for content going in or coming out, that act as hard stops for inappropriate content. So even if you do somehow convince the LLM to produce a recipe for biochemical weapon that output will suffer a hard veto at the exit.
- The output usually contains *statistics* for number of tokens consumed and produced, among other things.
- And finally, **the KV-cache**. The AI Service and LLM knows nothing about you, but it does *cache* the calculations for a brief while. Nowadays it seem that 5 minutes is the common caching time. You simply *pay less* for the cached part, typically only 10%. So if you chat continuously and don't take more than 5 minute breaks then you'll save a lot of money. Wait 6 minutes and the cost is about 10x as high because the entire context has to be re-processed. In relation to that, the agent can set up to four explicit *cache markers*.

### "Now I have the full picture"
<img src="images/service/overview/full.png">

####
Indeed, this is the full overview of how any modern AI Service work, in principle.

# The Context

####
Everything we've looked at is about *putting tokens into a context* with the intent of steering the next prediction toward something useful.

---
<img src="images/context/its-the-context-economy-stupid.png">

####
But the context is finite and processing costs you per token.

So not just adding the right things, but also keeping the context lean, is the challenge.

The cost of tokens in the context has a couple of surprises in store.

### Advice for your context economy
- You *pay per token*; fixed price/token for API, or via *your quota* when using an agent.<br>*Output tokens* are typically *5 times* as expensive as input tokens<br>*Cached tokens cost 10%*, so continue your chat within 5 min (optional 1 hour) to save cost
<br>
- System, tools, results, images, docs eat many tokens; don't anguish over *your tiny prompt*
<br>
- Pack multiple asks into one; *"Yes, and also..."* and *"Looks fine. And now x and y..."*<br>Save tokens by being *be precise* about names of files, what the output should look like, etc
<br>
- *Starting a fresh chat* is the universal remedy to save tokens; summarize or compact first.<br>You can also ask the AI to *summarize your chat or results to a file*, then start fresh with that

### Token spree

<style scoped>
/* A slim slide margin is left around the iframe on purpose: it gives you
   somewhere to click to pull keyboard focus back out of the game, and keeps
   the on-screen navigation controls reachable. */
section { padding: 12px; display: flex; flex-direction: column; }
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

*[Open interactive version](https://ricflams.github.io/techtalk-ai-demystified/tokenspree/)*
</div>

####
Here's an interactive visualization of where your token costs go.

Try this:

- Click the "Per-turn cost" and see that *the first turn is un-cached* and that *outputs are more expensive*
- Click the "Total cost" to see what the total cost after 10 turns is
- Try turning off the cache and see that it would be 2-3x more expensive, and then turn it back on
- Let's increase the number of turns to, say, 30

Now let's spend some tokens. Try each spending spree, one by one:

- Add some MCP servers. They're actually not that expensive nowadays
- Upload a big document. Your chat carry that doc in every turn
- Helpful IDE/tools. Send the selected document, tool results
- Think harder. That can eat a lot of tokens and we hit the quota at turn 34. Try unchecking/checking "Discard thinking" to see what will happen if thinking isn't discarded.
- Long outputs, like producing code or documents. Expensive. Coindidentally, I first made this app online in Claude.ai and hit my quota.
- Bust the cache. It's expensive to be Away From Keyboard, or change the model
- Expensive model. Everything gets N times more costly.

Now add them all:

- MCP, doc, IDE - hey, what happened, why the the curve "break"?
- Going back to Per-turn tokens reveal that auto-compaction kicked in because the context window was only 200 K; up it to 1M and switch back to Total cost
- Think harder - now we reached the quota
- Long outputs - quota reached twice
- Bust cache - quota reached 4 times
- Expensive model - bam!

Mitigations:
- Try clear and compact. They save, of course, but it's a proper shield against the other token-spending ways.

# How to ...

### How to speak to the AI
- Just *speak plainly*, including small nugding words to avoid steering to coarsely
	- "I would mildly prefer xxx, but not if yyy"
<br>
- Be *precise* about *the goal you want*
	- Don't say "it's green" or "it should not be green" - say "it should be red"
<br>
- But also *don't be prescriptive* about exactly how the AI should *achieve* the goal
	- Instead, talk about the goal. "I want fluid layout, and the graph is the centerpiece"
<br>
- Using *examples* often produce much better output
<br>
- In Claude, use `/insight` to see how you're doing

####
Links:
- [Claude Academy](https://claude-academy.com/)
- [You're falling behind. It's time to catch up.](https://www.youtube.com/watch?v=Z9UxjmNF7b0)

####

### How to hold the AI
- Modern agentic workflows, controlled by the AI models via tools, often works so well that you frankly *don't really have to* instruct them in a special way.
<br>
- A successful agentic loop that has emerged is:
<br>
	1. Use *multiple agents* in an "orchestrator/worker" fashion
	2. Explicitly *verify the result* before claiming it's done
	3. Take *small steps*, setting and updating goals along the way
	4. Take *notes* (in files), which boosts reasoning very much (eg 3x)

####
Links:
- [Google: The New SDLC With Vibe Coding"](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding)
- [Mixture-of-Expert vs Multi-Agent Systems](https://gurusup.com/blog/moe-vs-multi-agent-systems)

### Yet constantly new trends, like "loop of loops"
<img src="images/guidance/nate-loop-of-loops.png">

####
Links:
- [AI Prompt Engineering: I Stopped Prompting One Task At A Time](https://www.youtube.com/watch?v=A4zMyjkL0Dc)
- [I guess we're writing loops now?](https://www.youtube.com/watch?v=iJVJwmCKW9o)


### How to keep up with the AI
Treat it as a tool in your professional toolbox.<br>Buy your *own* good hammer, like a carpenter would

A monthly subscription of $20 is a cheap investment

# Demystifications

####
Let's run through a quick series of myths and facts and demystify them.

### We don't know how the AI works
<p class="verdict no">Oh yes, we know <em>exactly</em> how the LLM works</p>

####
We know *exactly* how the math and code works, as you've seen throughout this presentation. The actual algorithms are still human-made, for now.

### We don't know what goes on inside the AI
<p class="verdict yes">Now <em>that's</em> true - we don't</p>

- We don't know what the dimensions or weights really "mean" or how facts are stored
<br>
- It was, and is, a genuine surprise that *the Transformer works as well as it does*

### "I included all of ..."<br>"The AI indexed the whole..."<br>"It read all the source code"
<p class="verdict no">No, it most likely <em>did not</em></p>

- Large data is typically *truncated*, *sampled*, or *compacted*
- The LLM will fight tooth and nail to *not include large files or much data*: it will only read the first 1000 lines, the first 20 files, 5 sampled Confluence-pages, even *write small scripts* to do a task, all to save context
- So *no*, if you have a lot of data it's likely *not all processed* collectively in one context
- That's why bits and pieces could be *missed*

### "I told it earlier, but now it has forgotten"
<p class="verdict yes">Yes, compaction will do that</p>

- The context is compacted (or truncated) when it gets close to the context window size.<br>So yes, the AI *can forget* what you've been talking about
<br>
- Extensive output, e.g. long tool-results, can cause this so it's possible that the AI forgets/compacts something you feel you've "just talked about".
<br>
- Keep your context lean: *clear*, *compact*, *start new chat*

### Use token-saving skills, like "Caveman"
<p class="verdict maybe">Be skeptical - can be more useless than useful</p>

- The "Caveman" skill originally was partly rooted in a *misunderstanding that brief prompt equals fewer tokens*, even proposing using ancient Chinese language *Wenyan* as a super-efficient, compact means of input; but neglecting that Wenyan does not capture the intent as well as plain English does and also that it only produced marginally fewer tokens compare to English, sometimes even more.
<br>
- Small function words *encode structure*, not just politeness. Prepositions and articles marks argument structure, and dropping them leaves the model guessing at your intent.
<br>
- *Terse can be okay:* "Fix null check line 40" works fine. *But "make good" is bad*.

####
Links:
- [Caveman](https://github.com/JuliusBrussee/caveman/blob/main/README.md)

### Better say "You are an expert xxxx..."
<p class="verdict maybe">Useful in some ways</p>

- No need to say this to *bring in competence* in an area; training has done that
<br>
- But useful for for asking for *a perspective*:
	- "you are a skeptical reviewer whose job is to find the flaw"
	- "explain as if to a junior dev who knows HTTP but not OAuth"

### A fine-tuned model would be better
<p class="verdict maybe">It's not the ideal you might imagine</p>

- Fine-tuning is rather expensive and hard
- It can even produce *overall worse results*
- Recent studies show modern frontier models outperforming fine-tuned models
&nbsp;
- Better alternatives
	- *plain models with RAG* for injecting domain knowledge
	- better *prompts* for context engineering
	- use *skills* and *tools* for reasoning workflows

####
Rich Sutton's acclaimed 2019 essay "The Bitter Lesson" argued that throughout AI history, generic methods that leverage compute (search, learning) have repeatedly beaten clever methods that encode human knowledge. Game playing, vision, speech — same pattern every time. Sutton's conclusion was uncomfortable: stop adding in rules of your own, just scale and generalize instead.

Links:
- [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
- [Is Fine-Tuning Still Needed? LLMs, RAG, & LoRA](https://www.youtube.com/watch?v=-W2JdSl1v48)
- [General-purpose large language models outperform specialized clinical AI tools on medical benchmarks](https://www.researchgate.net/publication/406992335_General-purpose_large_language_models_outperform_specialized_clinical_AI_tools_on_medical_benchmarks)

### The AI just wants to please you
<p class="verdict maybe">Some do, some don't</p>

- For example, Claude's training specifically *discourages pleasing behavior*
- The LLM continuation-reasoning does by its very nature tend to favor "continuing with the story so far", which generally means "playing along" with your postulates.
<br>
- Make sure to challenge the output
- Say e.g. "Roast this, poke holes and find the weak spots"

### The AI can't help hallucinating
<p class="verdict yes">True, but it can largely be mitigated</p>

- The model *doesn't know it's wrong* when it hallucinates, so there is no use in saying "don't hallucinate". Instead:
<br>
- Give it a *clear goal* it can finish
- Make *failure an explicit accepted continuation*; "if there's no King Johan then tell me"
- Have *another agent* supervise and assess the output

####
Interestingly, deeper reasoning (chain of thought) actually *lowers* the success rate for the LLM detecting nonsense a bit, which is known as the **Reasoning Trap**, or Paradox.

Links:
- [The Reasoning Trap: How Enhancing LLM Reasoning Amplifies Tool Hallucination](https://arxiv.org/html/2510.22977v1)

### Ask it "why it did that" and it will tell you
<p class="verdict no">No, don't trust that explanation</p>

- The reasoning, chain of thought, is over and done when you see the response. If you ask "why this?" then the LLM seek a plausible continuation of the context "response plus user questioning 'why this?'". That reasoning may very well have *nothing to do with how it actually arrived* at the response. So, it produces the most likely narrative to support that earlier response, possibly completely hallucinatory. "It must have been done so because ..."
- It may not always happen, for sure, but it may well happen.

### Say no to training, it'll leak your data
<p class="verdict maybe">No, only if you send your secrets relentlessly</p>

- *No words from your chat is actually remembered*
<br>
- "Use your data for training" means that your chat will be used just like the massive amounts of texts seen during pre-training. Training never stores the text but instead nudges billions of weights a tiny bit.
<br>
- The model only memorizes *repetitions*. Send your password once? Doesn't stick. Send it 10 times? Then it's *1000x* more likely to stick, due to an effect called *superlinearity*. Still, it takes rather massively repeatedly texts to make a dent in the model's weights.

### "Make no mistakes"
<p class="verdict no">Largely useless</p>

- It urges more carefulness, but that's already baked into modern models
<br>
- "Make no mistakes" does not point out what a mistake is. Instead, *describe exactly* how to verify the output. Don't say "be factual" but say "if a person-record has no year then write 0, don't just invent a date".

### Saying "please" costs a fortune and is useless
<p class="verdict no">No, it doesn't and no it isn't</p>

- "Please" is *one input token* and that cost really is neglible
- "Please" add *conversational structure* and make it clearer that you make a request
- "Please" is found in *productive successful conversations*, the pattern we're seeking
- Politeness is mirrored in the output. A terse and impolite respose is more prone to leave out something useful so it needs more follow-up chats.
&nbsp;
Some say *the best reason* for being polite is simply that:
&nbsp;
- It's good for *you*, even in simulated conversations: positive social behavior release oxytocin and dopamine, while an impolite demeanor release cortisol and adrenaline

### It must follow "YOU MUST NEVER DO xxx!"
<p class="verdict maybe">Relative emphasis works, but is no guarantee</p>

- Emphasis markers like "UPPER CASE" or `*bold*` just shifts probabilities but cannot guarantee anything.
<br>
- Emphasis is useful in a *relative* manner, for marking some instructions to me *more important* than others.
<br>
- Generally, don't expect to be able to control the LLM completely. It's just statistics.


### All AI models are the same after all
<p class="verdict no">No, not at all</p>

- They may well know basically *the same facts*
- But they have *very different behaviors and values*


### Does it understand?<br>Is the AI sentient?
<p class="verdict maybe">Maybe - experts disagree</p>

- The fact that the answer isn't a resounding *"no"* is astounding.
<br>
- *What even is understanding, sentience, consciousness*?
<br>
- LLMs have reinvigorated the linquistic science and debate. It's utterly fascinating.

####
Links:
- [Modern language models refute Chomsky’s approach to language](https://ling.auf.net/lingbuzz/007180/current.pdf)
- [Dissociating language and thought in large language models](https://arxiv.org/abs/2301.06627)
- [AI Pioneer Geoffrey Hinton: AI Is Conscious, Superintelligence is Coming, And We Should Be Worried](https://www.youtube.com/watch?v=p7t1Q_p2gZs)
- [Will AI outsmart human intelligence? - with 'Godfather of AI' Geoffrey Hinton](https://www.youtube.com/watch?v=IkdziSLYzHw)


# Takeaways

####
What a journey.

### Thank you, and remember

<br>
<div class="cols">
<img class="col-1" src="images/intro/github-com-ricflams-techtalk-ai-demystified.png">
<div class="col-4">

It's all *just text*, not rules

Keep your *context lean*

Try *the terminal*, maybe you'll like it

*Re-visit this* at ricflams.github.io/techtalk-ai-demystified/<br>in readable form with *plenty* more notes and links

</div>
</div>

<br>
<br>
Enjoy and don't dispair 😊
<br>
<img src="images/intro/two-years-behind.png">

####
Links:
- [AI Demystified repo](https://github.com/ricflams/techtalk-ai-demystified/)
- [You've Been Using AI the Hard Way (Use This Instead)](https://www.youtube.com/watch?v=MsQACpcuTkU)
- Best LLM resources, imho: [3blue1brown](https://www.3blue1brown.com/?topic=neural-networks)

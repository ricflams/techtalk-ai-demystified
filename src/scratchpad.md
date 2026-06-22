### Right here and now

* Right here ... *and*
* Right here *and* ... *now*
* Right here *and* *now*, your brain ... *is*
* Right here *and* *now*, your brain *is* predicting ... *the*
* Right here *and* *now*, your brain *is* predicting *the* ... *next*
* Right here *and* *now*, your brain *is* predicting *the* *next* ... *word*
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before ... *it*
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* ... *leaves*
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* *leaves* ... *my*
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* *leaves* *my* ... *mouth*

### Right here and now

* Right here ___
* Right here *and* ____
* Right here *and* *now*, your brain ____
* Right here *and* *now*, your brain *is* predicting ____
* Right here *and* *now*, your brain *is* predicting *the* ____
* Right here *and* *now*, your brain *is* predicting *the* *next* ____
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before ____
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* ____
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* *leaves* *my* ____
* Right here *and* *now*, your brain *is* predicting *the* *next* *word* before *it* *leaves* *my* *mouth*


### I bet you can predict the next word

<div>

1. Once upon a ___<br><br>

2. 1000 × 1000 is ___<br><br>

3. Friend: Knock knock
You: ___<br><br>

4. Tourist: What's the capital of Japan?
Guide: Tokyo.
Tourist: What language do they speak there?
Guide: ___

</div>





---
<img class="full" src="images/embedding/2d-90deg.png" />


---
<img class="full" src="images/embedding/2d-88deg.png" />


---
<img class="full" src="images/embedding/2d-60deg.png" />


---
<img class="full" src="images/embedding/2d-3d.png" />


---
<img class="full" src="images/embedding/superposition-explosion.png" />



### "I'm gonna stop you right there..."

When you hear people say this, it's ... just not true:
&nbsp;
_"I ran the AI on the source code ..."_
Questionable, because the AI will not fit "all the source code" in the context
&nbsp;
_"It has access to our marketing space in Confluence so it knows all about..."_
No. It can fetch from Confluence, yes, but the context doesn't hold all docs
&nbsp;
_"Maybe it remembered from earlier that..."_
Maybe. But only if that "thing from earlier" has somehow been put into the context
&nbsp;
_"It seem to become better at ..."_
Maybe. But only those improvements has somehow been put into the context



### Top 8 take-aways

* The LLMs knowledge itself is fixated after training
* The context is *ALL* the LLM knows about; if it's not in the context then the LLM does not know about it.
* Every time you send a prompt, the entire chat is re-processed
* &nbsp;
* &nbsp;
* &nbsp;
* &nbsp;
* &nbsp;
* &nbsp;



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
---
title: Breaking the First Rule of Starting a Blog
date: 2025-11-14
tags: [meta, blogging, AI, FastHTML, HTMX]
excerpt: My first (personal) blog post. I discuss the many good reasons to blog, the many available platforms for hosting a blog, and why I still felt the need to build my own.
---

# Breaking the First Rule of Starting a Blog

If you're reading these words, that means I have officially left my online comfort zone.

I have done a reasonable amount of writing over the years—essays, peer-reviewed papers, even a few blog posts for my old company—but this post is different: it will be my first time writing something that nobody asked for. I *read* and follow a huge number of blogs, and I have enormous admiration for the people who write them. Yet I've always cringed at the idea of writing my own.

Writing *anything* on the internet is actually a pretty uncharacteristic behaviour for me. I was thinking back recently to when I was learning to code in the pre-LLM days by trawling Stack Overflow; I would try to enumerate every possible way of rephrasing my search until I'd find a post describing a sufficiently similar problem to mine. Sometimes I would spend hours and still not quite find what I was looking for.[^1] When I was successful, I was so grateful to the other users who asked (and more so answered) the questions, though it never once occurred to me to submit my own! Some subconscious diffidence held me back. I viewed the internet as comprising two completely distinct groups: producers and consumers; those who engage and share openly online, and the digitally shy who observe from the sidelines.

This, then, is my leap from one camp to the other. It's taken me far longer than it should have, because there's a cardinal rule of starting a blog, and I knowingly and naïvely decided to break it. In this post, I'll explain my reasons, and I'll describe how my decision to build a blog led me on a journey through aspiration and exhilaration, briefly into despair, then finally to a renewed sense of optimism and appreciation for craft and mastery.

## Why to *Write* a Blog

In reading so many blogs over the years, I've stumbled across countless examples of the "Why you should start a blog" post.[^2] Normally, when a group engaging in an activity loudly encourages the masses to join them (e.g., crypto bros), healthy skepticism is warranted. With bloggers, though, I'm inclined to believe them. The message they peddle, of the overwhelmingly positive influence blogging has had on their lives, seems to me free of perverse incentives; there's no pyramid to climb, no tokens to pump. Evidently, I've been convinced.

This being my first post, I obviously can't comment on how blogging has affected my life, but I can briefly touch on some of the arguments that resonated with me:

**Writing helps you learn.** It forces you to clarify and organise your thoughts in ways that simply thinking never does. In the early days of my PhD, I repeatedly fell into the trap of delaying writing until I felt I had done enough for a complete and polished paper. Once I finally began, I would immediately identify holes in my understanding, alternative approaches I hadn't considered, or more compelling experiments I should have run.

**Writing builds a personal brand.** This idea (in fact, the very phrase *personal brand*) was something I had the most difficulty with, despite always being impressed, when interviewing candidates, by people who maintain blogs or personal portfolios. Rachel Thomas' blog post on [Making Peace With Personal Branding](https://rachel.fast.ai/posts/2017-12-18-personal-brand) helped me come round to the idea of engaging in the activity myself. Personal branding is more than the shallow self-promotion that pervades LinkedIn. It's simply about making high-quality work that you're proud of discoverable. A blog is like an extended CV that demonstrates not just credentials but technical competence, communication skills and thoughtfulness about your chosen industry.

**Writing is genuinely enjoyable.** It takes discipline and practice, but it's undeniably rewarding. I'm a pedantic and often painfully slow writer—*should that be an em-dash or a colon? Should the full stop be inside or outside the quotation marks? Should I address that split infinitive?*—but that frustration is counterbalanced by the satisfaction that comes from a cleverly constructed sentence or an elegantly explained idea.[^3]

**Publishing can lead to serendipitous opportunities.** At my old company, Agemo, we took some of the ideas we had been working on (e.g., branching, reflection, back-tracking in agentic systems) and applied them to the [ARC-AGI challenge](https://arcprize.org/), a global competition that measures progress against a famously difficult AI benchmark. Due to time constraints and other commercial priorities, we never formally entered the competition, but I packaged the work we had done into an open-source Python [library](https://github.com/agemoai/arcsolver) and wrote a couple of [blog posts](/blog?tags=ARC-AGI) about it. These posts caught the attention of François Chollet, creator of the challenge and renowned AI researcher, who was impressed enough to arrange a meeting at NeurIPS, which eventually led to him joining Agemo as a technical adviser. None of this would have happened if I'd simply kept the work internal.

![Meeting François Chollet](chollet-neurips.png)
*Meeting François Chollet at NeurIPS 2024*

There are plenty more arguments too: the articles I linked above each offer a slightly different set of interesting and compelling reasons to blog, and I encourage you to read them all. One point that they all seem to agree on, though, is that the first step is to just start writing. Pick Medium, Substack, or any other platform, and get on with it—you can always migrate to something fancier later. In Ben Kuhn's section on how to set up your blog, he explicitly states, "You are not allowed to spend more than 30 minutes on this part until you have written four blog posts!" Yet here I am, teaching myself web development from scratch.

## Why to *Build* a Blog

So I had my reasons to write—but I also had my excuses not to. It's one thing to recognise that writing a blog would be valuable; it's another to overcome years of digital shyness and actually press publish. For me, posting to a platform like Medium felt too much like social media, with all the pressures and self-consciousness that entails. I could just *see* how it would play out: I'd set up my profile (*"Follow me for weekly updates about all things AI!"*), write three disconnected posts over the course of a year to zero followers, which would sit there forever, mocking me and my hubris for ever thinking anyone would be interested in reading what I had to say. No, what I needed was a psychological scaffold, a project within which writing blog posts was just a part. I decided that teaching myself web development was that perfect project.   

And how hard could it be? When I formed this resolution, back in mid-2023, I felt emboldened by the seemingly limitless powers of these magical new AI tools, GPT-4 and Claude. However, if you're familiar with the *Gartner Hype Cycle* graph, you'll recognise the journey I was about to take...

![hype cycle graph](ai-hype-cycle.png)
*My Journey Along the Hype Cycle*

### The Peak of Inflated Expectations

At this point, my programming experience had been largely contained in an academic setting, using Python for data wrangling and implementing and training machine learning models. At work, I was getting exposed to more back-end engineering, architecting AI agents and workflows by chaining together API calls, but when it came to the front end, it's no word of exaggeration to say I didn't know the difference between HTML and CSS. As I used AI more and more for programming, my excitement built. My ambition grew too. I had always envied web developers and full-stack engineers, how they could take an idea and magic it into existence. Maybe, finally, thanks to AI, I was going to be able to learn how to program websites and *proper software*, not just ML models.

I began prompting. Within minutes, I had components, routing, state management. I'd describe what I wanted and watch thousands of lines of code materialise before my eyes. For a brief moment, it felt like a superpower; that is, until I made the foolish mistake of trying to figure out how it all worked.

### The Trough of Disillusionment

My excitement was quickly tempered when I began asking questions. I'd ask something like, "I see we're using React. Please explain what that is," to which the LLM would respond with a textbook definition: "React is a popular JavaScript library for building user interfaces, created and maintained by Meta. Here are the key things to know about it... Angular is a popular alternative developed and maintained by Google." When I'd ask why we'd chosen one over the other, I'd get back a totally non-committal answer explaining why both were great in different ways. The part of me that wanted to make sure I was doing things properly led me into complete frustration. I was overwhelmed by the sheer complexity of the front-end ecosystem, bombarded by words that were completely foreign to me—React, Next, Vue, Svelte, Vite, Node—libraries, frameworks (which are apparently different), bundlers, runtimes, build tools. What started out sounding like an exciting project began to feel like a fool's errand.

I have no ambition to become a front-end engineer; if I'm learning a new language, shouldn't it be something like Rust or Mojo that I could use in my actual job? One option was to just forget about learning and lean into *vibe coding*, but what would be the point in prompting my way to a website, generating a repository full of code that I don't understand in a language I know nothing about? I'd have no pride in it. It would feel like buying a London Marathon medal on eBay.

This realisation about web development was part of a growing disillusionment with AI tools more generally. Over time, the thrill of producing huge amounts of code had begun to fade, and I was noticing that I was disengaged. Even on simple tasks, I'd find myself completely zoned out, repeatedly typing "it's still not working, try again" into Claude Code. When code did work, there was no sense of achievement or satisfaction. The promise that I would become more and more productive, that I would effortlessly learn new programming languages, was proving false. The opposite was happening: I was getting worse at the one programming language I had previously felt I was getting close to mastering. I shut the door on my web development dreams and focused on regaining and improving the skills I already had.

### The Slope of Enlightenment

To be clear, I hadn't lost hope in AI itself. Ever since I first interacted with LLMs, I knew that this was going to be a genuinely transformative technology. What I was growing disillusioned with was the approach the industry seemed to be pushing. The goal seemed to be to have the human do less and less, to automate everything; if you're not running agents in parallel whilst you sleep, those are hours wasted and you'll fall behind.

One of the few voices online that challenged that view was Jeremy Howard, founder of Answer.AI. I've always been a huge fan of his work, and so when he announced that he was running an online course teaching the approach that he and his company take when working with AI, I jumped to take one of the few available spots. The course, *How to Solve It with Code*, demonstrates "basically the opposite of 'vibe coding'; it’s all about small steps, deep understanding, and deep reflection."[^4]
It takes deliberate practice and a surprising amount of self-restraint to use AI in this way, always asking for high-level suggestions, not solutions; explanations, not code completions. Gradually though, I found my productivity increasing and my engagement, excitement and ambition returning to the levels of those early, over-excited days of AI use—but this time grounded in understanding rather than illusion.

A few months later, the algorithms of YouTube presented me with an interview with Carson Gross, creator of a web development library called HTMX. He's a steadfast contrarian and very amusing; for example, a large portion of HTMX's official website is just [memes](https://htmx.org/essays/#memes) calling out the absurdity of the front-end framework situation. I had never heard of his library before, but if his claim was to be believed, it allowed you to build web apps as powerful and responsive as any modern React-based application using code that was as simple and minimal as the very first websites ever made. Given my complete lack of understanding of web development technologies, I couldn't judge whether this was—as it sounded like it must be—too good to be true or if it should be taken seriously.

When I later discovered that Answer.AI had developed a Python-based front-end [framework](www.fastht.ml/) on top of HTMX, I needed no further convincing that it could indeed be taken seriously. I sensed the web development door that I had slammed shut creak back open. I bought Carson's book, [*Hypermedia Systems*](https://hypermedia.systems/), and read it in two sittings. Then I immediately set about building this blog.

### The Plateau of Productivity

The difference between my current experience building this website and my naïve early attempts could not be more stark. 
By choosing a contrarian stack and not blindly following the default route that ChatGPT recommends, I've ensured that I'm engaged and invested.
Instead of trying to wrap my head around the idiosyncrasies of a new language, constantly questioning whether it's a productive use of my time, I'm writing Python and getting to learn about HTML, HTTP, CSS, routing—all the foundational technologies of the web. 
At the same time, I'm deepening my craft, learning about the advanced language features that make Python the perfect fit for hypermedia-oriented web apps; e.g., duck typing, introspection and decorators.
At the time of writing, this entire website is just under 300 lines of Python in a single file. I've swapped the thrill of generating thousands of lines of code for the sense of achievement from minimising the lines of code.

When I tell friends that I'm building a personal website, the response is usually "yeah, it's so easy now with things like Lovable, right?".
When I explain that, in fact, no, I'm building it with FastHTML, a completely new framework that LLMs have very little knowledge of, which is based on HTMX, a library developed by a guy in Montana who posts a crazy amount of memes on Twitter, it's hard not to feel like I'm swimming against the tide.
But a website I'm proud of, in 300 lines of Python that I fully understand—how satisfying is that?

---

So, should you build your own blog? Probably not. Most people interested in starting a blog should indeed just start writing. My decision to build from scratch, I've come to realise, was partly procrastination, partly perfectionism, and partly a defence mechanism of the digitally shy. *Hopefully,* I'll experience all the virtues of writing extolled by other bloggers. If not though, if nobody ever reads a word, if I lose momentum and stop writing, I'll still be able to justify to my future self that it was *really* an exercise in learning web development—and that part (after a few false starts) went very well!

[^1]: I actually think this was an extremely beneficial experience, which is lost with LLMs. The process of having to articulate your problem in general terms and then having to identify which of the many asked and answered questions are functionally equivalent, was an important step in learning. 

[^2]: See, e.g., Rachel Thomas's [Why you (yes, you) should blog](https://rachel.fast.ai/posts/2017-07-28-you-should-blog), Alexey Guzey's [Why You Should Start a Blog Right Now](https://guzey.com/personal/why-have-a-blog), Ben Kuhn's [Why and how to write things on the Internet](https://www.benkuhn.net/writing), and Steve Yegge's [You Should Write Blogs](https://sites.google.com/site/steveyegge2/you-should-write-blogs). Notice a pattern?

[^3]: I clearly get satisfaction from alliteration too...

[^4]: See [here](https://www.answer.ai/posts/2025-10-01-solveit-full.html) for a full description

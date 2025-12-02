---
title: When Designing an Agent, Design for a Human
date: 2025-11-26
tags: [AI, agents, LLMs, FastHTML, UI, MCP]
excerpt: Some learnings I recently shared at an AI lightning talks session, including encouragement to build custom UIs for agent tools.
---

# When Designing an Agent, Design for a Human

> This post is based on a presentation I gave at a recent "AI Lightning Talks" event at the incident.io offices in London. You can watch the full talk below:

[yt:FFxJVtCFGmI]

In this post, I'll share three tips that I learned from my experience designing and building the agent that powers [CodeWords](https://codewords.ai/).

For context, CodeWords is an AI platform for building powerful software tools and workflow automations through natural language prompting alone.
Users describe what they want, the agent writes the code, and the tool is automatically deployed to the cloud and ready to use.[^1]
It's like n8n but without all the clicking and dragging, like Lovable but focused on the backend logic and not the shiny front end.

The power of CodeWords is the versatility: tools can connect with over 2,000 third-party integrations, trigger web automations via a Chrome extension, chain other sub-tools into complex workflows; even be used as MCP servers. However, with great power comes great... context. The major design challenge was ensuring the LLM has the right information at the right time—and minimal irrelevant information. In the talk, I distilled from my experience the following three tips:

1. Start simple and add complexity only as needed
2. Make use of the JSON schema when implementing tools
3. Build UIs for your tools!

The third tip is the most non-obvious, and may seem to many like an unreasonable request and a waste of time. However, as I'll explain, it is the very enactment of my main overarching learning that formed the title of my talk: *think of the LLM as a human*. 

## Start Simple

The biggest mistake you can make when designing agents is to try and make it really clever and sophisticated from the start. There are a million blog posts and video tutorials out there where someone shows off the world's most complicated agent: *"It's made up of 8 subagents, each with different roles, and they can dynamically spin up sub-sub-agents on the fly!"*. It's easy to be impressed and tempted to try to build something similar straight away. Stop right there. Start simple.

A useful exercise is the *intern test*. Think about what the set of tasks being attempted are, and then imagine assigning them to a fresh intern. What context would they need? What software would they need? Go further: imagine you normally do those tasks as your job; you're about to go off on holiday and you need this intern to be able to cover for you while you're gone. You'll be uncontactable so how would you explain in one email everything they'd need to reliably do your job? That email is your system prompt! Any software you mention are the agent's tools.

> Would an intern have the minimal, necessary and sufficient information and tools to succeed?

We took this approach when designing the CodeWords agent. We built tools so that it could perform its core actions: writing, editing, testing code, viewing logs, etc. Any other context, we began gathering in the system prompt. Every time the agent failed to build a working tool, we'd apply the test, filling gaps in the system prompt, explaining edge cases, reducing ambiguity. As the system prompt grew and grew though, we realised we were failing the *minimal* check. Think how overwhelmed an intern would be receiving a 10,000-word email on their first day explaining every possible edge case they may encounter; better would be to point them to some documentation.

So that's exactly what we did. I started writing markdown documents—proper documentation, just like you'd write for a human developer—organised into separate pages; one for integrations, one for web automation, etc. The beauty of this approach is that you can leverage existing tools to make this documentation easy to navigate—for both humans and agents. We hosted our docs on GitHub with a table of contents `README.md` and relative links connecting related pages. Suddenly, we had something a human could easily navigate through and sanity-check. When the agent failed at a task, I could put myself in its shoes: "If I was doing this task, which document would I read?" This made it trivially easy to spot gaps or mistakes in the documentation.

Once we had our documentation structured this way, the system prompt could be reduced to just what information is common to all scenarios and we could add the natural `consult_docs` tool that lets the agent retrieve specific documents on demand. If you're familiar with the `llms.txt` standard,[^2] you'll recognise this pattern. Instead of shoving thousands of tokens about, say, using a Slack integration, into every request, the agent only pulls in that context when a user asks for something that would require it.

This is the key insight: **add complexity only when you need it, and add it in a way that a human would find useful**. Don't start with a fancy RAG pipeline or a fleet of sub-agents. Think of the intern email. When that gets unwieldy, consider new tools or remedies. Each step of added complexity should be motivated by a real pain point you've experienced, and each step should make things easier for both the agent and for you to debug.

## Tool Design

Once you've identified what tools your agent needs through this iterative process, the next challenge is implementing them well. These tips may sound obvious but I constantly see people rush this part—they write a function, throw a docstring on it, and assume the LLM will figure it out. Remember: **the agent can't see your source code**. It only sees the JSON schema that gets generated from your function signature and docstring. Making that as clear and concise as possible is an easy win.

Here's a simple example implementing an MCP tool to write or update Todo items. You might start with something like this:

```python
@mcp.tool
def todo_write(id=None, title=None, status=None, depends=None):
    """
    Write a todo item.
    
    Parameters
    ----------
    id : optional
        Task identifier for updating existing tasks
    title : optional
        The title of the task
    status : optional
        Status of the task (pending, in_progress, completed, cancelled)
    depends : optional
        List of task IDs this task depends on
        
    Returns
    -------
    dict
        Task information including the task ID
    """
    ...
```

This will work, but it's far from optimal. It's unclear what format any of the arguments should take. Is `id` a string? An int? And in what situations should the tool be used? You might explain all this in the system prompt, but that can waste tokens and increases the chance of errors.

Here's a better version:

```python
from pydantic import Field
from typing import Annotated, Literal

@mcp.tool
def todo_write(
    id: Annotated[
        int | None,
        Field(
            description="Task ID. Provide this to update an existing task. Omit to create a new task (a new ID will be generated and returned)",
            ge=1
        )
    ] = None,
    title: Annotated[
        str | None,
        Field(
            description="Brief description of the task to complete. Required when creating a new task",
            examples=["Implement user authentication", "Add unit tests for API endpoints"]
        )
    ] = None,
    status: Annotated[
        Literal["pending", "in_progress", "completed", "cancelled"] | None,
        Field(
            description="Current status of the task. Use 'cancelled' to delete a task"
        )
    ] = None,
    depends: Annotated[
        list[int] | None,
        Field(description="List of task IDs that must be completed before this task can be started.")
    ] = None
):
    """
    Use this tool to create and manage a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.

    When to use this tool:
      - complex multi-step tasks - when a task requires 3 or more distinct steps or actions
      - if the user directly asks you to use the todo list
      - when you start work on a task - mark it as `in_progress` BEFORE beginning work. You should only have one todo in progress at a time
      - after completing a task - mark it as `completed` and add any new follow-up tasks discovered during implementation 
    Use this tool to break down your work into manageable tasks and track your progress
    through a coding session. Each todo should represent a discrete piece of work that can
    be tracked independently.
    
    When NOT to use this tool:
      - if there is only a single, straightforward task
      - if the task can be completed in less than 3 trivial steps
      - if the task is purely conversational or informational
    """
    ...

```

Now we're making use of Python's type system to be explicit about what the tool expects. We've added descriptions and examples *directly* to the parameters themselves, which gets included in the JSON schema that the agent sees. This means you can keep the tool description concise and focused on how and when to use the tool. Remember **DRY (Don't Repeat Yourself)**; coding assistants like Cursor *love* writing verbose Numpy-style docstrings that list every parameter. As the parameters are already thoroughly annotated, that's just wasted tokens and introduces opportunities for the descriptions to diverge. 

Finally, **check what the agent sees.** People rarely do this, but its a good idea to sanity-check your tool descriptions by inspecting the JSON schema that gets sent to the LLM. If you're building an MCP server, you can `curl` it and use `jq` to pretty-print the output; for example:

```bash
curl http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <your_session_id>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }' | grep "^data:" | sed 's/^data: //' | jq '.result.tools'
```

The output shows you exactly what the LLM sees when deciding whether to use your tool. This is your ground truth. If the schema doesn't clearly convey what you intended, the agent won't understand it either.

## Build UIs!

Earlier on, I explained how, by viewing our docs on Github, we could put ourselves in the shoes of the agent using its `consult_docs` tool. For a given user request, we could easily check what links *we* would have followed from the main README to find the necessary information. We could step through the process, spot bugs and naturally identify areas where the experience could be improved. 

You may be thinking, "Fine, for this one example you got a UI for free, but it wouldn't be worth the effort building a custom UI for every tool". I'd argue otherwise.

There are so many libraries available today—for example, Gradio, Streamlit—that make it extremely easy to build simple UIs or web apps. And with tools like Claude Code and Cursor, there are very few excuses not to at least consider it. My personal favourite is a framework called FastHTML, which lets you build functional web apps in pure Python with minimal code.[^3] Here's an example converting our markdown files into a full documentation website:

```python
from fasthtml.common import *
from monsterui.all import *
from pathlib import Path

app, rt = fast_app(live=True, hdrs=Theme.blue.headers(highlightjs=True))

def layout(*c):
    return Div(Container(*c, cls="bg-white border-2 shadow-xl"), cls="bg-slate-100 min-h-screen p-4 flex flex-col")

@rt
def index():
    return get('README.md')

@rt('/{path:path}')
def get(path: str):
    content = (Path(__file__).parent / 'docs' / path.strip('/')).read_text()
    return layout(render_md(content))

serve()
```

That's it. 18 lines of code and you have a navigable documentation website.[^4] No React, no build step, no `npm install` limbo. 

Where this gets really powerful is that when you design a UI for you and your team to use, you'll naturally start extending it and adding features that make it easier to use. And what makes it easier for you to use also makes it easier for the agent to use.

For example, when we did this, a colleague would ask "Does the agent have any templates that implement a LinkedIn automation using the Chrome extension?" and I'd find myself scrolling through the `/templates.md` doc on our UI looking to see if there is one. I immediately notice that this is inefficient. I should be able to search 'LinkedIn'; and so should the agent.
Another 50 lines or so of code and I've got a nice search bar in our UI that implements keyword search using `bm25` and displays results ordered by best match.
Again, testing and debugging this within a UI is so much easier. Does searching for 'LinkedIn' surface the right results? Should I experiment with semantic search using embeddings instead? Does the chunk of text displayed for each result provide enough context? Once I'm happy with the search function in my UI, I can literally import it from my FastHTML script into my MCP server script and expose it as a tool. No duplication, no drift between what the human sees and what the agent sees. The UI isn't wasted effort—it's your development and debugging environment.

The key is to build the minimal UI that eliminates friction from using the agent's tools. It doesn't need to win any design awards; you shouldn't need to get your front-end dev involved. In fact, if it's looks really slick, you've probably spent too much time on it. The goal is simply to be able to BE THE AGENT, put yourself in its shoes, experience what it experiences. That's how you build and refine tools that work.

## Conclusion

These tips seem obvious in hindsight; however, they weren't obvious to me when I started. My background is in research, so I'm wired to avoid anthropomorphising LLMs. I cringe at words like *thinking* being used to describe the outputs of a statistical model. So when I spent time on the applied side, building an agent to power a real software generation platform, it was a bit of a surprise to me that I found pretending the LLM is a human to be the single most useful frame of mind to adopt.

If you clicked on this post hoping to find instructions for building the most complex multi-agent, multi-model, multi-everything AI system, I apologise. 
Thankfully though, there are plenty of those around, and I hope there was some value in me sharing a few simpler, easy to overlook tips that are useful to bear in mind for anyone designing an agent, no matter how complex.

[^1]: Under the hood, a CodeWords *function* or *service* is a Python script, implemented in a flavour of FastAPI that we developed to ensure it plays nicely with the platform for automated testing, deployment, etc. 

[^2]: See [llmstxt.org](https://llmstxt.org/)

[^3]: This website is written in FastHTML

[^4]: In practice, you might want to add things like path verification to ensure users can't navigate to non-documentation files, but it really doesn't need to be much longer than this.

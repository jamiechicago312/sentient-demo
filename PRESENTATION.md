# SLIDE CONTENT - Copy & Paste Ready

---

## SLIDE 1: Title

# "What's Up Doc?"
## Auto-Generating Technical Documentation with OpenHands SDK

A hackathon demo by [Your Name]

---

## SLIDE 2: The Problem

### Documentation is painful
- Developers hate writing docs
- Every repo needs: setup, architecture, usage, API reference
- Mintlify is great, but you still have to write it

### Our Solution
- **One command** → analyzes any GitHub repo → generates full Mintlify docs → opens a Pull Request

---

## SLIDE 3: High-Level Architecture

```
[CLI]          [Pipeline]         [OpenHands Agent]     [GitHub PR]
  ↓                ↓                      ↓                  ↓
cli.py    →   pipeline.py      →    agent_runner.py   →   github.py
```

**What happens:**
1. Clone source repo (read-only)
2. Clone target docs repo (write access)
3. Agent inspects source code
4. Agent writes Mintlify docs to target
5. Pushes branch & opens PR

---

## SLIDE 4: Three Core SDK Concepts

1. **LLM** - The brain (model, API key, base URL)
2. **Agent** - The worker (has tools, follows instructions)
3. **Conversation** - The interface (send prompts, run agent)

```python
llm = LLM(model="...", api_key="...")
agent = Agent(llm=llm, tools=[...])
conversation = Conversation(agent=agent, workspace="/tmp")
conversation.send_message("Your task")
conversation.run()
```

~10 lines of code to have an autonomous agent!

---

## SLIDE 5: Tools = Superpowers

| Tool | What It Does | Why We Need It |
|------|--------------|----------------|
| TerminalTool | Run shell commands | Clone repos, inspect code, run git |
| FileEditorTool | Read/write files | Create documentation files |
| TaskTrackerTool | Track progress | Keep agent organized |

**Key insight:** 
- Tools = what the agent CAN do
- Prompt = what the agent SHOULD do

---

## SLIDE 6: The Prompt (Secret Sauce)

```python
prompt = """You are an expert software engineer and technical writer.

Goal: create Mintlify-based technical documentation for SOURCE repo.

Requirements:
- Only READ from SOURCE. Do not modify SOURCE.
- Write documentation into TARGET using Mintlify.

Deliverables:
- mint.json (or updated)
- docs/introduction.mdx
- docs/setup.mdx
- docs/architecture.mdx
- docs/usage.mdx
- docs/api.mdx (if applicable)

Suggested approach:
1. Inspect SOURCE structure
2. Identify key modules
3. Write Mintlify docs
4. Update mint.json navigation
"""
```

---

## SLIDE 7: Agent in Action

**What the autonomous agent does:**

1. `git clone` the source repo
2. `ls`, `find`, `cat` to explore the codebase
3. Read README, pyproject.toml, package.json
4. Identify: entrypoints, APIs, architecture
5. Create `docs/` files in target repo
6. Generate or update `mint.json`
7. **Done!** (stops autonomously)

**The agent figured this out on its own** - we never told it exact file paths.

---

## SLIDE 8: Pipeline Code

```python
def run_pipeline(...):
    # 1. Set up workspace
    clone_repo(source, source_dir)
    clone_repo(target, target_dir)
    
    # 2. Build the prompt
    prompt = build_docgen_prompt(...)
    
    # 3. Run the OpenHands agent ← SDK handles this
    run_openhands_doc_agent(workspace=ws, prompt=prompt, ...)
    
    # 4. Git operations (our code)
    commit_all(target_dir, "docs: add ...")
    push_branch(target_dir, branch)
    
    # 5. Create PR
    create_pull_request(...)
```

SDK handles autonomy; we handle orchestration.

---

## SLIDE 9: Live Demo

### Try it yourself:

```bash
export LLM_API_KEY="your-key"
export GITHUB_TOKEN="your-token"

whatsupdoc \
  --source https://github.com/OpenHands/software-agent-sdk \
  --target https://github.com/YOU/your-docs-repo \
  --coverage "overview,setup,architecture,api"
```

### Or dry-run (no PR):
```bash
whatsupdoc --source ... --target ... --dry-run
```

---

## SLIDE 10: Why OpenHands SDK?

| Feature | Benefit |
|---------|---------|
| Pre-built tools | Terminal, FileEditor, TaskTracker ready to use |
| Workspace isolation | Agent works in clean, controlled directory |
| Conversation API | Simple message-passing, easy to understand |
| LLM flexibility | Use any provider via LiteLLM compatibility |
| Agent loop | Automatically handles multi-step tasks |

### This demo shows:
- Real autonomous behavior
- Multi-step task completion
- File system operations
- GitHub API integration

---

## SLIDE 11: Minimal Code to Get Started

```python
from openhands.sdk import Agent, Conversation, LLM, Tool
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool

llm = LLM(
    model="openhands/claude-sonnet-4-5-20250929", 
    api_key="your-key"
)
agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
    ]
)
conversation = Conversation(agent=agent, workspace="/tmp/demo")
conversation.send_message("Create a file called hello.txt with 'Hello World'")
conversation.run()
```

**~15 lines to have your own autonomous agent!**

---

## SLIDE 12: Resources

- **OpenHands SDK Docs**: https://docs.openhands.dev/sdk/getting-started
- **This Demo Repo**: https://github.com/All-Hands-AI/whatsupdoc
- **Get API Key**: https://app.all-hands.dev/settings/api-keys
- **Mintlify**: https://mintlify.com

---

## SLIDE 13: Questions?

# Thanks!

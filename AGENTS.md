# Repository Guide (for OpenHands agents)

## What this repo is

A minimal demo project that builds a documentation-generation agent using the OpenHands Software Agent SDK.

## Quickstart

```bash
# On WSL/Ubuntu you may need:
# sudo apt update && sudo apt install -y python3-venv python3-pip

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

export LLM_API_KEY=...          # OpenHands Cloud or other LiteLLM-supported provider
export LLM_MODEL=openhands/claude-sonnet-4-5-20250929
export GITHUB_TOKEN=...         # GitHub PAT with push permission on target repo

whatsupdoc --help
# if needed:
python -m whatsupdoc --help
```

## Layout

- `src/whatsupdoc/cli.py`: CLI entrypoint
- `src/whatsupdoc/agent_runner.py`: OpenHands SDK wiring (LLM, Agent, Conversation)
- `src/whatsupdoc/pipeline.py`: clones repos, runs agent, pushes branch, opens PR
- `src/whatsupdoc/github.py`: GitHub REST calls (PR creation)
- `src/whatsupdoc/git_utils.py`: git helpers

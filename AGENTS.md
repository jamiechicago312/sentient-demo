# Repository Guide (for OpenHands agents)

## What this repo is

A minimal demo project that builds a documentation-generation agent using the OpenHands Software Agent SDK.

## Quickstart

```bash
pip install -e .
export LLM_API_KEY=...          # OpenHands Cloud or other LiteLLM-supported provider
export LLM_MODEL=openhands/claude-sonnet-4-5-20250929
export GITHUB_TOKEN=...         # GitHub PAT with push permission on target repo
whatsupdoc --help
```

## Layout

- `src/whatsupdoc/cli.py`: CLI entrypoint
- `src/whatsupdoc/agent_runner.py`: OpenHands SDK wiring (LLM, Agent, Conversation)
- `src/whatsupdoc/pipeline.py`: clones repos, runs agent, pushes branch, opens PR
- `src/whatsupdoc/github.py`: GitHub REST calls (PR creation)
- `src/whatsupdoc/git_utils.py`: git helpers

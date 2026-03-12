# whatsupdoc

A demo agent built with the **OpenHands Software Agent SDK** that:

1. Clones a **public source repo** (read-only)
2. Clones a **target docs repo** (write access required)
3. Uses an OpenHands SDK agent to analyze the source repo and generate **Mintlify-based technical documentation** into the target repo
4. Pushes a branch and opens a **GitHub Pull Request** in the target repo

OpenHands SDK docs:
- https://docs.openhands.dev/sdk/getting-started

## Prerequisites

- Python 3.10+
- `git`
- A GitHub token with permission to push to the target repo (`GITHUB_TOKEN`)
- An LLM API key compatible with OpenHands SDK (`LLM_API_KEY`)
  - For OpenHands Cloud, get a key from: https://app.all-hands.dev/settings/api-keys
- The target repo should ideally already have at least 1 commit. If it's empty, whatsupdoc will create an initial commit on the default branch so it can open a PR.

## Install

```bash
pip install -e .
```

## Run (headless)

### Option A: use a local `.env` file (recommended)

This repo supports loading secrets from a local `.env` file via `python-dotenv`.
The `.env` file is already gitignored.

```bash
cp .env.example .env
# edit .env with your keys

whatsupdoc \
  --source https://github.com/OpenHands/software-agent-sdk \
  --target https://github.com/<you>/<your-docs-repo> \
  --coverage "overview,setup,architecture,api"
```

### Option B: export environment variables

```bash
export LLM_API_KEY="..."
export LLM_MODEL="openhands/claude-sonnet-4-5-20250929"  # example
export GITHUB_TOKEN="..."

# If you installed with `pip install -e .` but `whatsupdoc` isn't on PATH,
# you can always run via: `python -m whatsupdoc ...`

whatsupdoc \
  --source https://github.com/OpenHands/software-agent-sdk \
  --target https://github.com/<you>/<your-docs-repo> \
  --coverage "overview,setup,architecture,api"
```

### Preview with Mintlify

In the target repo:

```bash
npx mintlify dev
```

## Notes

- The tool will create a Mintlify scaffold (`mint.json`) in the target repo if it does not exist.
- Documentation pages are written under `docs/`.
- The source repo is treated as read-only: the agent only inspects files.

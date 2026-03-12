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

## Install

`whatsupdoc` is a Python package (name: `whatsupdoc`) with a CLI entrypoint (command: `whatsupdoc`).

### Recommended: install into a virtual environment

```bash
python3 -m venv .venv
# mac/linux/WSL
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -e .
```

#### WSL / Ubuntu troubleshooting

If `python3 -m venv .venv` fails with `ensurepip is not available`, install venv support:

```bash
sudo apt update
sudo apt install -y python3-venv
# If you're on Ubuntu 24.04 / Python 3.12 and it still fails:
# sudo apt install -y python3.12-venv
```

If `python` is not found **outside** the venv, that’s normal on some distros—use `python3`.
(Inside the venv, `python` should exist after activation.)

Notes:
- `pip install -e .` must include the path argument (the dot): `python -m pip install -e .`
- `pip install -e .` is an **editable install** (good for local development; code changes take effect without reinstalling).
- If you only want a normal install, use: `python -m pip install .`
- This project is not published to PyPI, so `pip install whatsupdoc` won’t work (install from the repo).
- If `whatsupdoc` isn’t found after install, run it as a module:
  - `python -m whatsupdoc --help`
  - or add your pip scripts dir to `PATH` (often `~/.local/bin`)

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

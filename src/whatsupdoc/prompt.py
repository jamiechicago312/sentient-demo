from __future__ import annotations

from pathlib import Path


def build_docgen_prompt(*, source_dir: Path, target_dir: Path, source_repo: str, coverage: str) -> str:
    topics = [t.strip() for t in coverage.split(",") if t.strip()]

    return f"""You are an expert software engineer and technical writer.

Goal: create Mintlify-based technical documentation for the SOURCE repository.

SOURCE repo (read-only): {source_repo}
SOURCE path on disk: {source_dir}
TARGET docs repo path on disk: {target_dir}

Requirements:
- Only READ from SOURCE. Do not modify SOURCE.
- Write documentation into TARGET using Mintlify as the basis.
- If TARGET has no Mintlify config, create a minimal Mintlify scaffold:
  - Create `mint.json` at TARGET repo root
  - Create docs pages under `docs/` (MDX) and add them to navigation
- If `mint.json` already exists, update navigation to include the new pages (do not delete existing pages).

Documentation coverage requested (prioritize these): {', '.join(topics) if topics else '(none specified)'}

Deliverables in TARGET:
- `mint.json` (or updated)
- `docs/introduction.mdx`
- `docs/setup.mdx`
- `docs/architecture.mdx`
- `docs/usage.mdx`
- `docs/api.mdx` (only if the repo has a public API; otherwise explain the interfaces that exist)

Quality bar:
- Be concrete. Refer to real file paths and entrypoints from SOURCE.
- Include setup steps, commands, and environment variables if they exist.
- If something is unknown, say so explicitly rather than guessing.
- Do not run any untrusted code from SOURCE. You may run safe inspection commands like `git`, `ls`, `find`, `cat`, `sed`, `python -c` for parsing, etc.

Suggested approach:
1. Inspect SOURCE structure (`ls`, `find`, README, pyproject/package.json, etc.)
2. Identify how the project is built/run/tested
3. Identify key modules and architecture
4. Write Mintlify docs pages into TARGET
5. Update `mint.json` navigation

When done, stop.
"""

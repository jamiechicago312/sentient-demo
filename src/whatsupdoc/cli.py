from __future__ import annotations

import os
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

from .pipeline import run_pipeline


# Load local secrets from a .env file (if present). This keeps secrets out of shell history.
# The file should be gitignored (this repo ships with `.gitignore` including `.env`).
load_dotenv(override=False)

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def generate(
    source: str = typer.Option(..., "--source", "-s", help="Public repo to scan (URL or owner/name)."),
    target: str = typer.Option(
        ..., "--target", "-t", help="Target GitHub repo where docs PR will be opened (URL or owner/name)."
    ),
    coverage: str = typer.Option(
        "overview,setup,architecture,usage,api",
        "--coverage",
        help="Comma-separated topics to cover in docs.",
    ),
    workspace: Path = typer.Option(
        Path(".whatsupdoc-workspace"),
        "--workspace",
        help="Local workspace directory used for cloning and generation.",
    ),
    base_branch: str | None = typer.Option(
        None,
        "--base-branch",
        help="Base branch for PR (default: detected from target repo).",
    ),
    llm_model: str | None = typer.Option(
        None,
        "--llm-model",
        envvar="LLM_MODEL",
        help="LLM model name (env: LLM_MODEL).",
    ),
    llm_api_key: str | None = typer.Option(
        None,
        "--llm-api-key",
        envvar="LLM_API_KEY",
        help="LLM API key (env: LLM_API_KEY).",
    ),
    llm_base_url: str | None = typer.Option(
        None,
        "--llm-base-url",
        envvar="LLM_BASE_URL",
        help="Optional LiteLLM/OpenAI-compatible base URL (env: LLM_BASE_URL).",
    ),
    github_token: str | None = typer.Option(
        None,
        "--github-token",
        envvar="GITHUB_TOKEN",
        help="GitHub token with permission to push/open PR (env: GITHUB_TOKEN).",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Generate docs locally but do not push or open a PR.",
    ),
):
    """Generate Mintlify technical docs for SOURCE and open a PR in TARGET."""

    if llm_api_key is None:
        # Convenience: some users think of this as an OpenHands API key.
        llm_api_key = os.getenv("OPENHANDS_API_KEY")

    if not llm_api_key:
        raise typer.BadParameter("Missing LLM API key (set LLM_API_KEY or OPENHANDS_API_KEY).")

    if not llm_model:
        # Works well for OpenHands Cloud users.
        llm_model = "openhands/claude-sonnet-4-5-20250929"

    if not dry_run and not github_token:
        raise typer.BadParameter("Missing GitHub token (set GITHUB_TOKEN or pass --github-token).")

    pr_url = run_pipeline(
        source=source,
        target=target,
        coverage=coverage,
        workspace=workspace,
        base_branch=base_branch,
        llm_model=llm_model,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        github_token=github_token,
        dry_run=dry_run,
    )

    if pr_url:
        console.print(f"\nPR created: [bold]{pr_url}[/bold]")
    else:
        console.print("\nDone.")

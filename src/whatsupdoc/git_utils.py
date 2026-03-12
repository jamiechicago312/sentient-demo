from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


def _run(cmd: list[str], *, cwd: Path) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if proc.returncode != 0:
        raise GitError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}")
    return proc.stdout.strip()


def ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def clone_repo(url: str, dest: Path) -> None:
    _run(["git", "clone", "--depth", "1", url, str(dest)], cwd=dest.parent)


def get_default_branch(repo_dir: Path) -> str:
    ref = _run(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], cwd=repo_dir)
    return ref.split("/")[-1]


def checkout_new_branch(repo_dir: Path, branch: str) -> None:
    _run(["git", "checkout", "-b", branch], cwd=repo_dir)


def commit_all(repo_dir: Path, message: str) -> None:
    _run(["git", "add", "-A"], cwd=repo_dir)

    status = _run(["git", "status", "--porcelain"], cwd=repo_dir)
    if not status.strip():
        raise GitError("No changes to commit in target repo.")

    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "openhands")
    env.setdefault("GIT_AUTHOR_EMAIL", "openhands@all-hands.dev")
    env.setdefault("GIT_COMMITTER_NAME", "openhands")
    env.setdefault("GIT_COMMITTER_EMAIL", "openhands@all-hands.dev")

    proc = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=str(repo_dir),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    if proc.returncode != 0:
        raise GitError(f"git commit failed ({proc.returncode}):\n{proc.stdout}")


def set_push_remote_with_token(repo_dir: Path, *, token: str, owner: str, repo: str) -> None:
    url = f"https://x-access-token:{token}@github.com/{owner}/{repo}.git"
    subprocess.run(
        ["git", "remote", "set-url", "origin", url],
        cwd=str(repo_dir),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def push_branch(repo_dir: Path, branch: str) -> None:
    _run(["git", "push", "-u", "origin", branch], cwd=repo_dir)

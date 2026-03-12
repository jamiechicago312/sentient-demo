from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


def _run_result(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def _run(cmd: list[str], *, cwd: Path) -> str:
    proc = _run_result(cmd, cwd=cwd)
    if proc.returncode != 0:
        raise GitError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}")
    return proc.stdout.strip()


def _try_run(cmd: list[str], *, cwd: Path) -> str | None:
    proc = _run_result(cmd, cwd=cwd)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def clone_repo(url: str, dest: Path) -> None:
    _run(["git", "clone", "--depth", "1", url, str(dest)], cwd=dest.parent)


def get_default_branch(repo_dir: Path) -> str:
    ref = _try_run(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], cwd=repo_dir)
    if ref:
        return ref.split("/")[-1]

    remote_show = _try_run(["git", "remote", "show", "origin"], cwd=repo_dir)
    if remote_show:
        for line in remote_show.splitlines():
            if line.strip().startswith("HEAD branch:"):
                head = line.split(":", 1)[1].strip()
                if head and head != "(unknown)":
                    return head

    remote_branches = _try_run(["git", "branch", "-r"], cwd=repo_dir) or ""
    names: list[str] = []
    for line in remote_branches.splitlines():
        line = line.strip()
        if not line.startswith("origin/"):
            continue
        name = line.removeprefix("origin/")
        if name == "HEAD":
            continue
        names.append(name)

    for preferred in ("main", "master"):
        if preferred in names:
            return preferred

    if names:
        return names[0]

    raise GitError(
        "Unable to determine the target repo's default branch. "
        "This usually means the target repository is empty (no commits/branches). "
        "Create an initial commit in the target repo (e.g., add a README on GitHub) "
        "or pass --base-branch."
    )



def repo_has_commits(repo_dir: Path) -> bool:
    return _try_run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo_dir) is not None


def init_empty_repo_with_initial_commit(repo_dir: Path, *, base_branch: str) -> None:
    """Initialize an empty cloned repo so we can create feature branches/PRs.

    GitHub allows creating empty repositories without any commits. `git clone` then
    yields a repo with no `HEAD`, and commands like `git checkout -b ...` fail.

    We fix this by creating an orphan base branch and making a small initial commit.
    """

    _run(["git", "checkout", "--orphan", base_branch], cwd=repo_dir)

    readme = repo_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Repository\n\nInitialized by whatsupdoc.\n",
            encoding="utf-8",
        )

    commit_all(repo_dir, "chore: initialize repository")


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

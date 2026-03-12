from __future__ import annotations

import re
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class GitHubRepo:
    owner: str
    name: str


_GH_RE = re.compile(
    r"^(?:https?://github\.com/)?(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)


def parse_github_repo(target: str) -> GitHubRepo:
    m = _GH_RE.match(target.strip())
    if not m:
        raise ValueError(f"Unrecognized GitHub repo format: {target}")
    return GitHubRepo(owner=m.group("owner"), name=m.group("repo"))



def get_repo_default_branch(*, repo: GitHubRepo, token: str | None = None) -> str | None:
    url = f"https://api.github.com/repos/{repo.owner}/{repo.name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers, timeout=60)
    if resp.status_code >= 300:
        return None

    data = resp.json()
    default_branch = data.get("default_branch")
    if isinstance(default_branch, str) and default_branch:
        return default_branch
    return None


def create_pull_request(
    *,
    repo: GitHubRepo,
    token: str,
    head: str,
    base: str,
    title: str,
    body: str,
) -> str:
    url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    resp = requests.post(
        url,
        headers=headers,
        json={
            "title": title,
            "head": head,
            "base": base,
            "body": body,
        },
        timeout=60,
    )

    if resp.status_code >= 300:
        raise RuntimeError(f"Failed to create PR: HTTP {resp.status_code}: {resp.text}")

    return resp.json()["html_url"]

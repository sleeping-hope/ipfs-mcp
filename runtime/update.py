import os
import httpx

REPO = os.getenv("MCP_REPOSITORY", "sleeping-hope/ipfs-mcp")
BRANCH = os.getenv("MCP_BRANCH", "main")
GITHUB_API = "https://api.github.com"

def update_status() -> dict:
    """Check the latest GitHub revision without mutating the running process."""
    url = f"{GITHUB_API}/repos/{REPO}/commits/{BRANCH}"
    try:
        response = httpx.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "source_of_truth": "github",
            "repository": REPO,
            "branch": BRANCH,
            "latest_commit": data.get("sha"),
            "latest_commit_url": data.get("html_url"),
            "update_available": None,
            "apply_mode": "restart-from-current-revision",
            "note": "Compare latest_commit with the revision used by the current runtime.",
        }
    except Exception as exc:
        return {
            "source_of_truth": "github",
            "repository": REPO,
            "branch": BRANCH,
            "update_available": None,
            "error": str(exc),
        }

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from tools.asset_pipeline.status import build_asset_status


def summarize_item_assets(root: Path) -> list[dict[str, Any]]:
    root = Path(root).resolve()
    items_dir = root / "data" / "items"
    summaries = []

    for item_path in sorted(items_dir.glob("oddity_*.json")):
        status = build_asset_status(root=root, item_id=item_path.stem)
        if not status["approved"]:
            continue
        ready_outputs = sum(1 for asset in status["assets"] if asset["exists"])
        summaries.append(
            {
                "item_id": status["item_id"],
                "display_name": status["display_name"],
                "generation_status": status["generation_status"],
                "approved": status["approved"],
                "ready_outputs": ready_outputs,
                "total_outputs": len(status["assets"]),
                "missing_stages": status["missing_stages"],
            }
        )

    return summaries


def build_project_status(
    *,
    root: Path,
    git_info: dict[str, Any] | None = None,
    test_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    items = summarize_item_assets(root)

    return {
        "git": git_info if git_info is not None else collect_git_info(root),
        "tests": test_info if test_info is not None else {"ran": False, "passed": None, "summary": "not run"},
        "asset_totals": {
            "items": len(items),
            "ready_outputs": sum(item["ready_outputs"] for item in items),
            "total_outputs": sum(item["total_outputs"] for item in items),
        },
        "items": items,
    }


def collect_git_info(root: Path) -> dict[str, Any]:
    branch = _run_git(root, ["branch", "--show-current"])
    status = _run_git(root, ["status", "--short"])
    log = _run_git(root, ["log", "--oneline", "-5"])

    changes = [line for line in status.splitlines() if line.strip()]
    return {
        "branch": branch.strip() or "unknown",
        "is_dirty": bool(changes),
        "changes": changes,
        "recent_commits": [line for line in log.splitlines() if line.strip()],
    }


def run_test_suite(root: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["python", "-m", "unittest", "discover", "-s", "tests"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    summary = _extract_test_summary(output)
    return {
        "ran": True,
        "passed": result.returncode == 0,
        "summary": summary,
        "exit_code": result.returncode,
    }


def render_project_status_markdown(status: dict[str, Any]) -> str:
    git = status["git"]
    tests = status["tests"]
    totals = status["asset_totals"]
    working_tree = "dirty" if git["is_dirty"] else "clean"

    lines = [
        "# Project Status",
        "",
        "## Repo",
        "",
        f"- Branch: `{git['branch']}`",
        f"- Working tree: {working_tree}",
        "",
        "## Verification",
        "",
        f"- Tests: {_format_test_status(tests)}",
        "",
        "## Asset Factory",
        "",
        (
            f"- Asset outputs: {totals['ready_outputs']}/{totals['total_outputs']} ready "
            f"across {totals['items']} item(s)"
        ),
    ]

    for item in status["items"]:
        missing = ", ".join(item["missing_stages"]) if item["missing_stages"] else "none"
        lines.append(
            f"- {item['item_id']} {item['display_name']}: "
            f"{item['ready_outputs']}/{item['total_outputs']} ready; missing {missing}"
        )

    if git["recent_commits"]:
        lines.extend(["", "## Recent Commits", ""])
        lines.extend(f"- `{commit}`" for commit in git["recent_commits"])

    if git["changes"]:
        lines.extend(["", "## Working Tree Changes", ""])
        lines.extend(f"- `{change}`" for change in git["changes"])

    return "\n".join(lines) + "\n"


def _format_test_status(test_info: dict[str, Any]) -> str:
    if not test_info["ran"]:
        return "not run"
    state = "passing" if test_info["passed"] else "failing"
    return f"{state} ({test_info['summary']})"


def _extract_test_summary(output: str) -> str:
    for line in output.splitlines():
        if line.startswith("Ran "):
            return line
    return "completed"


def _run_git(root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a compact project progress dashboard."
    )
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run the Python test suite and include the result.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of Markdown.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    test_info = run_test_suite(root) if args.run_tests else None
    status = build_project_status(root=root, test_info=test_info)

    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(render_project_status_markdown(status), end="")

    return 1 if status["tests"]["ran"] and not status["tests"]["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

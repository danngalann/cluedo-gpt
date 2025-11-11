#!/usr/bin/env python3
import re
import subprocess
import sys

import toml


PYPROJECT = "pyproject.toml"
DEV_GROUP = "dev"


def strip_constraint(spec: str) -> str:
    """Strip off any version/operator so 'pkg[extra]>=1.2.3' → 'pkg[extra]'."""
    m = re.match(r"^([^\s<>=!]+(?:\[[^\]]+\])?)", spec)
    if not m:
        sys.exit(f"Error parsing specifier: {spec}")
    return m.group(1)


def run_uv(args: list[str]):
    print(f"> uv {' '.join(args)}")
    res = subprocess.run(["uv", *args])  # noqa: S603, S607
    if res.returncode:
        sys.exit(res.returncode)


def main():
    data = toml.load(PYPROJECT)
    main_specs = data.get("project", {}).get("dependencies", [])
    dev_specs = data.get("dependency-groups", {}).get(DEV_GROUP, [])

    main_pkgs = [strip_constraint(s) for s in main_specs]
    dev_pkgs = [strip_constraint(s) for s in dev_specs]

    if main_pkgs:
        # remove only main
        run_uv(["remove", *main_pkgs])
    else:
        print("⧖ no main dependencies to remove")

    if dev_pkgs:
        # remove dev with group flag
        run_uv(["remove", *dev_pkgs, "--group", DEV_GROUP])
    else:
        print(f"⧖ no `{DEV_GROUP}` dependencies to remove")

    if main_pkgs:
        run_uv(["add", *main_pkgs])
    if dev_pkgs:
        run_uv(["add", "--group", DEV_GROUP, *dev_pkgs])

    print("✅ All dependencies re-added at latest versions.")


if __name__ == "__main__":
    main()

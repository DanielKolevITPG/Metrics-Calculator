"""App entry point.

UI is the default; pass `--cli` to use the terminal UI.
"""

from __future__ import annotations

import sys

from .cli import run_cli


def entrypoint(argv: list[str] | None = None) -> None:
    """Launch UI by default; fall back to CLI when needed."""
    if argv is None:
        argv = sys.argv[1:]

    if "--cli" in argv:
        run_cli()
        return

    try:
        from .ui import run_ui

        run_ui()
    except Exception as e:
        print(f"UI failed to start ({e}). Falling back to CLI.")
        run_cli()

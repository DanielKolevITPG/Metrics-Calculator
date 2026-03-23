"""Workspace launcher.

This repository uses a `src/` layout.

Run UI (default): `python main.py`
Run CLI: `python main.py --cli`
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    root = Path(__file__).resolve().parent
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main(argv: list[str] | None = None) -> None:
    _ensure_src_on_path()
    # Import after sys.path modification
    from matrix_calculator.entrypoint import entrypoint  # type: ignore[import-not-found]

    if argv is None:
        argv = sys.argv[1:]
    entrypoint(argv)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)

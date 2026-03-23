"""Module entry point.

Note: with a `src/` layout this works reliably after installing the project
(e.g. `pip install -e .`) or when `src` is on `PYTHONPATH`.
"""

from .entrypoint import entrypoint


if __name__ == "__main__":
    entrypoint()

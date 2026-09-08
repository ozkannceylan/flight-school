"""SEE IT — Lab {{NUM}}. Writes media/lab{{NUM}}.gif."""

from __future__ import annotations

from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media


def main() -> None:
    _ = get("lab{{NUM}}")
    ensure_media()
    print(f"TODO: write {MEDIA / 'lab{{NUM}}.gif'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Render an SVG route book to PNG for sharing.

Uses resvg-py (https://pypi.org/project/resvg-py/) which has good Chinese font
fallback handling on Linux. On macOS, the SVG renders perfectly as-is in any
browser; this script is mainly for environments without GUI access.

Install:
    pip install resvg-py --break-system-packages

Usage:
    python3 render_png.py input.svg output.png [--width 1440]

Notes:
- Default width is 1440px which is a good balance for WeChat sharing.
- For higher quality (poster-grade), use 2160 or 2880.
- Emojis won't render in environments without an emoji font (Linux sandboxes).
  In that case they show as empty boxes (□) which actually function fine as
  bullet markers. For full emoji rendering, open the SVG in a macOS browser.
"""

import argparse
import sys
from pathlib import Path


def render(svg_path: Path, png_path: Path, width: int = 1440) -> None:
    try:
        import resvg_py
    except ImportError:
        sys.exit(
            "resvg-py is not installed. Run:\n"
            "  pip install resvg-py --break-system-packages"
        )

    svg_text = svg_path.read_text(encoding="utf-8")
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_text, width=width)
    png_path.write_bytes(bytes(png_bytes))
    print(f"Rendered {svg_path.name} → {png_path.name} at {width}px width")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a route-book SVG to PNG")
    parser.add_argument("svg", type=Path, help="Input SVG path")
    parser.add_argument("png", type=Path, help="Output PNG path")
    parser.add_argument(
        "--width",
        type=int,
        default=1440,
        help="Output PNG width in pixels (default: 1440)",
    )
    args = parser.parse_args()

    if not args.svg.exists():
        sys.exit(f"Input SVG not found: {args.svg}")

    args.png.parent.mkdir(parents=True, exist_ok=True)
    render(args.svg, args.png, args.width)


if __name__ == "__main__":
    main()

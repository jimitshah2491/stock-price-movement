"""Command-line entry point. Research commands will be added with the workflow."""

import argparse
import json
import logging
from importlib.metadata import version

from pydantic import ValidationError

from stock_price_movement.config import Settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="stock-price-movement",
        description="Personal investment research for Alphabet (GOOGL).",
    )
    parser.add_argument("--version", action="version", version=version("stock-price-movement"))
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("config", help="Show local configuration without fetching data.")
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        settings = Settings()
    except ValidationError as exc:
        problems = "; ".join(
            f"{'.'.join(map(str, error['loc']))}: {error['msg']}"
            for error in exc.errors(include_input=False, include_url=False)
        )
        parser.error(f"Invalid configuration: {problems}")

    logging.basicConfig(level=settings.log_level, format="%(levelname)s %(name)s: %(message)s")
    # Explicit fields prevent future credentials from appearing in configuration output.
    print(
        json.dumps(
            {
                "company": "Alphabet",
                "ticker": "GOOGL",
                "data_dir": str(settings.data_dir.expanduser().resolve()),
                "log_level": settings.log_level,
            },
            indent=2,
        )
    )
    return 0

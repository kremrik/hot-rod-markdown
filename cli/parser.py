import argparse
from typing import List


def cli(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        required=False,
        help="Path to directory to begin traversal",
    )

    return parser.parse_args(arguments)

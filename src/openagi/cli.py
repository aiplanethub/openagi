import argparse
import logging
import os
from openagi.memory.base import BaseMemory


def clear_long_term_memory():
    """Clears the long-term memory directory using environment variables."""
    long_term_dir = os.getenv("LONG_TERM_DIR", ".long_term_dir")
    BaseMemory.clear_long_term_memory(long_term_dir)


def main():
    parser = argparse.ArgumentParser(description="OpenAGI CLI for various commands.")

    parser.add_argument(
        "--clear-ltm",
        action="store_true",
        help="Clear the long-term memory directory."
    )

    args = parser.parse_args()

    if args.clear_ltm:
        clear_long_term_memory()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

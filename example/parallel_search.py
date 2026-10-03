"""Run an opt-in web search without configuring a search API key."""

import argparse

from openagi.actions.tools.parallel_search import ParallelSearch
from openagi.actions.utils import run_action


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Question or objective to search for")
    parser.add_argument("--timeout", type=float, default=30, help="Seconds per HTTP request")
    args = parser.parse_args()
    print(
        run_action(ParallelSearch, memory=None, llm=None, query=args.query, timeout=args.timeout)
    )


if __name__ == "__main__":
    main()

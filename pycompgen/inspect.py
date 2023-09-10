import argparse
from typing import Dict, List, Optional, Tuple


def sort_key(item: str) -> str:
    """
    All arguments prefixed by "--" or "-" should come before positionals (e.g. subcommands).

    Short and long options should be sorted alphabetically without accounting for the single "-" in
    front of short options and the double "--" in front of long options.
    """
    if item.startswith("--"):
        return item[1:]
    return item


def possible_completions_by_context(
    parser: argparse.ArgumentParser,
    current_context: Optional[Tuple[str, ...]] = None,
) -> Dict[Tuple[str, ...], List[str]]:
    """
    For each possible command context in the given argument parsers, returns the possible completions
    at that context.

    Structure of return is a dictionary whose keys are the possible contexts (tuples of strings) and
    whose values are the possible completions (lists of strings).
    """
    if current_context is None:
        current_context = tuple()

    result: Dict[Tuple[str, ...], List[str]] = {}

    completions: List[str] = [key for key in parser._option_string_actions]

    for action in parser._get_positional_actions():
        # If action is a _SubparsersAction, we need to recurse.
        if isinstance(action, argparse._SubParsersAction):
            for choice, subparser in action.choices.items():
                completions.append(choice)
                subresult = possible_completions_by_context(
                    subparser,
                    current_context + (choice,),
                )
                for key, value in subresult.items():
                    result[key] = value

    result[current_context] = sorted(completions, key=sort_key)

    return result

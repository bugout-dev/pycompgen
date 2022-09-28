"""
Generate bash completion for an argparse CLI.
"""
import argparse
from typing import Dict, List, Optional, Tuple


def command_info(
    parser: argparse.ArgumentParser, prefix: Tuple[str, ...] = tuple()
) -> Dict[Tuple[str, ...], List[Tuple[str, Optional[List[str]]]]]:
    """
    Args:
    1. parser - an argparse.ArgumentParser representing a CLI or a sub-CLI
    2. prefix - commands and subcommands called prior to reaching the current parser

    Returns: A dictionary of the form
    ```
    {
        ("<command>", "<subcommand_1>", ..., "<subcommand_n>"): [("<option_1>", [<possible_values_if_any_or_None>]), ..., ("<option_m>", [<possible_values_if_any_or_None>])]
    }
    ```
    where options are strings of the form `--xyz` and `-x`.

    This dictionary iterates over all possible subcommand paths from the root command.

    The implementation of this function enumerates over the action types listed here:
    https://github.com/python/cpython/blob/81b9d9ddc20837ecd19f41b764e3f33d8ae805d5/Lib/argparse.py#L780
    """
    result: Dict[Tuple[str, ...], List[str]] = {}
    completion_options: List[Tuple[str, Optional[List[str]]]] = []

    optional_actions = parser._get_optional_actions()
    for option in optional_actions:
        choices = None
        if option.choices is not None:
            choices = [str(choice) for choice in option.choices]
        for option_string in option.option_strings:
            completion_options.append((option_string, choices))

    result[prefix] = completion_options

    subcommands: Dict[str, argparse.ArgumentParser] = {}
    positional_actions = parser._get_positional_actions()
    for action in positional_actions:
        if isinstance(action, argparse._SubParsersAction):
            subcommands = {**subcommands, **action.choices}

    for subcommand, subcommand_parser in subcommands.items():
        subcommand_result = command_info(subcommand_parser, (*prefix, subcommand))
        for path, info in subcommand_result.items():
            result[path] = info

    return result


def generate_completion(parser: argparse.ArgumentParser) -> str:
    """
    Args:
    1. parser - an argparse.ArgumentParser representing a CLI

    Returns: A bash completion script for the CLI represented by the parser.
    """
    pass

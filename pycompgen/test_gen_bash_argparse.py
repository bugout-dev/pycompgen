import argparse
import unittest

from . import gen_bash_argparse


class TestCommandInfo(unittest.TestCase):
    def test_command_info_with_simple_command(self):
        simple_parser = argparse.ArgumentParser()
        simple_parser.add_argument("-s", "--something", required=True, type=int)
        simple_parser.add_argument("-a", "--anything", required=False, type=int)
        info = gen_bash_argparse.command_info(simple_parser)
        self.assertDictEqual(
            info,
            {
                tuple(): [
                    ("-h", None),
                    ("--help", None),
                    ("-s", None),
                    ("--something", None),
                    ("-a", None),
                    ("--anything", None),
                ]
            },
        )

    def test_command_info_with_simple_command_without_help(self):
        simple_parser = argparse.ArgumentParser(add_help=False)
        simple_parser.add_argument("-s", "--something", required=True, type=int)
        simple_parser.add_argument("-a", "--anything", required=False, type=int)
        info = gen_bash_argparse.command_info(simple_parser)
        self.assertDictEqual(
            info,
            {
                tuple(): [
                    ("-s", None),
                    ("--something", None),
                    ("-a", None),
                    ("--anything", None),
                ]
            },
        )

    def test_command_info_with_command_with_choices(self):
        simple_parser = argparse.ArgumentParser()
        simple_parser.add_argument(
            "-s", "--something", required=True, choices=["lol", "rofl"]
        )
        info = gen_bash_argparse.command_info(simple_parser)
        self.assertDictEqual(
            info,
            {
                tuple(): [
                    ("-h", None),
                    ("--help", None),
                    ("-s", ["lol", "rofl"]),
                    ("--something", ["lol", "rofl"]),
                ]
            },
        )

    def test_command_info_with_subcommands(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        rofl_subparser = subparsers.add_parser("rofl")
        rofl_subparser.add_argument("-a")
        lol_subparser = subparsers.add_parser("lol")
        lol_subparser.add_argument("-a", choices=["x", "y"])
        lol_subparser.add_argument("-b", "--boom", action="store_true")
        info = gen_bash_argparse.command_info(parser)
        self.assertDictEqual(
            info,
            {
                tuple(): [
                    ("-h", None),
                    ("--help", None),
                ],
                ("rofl",): [
                    ("-h", None),
                    ("--help", None),
                    ("-a", None),
                ],
                ("lol",): [
                    ("-h", None),
                    ("--help", None),
                    ("-a", ["x", "y"]),
                    ("-b", None),
                    ("--boom", None),
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()

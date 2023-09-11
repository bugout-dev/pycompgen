import argparse
import unittest

from .inspect import possible_completions_by_context


class TestInspectSimple(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description="This is a parser to be used in tests"
        )

        subparsers = self.parser.add_subparsers()

        look_parser = subparsers.add_parser("look", help="Look at something")
        look_parser.add_argument(
            "--stare", action="store_true", help="Set this flag to get a good stare in"
        )

        speak_parser = subparsers.add_parser("speak", help="Say something")
        speak_parser.add_argument("words", nargs="+", help="Words to say")

    def test_possible_completions_by_context(self):
        completions = possible_completions_by_context(self.parser)
        self.assertDictEqual(
            completions,
            {
                tuple(): ["-h", "--help", "look", "speak"],
                ("look",): ["-h", "--help", "--stare"],
                ("speak",): ["-h", "--help"],
            },
        )


class TestInspectCommandWithSubcommandAndOptions(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description="This is a parser to be used in tests"
        )
        self.parser.add_argument("-l", help="Something something lll")

        subparsers = self.parser.add_subparsers()

        subcommand_parser = subparsers.add_parser(
            "a-subcommand", help="Something something subcommand"
        )
        subcommand_parser.add_argument(
            "--suboption", required=True, help="Something something suboption"
        )

    def test_possible_completions_by_context(self):
        completions = possible_completions_by_context(self.parser)
        self.assertDictEqual(
            completions,
            {
                tuple(): ["-h", "--help", "-l", "a-subcommand"],
                ("a-subcommand",): ["-h", "--help", "--suboption"],
            },
        )


if __name__ == "__main__":
    unittest.main()

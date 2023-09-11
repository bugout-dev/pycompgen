import argparse
import unittest

from .inspect import possible_completions_by_context


class TestInspectSimple(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description="This is a parser to be used in tests"
        )
        self.parser.add_argument(
            "-a", "--a", required=True, help="Something something a"
        )
        self.parser.add_argument(
            "-z", "--z", action="store_true", help="Something something z"
        )
        self.parser.add_argument(
            "some-positional-arg", nargs="+", help="Some positional argument"
        )

    def test_possible_completions_by_context(self):
        completions = possible_completions_by_context(self.parser)
        self.assertDictEqual(
            completions,
            {
                tuple(): [
                    "-a",
                    "--a",
                    "-h",
                    "--help",
                    "-z",
                    "--z",
                ],
            },
        )


class TestInspectSubcommands(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description="This is a parser to be used in tests"
        )

        self.subparsers = self.parser.add_subparsers()

        self.look_parser = self.subparsers.add_parser("look", help="Look at something")
        self.look_parser.add_argument(
            "--stare", action="store_true", help="Set this flag to get a good stare in"
        )

        self.speak_parser = self.subparsers.add_parser("speak", help="Say something")
        self.speak_parser.add_argument("words", nargs="+", help="Words to say")

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

    def test_possible_completions_by_context_for_subparser(self):
        completions = possible_completions_by_context(self.look_parser)
        self.assertDictEqual(
            completions,
            {
                tuple(): ["-h", "--help", "--stare"],
            },
        )


class TestInspectCommandWithSubcommandAndOptions(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser(
            description="This is a parser to be used in tests"
        )
        self.parser.add_argument("-l", help="Something something lll")

        self.subparsers = self.parser.add_subparsers()

        self.subcommand_parser = self.subparsers.add_parser(
            "a-subcommand", help="Something something subcommand"
        )
        self.subcommand_parser.add_argument(
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

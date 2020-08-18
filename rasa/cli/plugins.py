import argparse
import shutil
import subprocess
import sys
from typing import Text, List


def add_plugin_parser(parser: argparse.ArgumentParser) -> None:
    _register_plugin_fallback(parser)


def _register_plugin_fallback(parser: argparse.ArgumentParser) -> None:
    current_error_fn = parser.error

    def command_not_found(message: Text) -> None:
        args = sys.argv

        if len(args) >= 2 and shutil.which(_executable_name(args)):
            _run_plugin(args)
            args[0] = _executable_name(args)
        else:
            return current_error_fn(message)

    # This patches only the outermost parser but that's enough for our purposes
    parser.error = command_not_found


def _executable_name(args: List[Text]) -> Text:
    return f"rasa-{args[1]}"


def _run_plugin(current_args: List[Text]) -> None:
    current_args[0] = _executable_name(current_args)
    try:
        process = subprocess.run(current_args)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    exit(process.returncode)

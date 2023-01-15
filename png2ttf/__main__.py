import argparse
from pathlib import Path

from generate_font import generate_font


def parse_argument_input(argument: str) -> Path:
    path = Path(argument)
    if not path.is_file():
        argumentparser.error(f"{path} file not found")
    return path


def parse_argument_output(argument: str) -> Path:
    path = Path(argument)
    if path.is_dir():
        argumentparser.error(f"{path} is a directory")
    return path


argumentparser = argparse.ArgumentParser(
    prog="png2ttf",
    description="This tool converts a bitmap font where black pixels are background "
    "to a ttf font.",
)

argumentparser.add_argument(
    "input", type=parse_argument_input, help="Path to png file with the font glyphs"
)
argumentparser.add_argument(
    "output", type=parse_argument_output, help="Path to output font file"
)
argumentparser.add_argument(
    "width", type=int, help="The width of a character (in pixels)"
)
argumentparser.add_argument(
    "height", type=int, help="The height of a character (in pixels)"
)

namespace = argumentparser.parse_args()

input: Path = namespace.input
output: Path = namespace.output
width: int = namespace.width
height: int = namespace.height

generate_font(input, output, width, height)

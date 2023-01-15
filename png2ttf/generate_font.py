from pathlib import Path

import fontforge
from PIL import Image
from PIL.PyAccess import PyAccess

PRIVATE_RANGE = 0xE000
FONT_ENCODING = "UnicodeFull"
SCALE_FACTOR = 10
BACKGROUND_COLOR = (0, 0, 0)


def generate_font(image_file: Path, output_file: Path, width: int, height: int) -> None:
    image = Image.open(image_file)
    font = fontforge.font()
    font.ascent = height * SCALE_FACTOR
    font.descent = 0 * SCALE_FACTOR
    font.encoding = FONT_ENCODING

    pixels: PyAccess = image.load()  # type: ignore
    for j in range(image.height // height):
        for i in range(image.width // width):
            offset = i + j * (image.width // width)
            # generate two copies of char, in 0-256 and in private range
            for codepoint in [offset, PRIVATE_RANGE + offset]:
                char = font.createChar(codepoint)
                char.width = width * SCALE_FACTOR
                pen = char.glyphPen()
                # draw each non-background pixel as a square
                for y in range(height):
                    for x in range(width):
                        pixel: tuple[int, int, int] = pixels[
                            i * width + x, j * height + y
                        ]
                        if pixel != BACKGROUND_COLOR:
                            pen.moveTo(
                                (x * SCALE_FACTOR, (height - y) * SCALE_FACTOR)
                            )  # draw a pixel
                            pen.lineTo(
                                ((x + 1) * SCALE_FACTOR, (height - y) * SCALE_FACTOR)
                            )
                            pen.lineTo(
                                (
                                    (x + 1) * SCALE_FACTOR,
                                    (height - y - 1) * SCALE_FACTOR,
                                )
                            )
                            pen.lineTo(
                                (x * SCALE_FACTOR, (height - y - 1) * SCALE_FACTOR)
                            )
                            pen.closePath()

    font.generate(output_file.absolute().as_posix(), flags=("opentype"))

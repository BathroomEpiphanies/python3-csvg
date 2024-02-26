import sys

from pathlib import Path
from csvg import Canvas, Image


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
)

png = Image(
    id = 'png',
    content = Path('test.png'),
    left = 1,
    top = 1,
    width = 20,
    height = 10,
    preserveAspectRatio = "none",
)

jpg = Image(
    id = 'jpeg',
    content = Path('test.jpg'),
    left = 32,
    top = -2,
    width = 20,
    height = 8,
    preserveAspectRatio = "xMidYMin slice",
)

canvas.elements = [png, jpg]


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

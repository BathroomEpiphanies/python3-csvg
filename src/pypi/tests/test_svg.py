import sys

from pathlib import Path
from csvg import Canvas, SVG


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
    elements = [
        SVG(
            id = 'svg',
            content = Path('test.svg'),
            left = 1.00,
            top = 1.00,
            width = 20,
            height = 10,
        )
    ]
)


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

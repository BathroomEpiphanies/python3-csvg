import sys

from csvg import Canvas


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    width = 65,
    height = 12,
    elements = [],
)


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

import sys

from csvg import Canvas, Line


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
)

line1 = Line(
    id = 'line2',
    x1 = canvas.left+2,
    y1 = canvas.top+2,
    x2 = canvas.right-2,
    y2 = canvas.bottom-2,
    stroke = '#888800',
    stroke_width = 2,
    stroke_linecap = 'round',
)

line2 = Line(
    id = 'line1',
    x1 = canvas.left+2,
    y1 = canvas.bottom-2,
    x2 = canvas.right-2,
    y2 = canvas.top+2,
    stroke = '#880088',
    stroke_width = 2,
    stroke_linecap = 'square',
    stroke_opacity = 0.6,
)

canvas.elements = [line1, line2]


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

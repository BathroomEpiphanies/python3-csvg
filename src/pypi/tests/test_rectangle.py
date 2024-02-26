import sys

from csvg import Canvas, Rectangle


canvas = Canvas(
    left = 0,
    top = 0,
    width = 65.0,
    height = 12.0,
    units = 'mm',
    elements = [
        rectangle := Rectangle(
            id = 'rectangle',
            left = 10.000,
            right = 30.000,
            top = 4.000,
            height = 30.000,
            fill = '#008888',
            fill_opacity = 0.8,
            stroke = '#0000ff',
            stroke_width = 2,
            stroke_linejoin = 'round',
            font_size = 2,
        )
    ]
)


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

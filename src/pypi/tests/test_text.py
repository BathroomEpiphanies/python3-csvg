import sys

from csvg import Canvas, Text


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0.0,
    top = 0.0,
    width = 65.0,
    height = 12.0,
)

text = Text(
    id = 'text',
    content = 'Hello World!',
    x = canvas.width/2,
    y = canvas.height/2,
    font_size = 8,
    font_family = 'Liberation Sans',
    font_weight = 'bold',
    text_anchor = 'middle',
    dominant_baseline = 'mathematical',
    fill = '#8844cc',
    fill_opacity = 0.9,
    stroke = '#000000',
    stroke_width = 0.2,
    stroke_linejoin = 'round',
    stroke_linecap = 'round',
)

canvas.elements = [text]


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)


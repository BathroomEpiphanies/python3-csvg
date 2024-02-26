import random
import sys

from csvg import Canvas, Circle



canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
    elements = []
)

random.seed(0)
for i in range(256):
    canvas.elements.append(
        Circle(
            id = f'circle_{i}',
            cx = random.randint(-15, 80),
            cy = random.randint(-15, 27),
            r = random.randint(2, 12),
            stroke = f'#{random.randint(0,2**24):06x}',
            stroke_width = random.randint(2,8)/10,
            stroke_opacity = 0.8,
            fill_opacity = 0,
        )
    )



svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

import sys

from csvg import Canvas, QRCode


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
)

qr_code_1 = QRCode(
    id = 'qr_code_1',
    content = 'THIS_IS_A_QR_CODE',
    right = canvas.right-4,
    top = canvas.top+2,
    bottom = canvas.bottom-2,
)

qr_code_2 = QRCode(
    id = 'qr_code_2',
    content = 'THIS_TEXT_IS_TOO_LONG_TO_FIT_THE_QR_CODE',
    version = 1,
    left = canvas.left+4,
    top = canvas.top+2,
    bottom = canvas.bottom-2,
)

canvas.elements = [qr_code_1, qr_code_2]


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

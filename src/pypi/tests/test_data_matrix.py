import sys

from csvg import Canvas, DataMatrix


canvas = Canvas(
    id = 'canvas',
    units = 'mm',
    left = 0,
    top = 0,
    width = 65,
    height = 12,
)

data_matrix_1 = DataMatrix(
    id = 'data_matrix_1',
    content = 'THIS_IS_TRYING_TO_BE_A_DATAMATRIX',
    top = 1,
    height = 10,
    symbol_size = '16x16',
    encoding = 'a',
    fill = '#000000',
)
data_matrix_1.left = 1/3*canvas.width-data_matrix_1.width/2

data_matrix_2 = DataMatrix(
    id = 'data_matrix_2',
    content = 'THIS_IS_A_DATAMATRIX',
    top = 1,
    height = 10,
    symbol_size = '32x32',
    encoding = 'a',
    fill = '#000000',
)
data_matrix_2.left = 2/3*canvas.width-data_matrix_2.width/2

canvas.elements = [data_matrix_1, data_matrix_2]


svg = canvas.solve().to_svg()
print(canvas._model, file=sys.stderr)
print(svg)

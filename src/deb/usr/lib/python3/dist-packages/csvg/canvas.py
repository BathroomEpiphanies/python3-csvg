from __future__ import annotations

from .element import Element
from .lib import get_float


class Canvas(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'left',
        'right',
        'width',
        'top',
        'bottom',
        'height',
    }
    
    _ATTRIBUTES_TO_TAGS = Element._ATTRIBUTES_TO_TAGS | {
        'units': None,
        'left': None,
        'right': None,
        'width': None,
        'top': None,
        'bottom': None,
        'height': None,
        'elements': None,
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__init__(**attributes)
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
    
    
    def _add_to_solver(self, solver):
        for element in self.elements:
            element._add_to_solver(solver)
        super()._add_to_solver(solver)
    
    
    def to_svg(self):
        left = get_float(self._model, self.left)
        top = get_float(self._model, self.top)
        width = get_float(self._model, self.width)
        height = get_float(self._model, self.height)
        return f'<svg' + \
                ' xmlns="http://www.w3.org/2000/svg"' + \
                ' xmlns:xlink="http://www.w3.org/1999/xlink"' + \
               f' width="{width}{self.units}" height="{height}{self.units}"' + \
               f' viewBox="{left} {top} {width} {height}"' + \
               f' {self._get_tags()}>\n' + \
                '    \n'.join(element.to_svg() for element in self.elements) + \
                '\n</svg>'

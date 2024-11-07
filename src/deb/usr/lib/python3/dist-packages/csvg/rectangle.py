from __future__ import annotations

from collections import deque

from .element import Element


class Rectangle(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'left',
        'right',
        'width',
        'top',
        'bottom',
        'height',
    }
    
    _ATTRIBUTES_TO_TAGS = Element._ATTRIBUTES_TO_TAGS | {
        'left': 'x',
        'top': 'y',
        'right': None,
        'bottom': None,
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__init__(**attributes)
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
    
    
    def _to_svg(
            self,
    ) -> deque[str]:
        return deque([f'<rect {self._get_tags()} />'])

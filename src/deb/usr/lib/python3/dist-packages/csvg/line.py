from __future__ import annotations

from collections import deque

from .element import Element


class Line(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'x1',
        'y1',
        'x2',
        'y2',
    }
    
    
    def _to_svg(
            self,
    ) -> deque[str]:
        return deque([f'<line {self._get_tags()} />'])

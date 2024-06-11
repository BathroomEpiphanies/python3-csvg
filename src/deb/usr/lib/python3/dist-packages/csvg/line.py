from __future__ import annotations

from .element import Element


class Line(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'x1',
        'y1',
        'x2',
        'y2',
    }
    
    
    def to_svg(self):
        return f'<line {self._get_tags()} />'

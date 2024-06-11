from __future__ import annotations

from .element import Element


class Circle(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'cx',
        'cy',
        'r',
    }
    
    
    def to_svg(self):
        return f'<circle {self._get_tags()} />'

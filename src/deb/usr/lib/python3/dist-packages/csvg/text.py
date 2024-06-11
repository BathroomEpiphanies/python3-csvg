from __future__ import annotations

from .element import Element


class Text(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'x',
        'y',
        'font_size',
    }
    
    
    def to_svg(self):
        return f'<text {self._get_tags()}>{self.content}</text>'

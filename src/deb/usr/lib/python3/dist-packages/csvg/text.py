from __future__ import annotations

from collections import deque

from .element import Element


class Text(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'x',
        'y',
        'font_size',
    }
    
    
    def _to_svg(
            self,
    ) -> deque[str]:
        return deque([f'<text {self._get_tags()}>{self.content}</text>'])

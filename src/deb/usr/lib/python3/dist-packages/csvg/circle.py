from __future__ import annotations

from collections import deque

from .element import Element


class Circle(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'cx',
        'cy',
        'r',
    }
    
    
    def _to_svg(
            self,
    ) -> deque[str]:
        return deque([f'<circle {self._get_tags()} />'])

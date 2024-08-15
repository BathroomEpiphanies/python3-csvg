from __future__ import annotations

import re
from pathlib import Path

from .element import Element


class SVG(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'left',
        'right',
        'width',
        'top',
        'bottom',
        'height',
    }
    
    
    _ATTRIBUTES_TO_TAGS = Element._ATTRIBUTES_TO_TAGS | {
        '_viewBox': None
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__init__(**attributes)
        if isinstance(self.content, Path):
            with open(self.content, mode='r') as fp:
                self.content = fp.read()
        self.content = re.sub(r'width="([0-9.]+)mm"', r'width="\1"', self.content)
        self.content = re.sub(r'height="([0-9.]+)mm"', r'height="\1"', self.content)
        pattern = re.compile(r'.*viewBox="([0-9.-]+) ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)".*', re.DOTALL)
        match = re.match(pattern, self.content)
        self._viewBox = match.groups()
        x,y,w,h = self._viewBox
        
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
        if 'width' not in attributes and not ('left' in attributes and 'right' in attributes):
            self.width = float(w)/float(h) * self.height
        if 'height' not in attributes and not ('top' in attributes and 'bottom' in attributes):
            self.height = float(h)/float(w) * self.width
    
    
    def to_svg(self):
        x,y,w,h = self._viewBox
        transforms = [
            f'translate({self._get_value(self.left)} {self._get_value(self.top)})',
            f'scale({self._get_value(self.width)/float(w)} {self._get_value(self.height)/float(h)})',
            f'translate({-float(x)} {-float(y)})',

        ]
        output = [f'<g transform="{" ".join(transforms)}" {self._get_tags()}>']
        output.extend(self.content.split('\n'))
        output.append('</g>')
        return '\n'.join(output)

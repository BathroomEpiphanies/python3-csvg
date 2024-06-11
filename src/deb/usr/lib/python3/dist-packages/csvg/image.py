from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image as _PIL_Image

from .element import Element


class Image(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'left',
        'right',
        'width',
        'top',
        'bottom',
        'height',
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__init__(**attributes)
        if isinstance(self.content, Path):
            with open(self.content, mode='rb') as fp:
                self.content = fp.read()
        byteio = io.BytesIO(self.content)
        image = _PIL_Image.open(byteio)
        self.content = base64.b64encode(self.content).decode()
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
        if 'width' not in attributes and not ('left' in attributes and 'right' in attributes):
            self.width = float(image.width)/float(image.height) * self.height
        if 'height' not in attributes and not ('top' in attributes and 'bottom' in attributes):
            self.height = float(image.height)/float(image.width) * self.width
    
    
    def to_svg(
            self,
    ) -> str:
        return f'<image {self._get_tags()} xlink:href="data:base64,{self.content}"/>'

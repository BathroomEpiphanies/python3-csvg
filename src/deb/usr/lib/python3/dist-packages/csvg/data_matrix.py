from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .element import Element


class DataMatrix(Element):
    
    _ARITHMETICALS = Element._ARITHMETICALS | {
        'left',
        'right',
        'width',
        'top',
        'bottom',
        'height',
    }
    
    
    _ATTRIBUTES_TO_TAGS = Element._ATTRIBUTES_TO_TAGS | {
        'encoding': None,
        'symbol_size': None,
        '_w': None,
        '_h': None,
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__init__(**attributes)
        command = [
            'dmtxwrite',
            '--symbol-size', self.symbol_size,
            '--encoding', getattr(self, 'encoding', 'b'),
            '--margin', '1',
            '--module', '1',
            '--format', 'svg',
        ]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate(input=self.content.encode())
        if process.returncode != 0:
            print(stderr.decode(), file=sys.stderr)
            err_svg = Path(__file__).parent/'data_matrix_fail.svg'
            stdout = open(err_svg, 'rb').read()
            self.symbol_size = '48x48'
        stdout = stdout.decode().split('\n')
        self.content = [s.strip() for s in stdout if 'rect' in s]
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
        self._w,self._h = (int(n) for n in self.symbol_size.split('x'))
        if 'width' not in attributes and not ('left' in attributes and 'right' in attributes):
            self.width = float(self._w)/float(self._h) * self.height
        if 'height' not in attributes and not ('top' in attributes and 'bottom' in attributes):
            self.height = float(self._h)/float(self._w) * self.width
    
    
    def to_svg(
            self
    ) -> str:
        transforms = [
            f' translate({self._get_value(self.left)} {self._get_value(self.top)})',
            f' scale({self._get_value(self.width)/float(self._w)} {self._get_value(self.height)/float(self._h)})',
            f' translate(-1 -1)',
        ]
        output = [f'<g transform="{" ".join(transforms)}" {self._get_tags()}>']
        output.extend(self.content)
        output.append('</g>')
        return '\n'.join(output)

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from .element import Element


class QRCode(Element):
    
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
        command = [
            'qrencode',
            '--size', '1',
            '--margin', '0',
            '--type', 'svg',
            '--output', '-',
        ]
        if hasattr(self, 'version'):
            command.extend([
                '--symversion', str(self.version),
                '--strict-version',
        ])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate(input=self.content.encode())
        if process.returncode != 0:
            print(stderr.decode(), file=sys.stderr)
            err_svg = Path(__file__).parent/'qr_code_fail.svg'
            stdout = open(err_svg, 'rb').read()
        stdout = stdout.decode()
        pattern = re.compile(r'.*viewBox="([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+)".*', re.DOTALL)
        match = re.match(pattern, stdout)
        self._viewBox = match.groups()
        x,y,w,h = self._viewBox
        stdout = stdout.split('\n')
        self.content = [s.strip() for s in stdout if 'rect' in s]
        self._constraints.append(self.width == self.right - self.left)
        self._constraints.append(self.height == self.bottom - self.top)
        if 'width' not in attributes and not ('left' in attributes and 'right' in attributes):
            self.width = float(w)/float(h) * self.height
        if 'height' not in attributes and not ('top' in attributes and 'bottom' in attributes):
            self.height = float(h)/float(w) * self.width
    
    
    def to_svg(
            self
    ) -> str:
        x,y,w,h = self._viewBox
        transforms = [
            f'translate({self._get_value(self.left)} {self._get_value(self.top)})',
            f'scale({self._get_value(self.width)/float(w)} {self._get_value(self.height)/float(h)})',
        ]
        output = [f'<g transform="{" ".join(transforms)}" {self._get_tags()}>']
        output.extend(self.content)
        output.append('</g>')
        return '\n'.join(output)

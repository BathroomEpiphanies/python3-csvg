from __future__ import annotations

import sys

from abc import ABC, abstractmethod
from typing import Any

import z3

from .lib import get_float


class Element(ABC):
    
    _ARITHMETICALS = set()
    
    _ATTRIBUTES_TO_TAGS = {
        #'id': None,
        'content': None,
        'left': 'x',
        'top': 'y',
        'font_family': 'font-family',
        'font_size': 'font-size',
        'font_weight': 'font-weight',
        'text_anchor': 'text-anchor',
        'dominant_baseline': 'dominant-baseline',
        'letter_spacing': 'letter-spacing',
        'font_stretch': 'font-stretch',
        'fill_opacity': 'fill-opacity',
        'stroke_width': 'stroke-width',
        'stroke_dasharray': 'stroke-dasharray',
        'stroke_linejoin': 'stroke-linejoin',
        'stroke_linecap': 'stroke-linecap',
        'stroke_miterlimit': 'stroke-miterlimit',
        'stroke_opacity': 'stroke-opacity',
    }
    
    
    def __init__(
            self,
            **attributes,
    ) -> None:
        super().__setattr__('_attributes', set())
        super().__setattr__('_constraints', [])
        super().__setattr__('_arithmeticals', {})
        super().__setattr__('_model', None)
        
        if 'id' in attributes:
            self.__setattr__('id', attributes['id'])
        else:
            self.__setattr__('id', f'{type(self).__name__}_{hex(id(self))}')
        
        for attribute,value in attributes.items():
            self.__setattr__(attribute, value)
    
    
    def __setattr__(
            self,
            __name:str,
            __value:Any,
    ) -> None:
        super().__getattribute__('_attributes').add(__name)
        if __name in type(self)._ARITHMETICALS:
            if __name not in self._arithmeticals:
                super().__setattr__(__name, z3.Real(f'{self.__getattribute__("id")}.{__name}'))
            self._arithmeticals[__name] = self.__getattribute__(__name)==__value
        else:
            super().__setattr__(__name, __value)
    
    
    def __getattribute__(
            self,
            __name:str,
    ) -> Any:
        if __name in type(self)._ARITHMETICALS:
            if __name not in self._arithmeticals:
                super().__setattr__(__name, z3.Real(f'{self.__getattribute__("id")}.{__name}'))
        return super().__getattribute__(__name)
    
    
    def solve(
            self,
            solver = None,
    ) -> Element:
        if solver is not None:
            super().__setattr__('_solver', solver)
        else:
            super().__setattr__('_solver', z3.Solver())
        if hasattr(self, 'elements'):
            for element in self.elements:
                element.solve(self._solver)
        if solver is None:
            self._add_to_solver(self._solver)
            result = self._solver.check()
            print('Unsat core', file=sys.stderr)
            print(self._solver.unsat_core(), file=sys.stderr)
            print(f'Result: {result}', file=sys.stderr)
            model = self._solver.model()
            self._set_model(model)
        return self
    
    
    def _set_model(
            self,
            model,
    ) -> None:
        super().__setattr__('_model', model)
        if hasattr(self, 'elements'):
            for element in self.elements:
                element._set_model(model)
    
    
    def _add_to_solver(
            self,
            solver,
    ) -> None:
        print(f'Adding {self.id} to solver', file=sys.stderr)
        for _,value in self._arithmeticals.items():
            print(str(value), file=sys.stderr)
            solver.assert_and_track(value, str(value))
        for value in self._constraints:
            print(str(value), file=sys.stderr)
            solver.assert_and_track(value, str(value))
    
    
    @abstractmethod
    def to_svg(
        self,
    ) -> str:
        ...
    
    
    def _get_value(
            self,
            attribute,
    ) -> float:
        return get_float(self._model, attribute)
    
    
    def _get_tags(
            self,
            attributes = [],
    ) -> str:
        output = []
        if not attributes:
            attributes = self._attributes | self._ARITHMETICALS
            #attributes = self._attributes | self._arithmeticals.keys()
        for attribute in attributes:
            tag = self._ATTRIBUTES_TO_TAGS.get(attribute, attribute)
            if tag is None:
                continue
            value = self.__getattribute__(attribute)
            if isinstance(value, z3.ArithRef):
                value = get_float(self._model, value)
            output.append(f'{tag}="{value}"')
        return ' '.join(output)

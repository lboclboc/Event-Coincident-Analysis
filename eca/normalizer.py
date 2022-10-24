#!/usr/bin/env python3

import re
from typing import Protocol

class Normalizer(Protocol):
    normalizers = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Normalizer.normalizers[cls.tag] = cls
        print(f"Registering class {cls}")

    @staticmethod
    def create_from_str(name: str):
        print(f"Generating object from {name} ")
        return Normalizer.normalizers[name]()

    def normalize(sel, line: str) -> str:
        ...

class NoDigits(Normalizer):
    tag = "no-digits"
    _re = re.compile(r'\d+')

    def normalize(self, line: str) -> str:
        return self._re.sub('9', line)

class NoPunctuation(Normalizer):
    tag = "no-punctuation"
    _re = re.compile(r'[^\w\s]+')

    def normalize(self, line: str) -> str:
        return self._re.sub('_', line)


if __name__ == "__main__":
    s = "hejsan23-+:()hopp42"
    n1 = Normalizer.create_from_str("no-digits")
    n2 = Normalizer.create_from_str("no-punctuation")
    print(f"normalizing {s} -> {n1.normalize(n2.normalize(s))}")

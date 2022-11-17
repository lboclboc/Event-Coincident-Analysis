#!/usr/bin/env python3

import re
from typing import Protocol

class Normalizer(Protocol):
    normalizers = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Normalizer.normalizers[cls.tag] = cls

    @staticmethod
    def create_from_str(name: str):
        return Normalizer.normalizers[name]()

    def normalize(sel, line: str) -> str:
        ...

class NoDigits(Normalizer):
    tag = "no-digits"
    _re = re.compile(r'\d+')

    def normalize(self, line: str) -> str:
        return self._re.sub('9', line)

class NoPunctuation(Normalizer):
    tag = "no-punctuations"
    _re = re.compile(r'[^\w\s]+')

    def normalize(self, line: str) -> str:
        return self._re.sub('_', line)

class NoChangeid(Normalizer):
    tag = "no-changeid"
    _re = re.compile(r"\sI[0-9a-f]+\s")

    def normalize(self, line: str) -> str:
        return self._re.sub(' change-id ', line)

class NoJoltHash(Normalizer):
    tag = "no-jolt-hash"
    _re = re.compile(r"\[[0-9a-f]+\]")

    def normalize(self, line: str) -> str:
        return self._re.sub('[jolt-hash]', line)

class NoUUID(Normalizer):
    tag = "no-uuid"
    _re = re.compile(r"[0-9a-f]{8}-"
                     r"[0-9a-f]{4}-"
                     r"[0-9a-f]{4}-"
                     r"[0-9a-f]{4}-"
                     r"[0-9a-f]{12}")

    def normalize(self, line: str) -> str:
        return self._re.sub('UUID', line)


if __name__ == "__main__":
    s = "hejsan23-+:()hopp42"
    n1 = Normalizer.create_from_str("no-digits")
    n2 = Normalizer.create_from_str("no-punctuation")
    print(f"normalizing {s} -> {n1.normalize(n2.normalize(s))}")

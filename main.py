from dataclasses import dataclass
from typing import Self


def contains_all[T](__a: set[T], __b: set[T]) -> bool:
    return all(item in __a for item in __b)

def contains_any[T](__a: set[T], __b: set[T]) -> bool:
    return any(item in __a for item in __b)



@dataclass
class FD:
    lhs: set[str]
    rhs: set[str]

    def __str__(self) -> str:
        left = list(self.lhs)[0] if len(self.lhs) == 1 else self.lhs
        right = list(self.rhs)[0] if len(self.rhs) == 1 else self.rhs
        return f"{left!r} -> {right!r}"

    def copy(self) -> Self:
        return self.__class__(lhs=self.lhs.copy(), rhs=self.rhs.copy())


@dataclass
class Relation:
    attrs: set[str]

    def contains_all(self, attrs: set[str]) -> bool:
        return contains_all(self.attrs, attrs)

    def contains_any(self, attrs: set[str]) -> bool:
        return contains_any(self.attrs, attrs)

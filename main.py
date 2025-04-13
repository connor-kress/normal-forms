from dataclasses import dataclass
from typing import Optional, Self
from pprint import pprint


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


def get_primary_key(relation: Relation, deps: list[FD]) -> set[str]:
    key = relation.attrs.copy()
    for dep in deps:
        # print(f"\tDep: {dep}")
        if relation.contains_all(dep.lhs):
            # print("\tcontains")
            key -= dep.rhs
        else:
            # print("\tnot contains")
            pass
    return key


def main() -> None:
    # relation = Relation({"A", "B", "C", "D"})
    relation = Relation({
        "traveler ssn", "agent", "years experience",
         "trip id", "start location", "end location",
         "passport number", "expiration date",
    })
    deps = [
        # FD({"A"}, {"C"}),
        # FD({"C"}, {"D"}),
        # FD({"A", "C"}, {"D"}),
        FD({"agent"}, {"years experience"}),
        FD({"traveler ssn"}, {"passport number"}),
        FD({"passport number"}, {"expiration date"}),
        FD({"trip id"}, {"start location", "end location"}),
    ]
    print("Relation:")
    pprint(relation)
    print("\nDependencies:")
    for dep in deps:
        print(dep)
    print()
    print(get_primary_key(relation, deps))


if __name__ == "__main__":
    main()

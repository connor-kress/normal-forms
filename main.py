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

    def copy(self) -> Self:
        return self.__class__(attrs=self.attrs.copy())

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


def get_dependency_violation(
    relation: Relation,
    deps: list[FD],
    key: set[str],
) -> Optional[FD]:
    # print(f"GET_DEPENDENCY_VIOLATION({relation.attrs})")
    transitive_dep: Optional[FD] = None
    for dep in deps:
        if not relation.contains_all(dep.lhs) or \
           not relation.contains_any(dep.rhs):
            # Inapplicable dependency
            continue
        if contains_all(dep.lhs, key):
            print("Valid dependency:", dep)
        elif contains_all(key, dep.lhs):
            print("Partial dependency:", dep)
            return dep.copy()
        else:
            print("Transitive dependency:", dep)
            if transitive_dep is None:
                transitive_dep = dep.copy()
    return transitive_dep


def get_cover(attrs: set[str], deps: list[FD]) -> set[str]:
    cover = attrs.copy()
    while True:
        # print(f"\tcover: {cover}")
        added = False
        for dep in deps:
            if contains_all(cover, dep.lhs) and not contains_all(cover, dep.rhs):
                # print(f"\tAdding dependency: {dep}")
                cover = cover.union(dep.rhs)
                added = True
        if not added:
            break
    return cover


def bcnf_decomposition(
    relations: list[Relation],
    deps: list[FD],
) -> list[Relation]:
    relations = [rel.copy() for rel in relations]
    while True:
        print("\nRelations: ")
        pprint(relations)
        print()
        violation_found = False
        for i, relation in enumerate(relations):
            key = get_primary_key(relation, deps)
            # print("Key:", key)
            violation = get_dependency_violation(relation, deps, key)
            if violation is None:
                continue
            else:
                violation_found = True
            # print("Violation:", violation)
            cover = get_cover(violation.lhs, deps)
            # print("Cover:", cover)
            new_relation = Relation(cover)
            reduced_relation = Relation(
                relation.attrs.difference(cover.difference(violation.lhs))
            )
            # print(f"{new_relation=}")
            # print(f"{reduced_relation=}")
            del relations[i]
            relations.insert(i, new_relation)
            relations.insert(i, reduced_relation)
            break
        if not violation_found:
            break
    return relations


def main() -> None:
    relation = Relation({
        "traveler ssn", "agent", "years experience",
         "trip id", "start location", "end location",
         "passport number", "expiration date",
    })
    deps = [
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
    new_relations = bcnf_decomposition([relation], deps)
    print("\nFinal relations:")
    pprint(new_relations)


if __name__ == "__main__":
    main()

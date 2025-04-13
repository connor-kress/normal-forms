from dataclasses import dataclass
from typing import Optional, Self


def contains_all[T](__a: set[T], __b: set[T]) -> bool:
    return all(item in __a for item in __b)


def contains_any[T](__a: set[T], __b: set[T]) -> bool:
    return any(item in __a for item in __b)


@dataclass
class FD:
    """Represents a functional dependency of database attributes."""

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
    """Represents a database relation (or table) as set of attributes."""

    attrs: set[str]

    def copy(self) -> Self:
        return self.__class__(attrs=self.attrs.copy())

    def contains_all(self, attrs: set[str]) -> bool:
        return contains_all(self.attrs, attrs)

    def contains_any(self, attrs: set[str]) -> bool:
        return contains_any(self.attrs, attrs)

    def format(self, deps: list[FD]) -> str:
        key = get_primary_key(self, deps)
        key_str = ", ".join(map(str, key))
        remaining_attrs = self.attrs - key
        remaining_str = ", ".join(map(str, remaining_attrs))
        if remaining_attrs:
            return f"({key_str}, {remaining_str})"
        else:
            return f"({key_str})"


def print_relations(relations: list[Relation], deps: list[FD]) -> None:
    for i, relation in enumerate(relations):
        print(f"\tR{i+1}: {relation.format(deps)}")


def get_primary_key(relation: Relation, deps: list[FD]) -> set[str]:
    """Returns the primary key of a relation given a set of
    functional dependencies.
    """
    key = relation.attrs.copy()
    for dep in deps:
        if relation.contains_all(dep.lhs):
            key -= dep.rhs
        else:
            pass
    return key


def get_dependency_violation(
    relation: Relation,
    deps: list[FD],
    key: set[str],
) -> Optional[FD]:
    """Returns the functional dependency that is violated by a
    relation in terms of the Boyce-Codd Normal Form if it exists,
    otherwise returns `None`.
    """
    # print(f"GET_DEPENDENCY_VIOLATION({relation.attrs})")
    transitive_dep: Optional[FD] = None
    for dep in deps:
        if not relation.contains_all(dep.lhs) or \
           not relation.contains_any(dep.rhs):
            continue # Inapplicable dependency
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
    """Returns the cover of a set of attributes given a set of
    functional dependencies.
    """
    cover = attrs.copy()
    while True:
        added = False
        for dep in deps:
            if contains_all(cover, dep.lhs) and not contains_all(cover, dep.rhs):
                cover = cover.union(dep.rhs)
                added = True
        if not added:
            break
    return cover


def bcnf_decomposition(
    relations: list[Relation],
    deps: list[FD],
) -> list[Relation]:
    """Decomposes a set a relations based on the Boyce-Codd
    Normal Form reduction algorithm.
    """
    relations = [rel.copy() for rel in relations]
    while True:
        print("\nRelations: ")
        print_relations(relations, deps)
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
                relation.attrs - (cover - violation.lhs)
            )
            # print(f"New relation: {new_relation.format(deps)}")
            # print(f"Reduced relation: {reduced_relation.format(deps)}")
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
    print(relation.format(deps))
    print("\nDependencies:")
    for dep in deps:
        print(f"\t{dep}")
    print()
    new_relations = bcnf_decomposition([relation], deps)
    print("\nFinal relations:")
    print_relations(new_relations, deps)


if __name__ == "__main__":
    main()

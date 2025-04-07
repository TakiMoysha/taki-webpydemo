from typing import Annotated, Protocol


class ISpecification[T](Protocol):
    def is_satisfied_by(self, obj: T, *args, **kwrags) -> bool: ...


__all__ = [
    "ISpecification",
]

# ====================================================== EXAMPLE


class UserModel:
    jobs: list
    is_superuser: bool


class SuperuserSpec[T: UserModel](ISpecification):
    def is_satisfied_by(self, obj: T) -> bool:
        return obj.is_superuser


class HasJobSpec[T: UserModel](ISpecification):
    def is_satisfied_by(self, obj: T) -> bool:
        return len(obj.jobs) > 0


class InWaitingListSpec[T: UserModel](ISpecification):
    def is_satisfied_by(self, obj: T, repository: Annotated[T, HasJobSpec]) -> bool:
        return True


# ====================================================== EXAMPLE
def by_spec(collection: list, spec: ISpecification) -> list:
    return [item for item in collection if spec.is_satisfied_by(item)]


# ====================================================== EXAMPLE

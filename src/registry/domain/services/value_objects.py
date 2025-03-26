from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from registry.domain.services.exceptions import InvalidSeviceDataError
from wsdk.validators import IValidator, UUIDValidator
from wsdk.value_object import BaseValueObject


## =================================================== VALIDATORS
class RegistryServiceNameValidator(IValidator[str | None]):
    def __call__(self, value: str | None) -> None:
        if value is None:
            return

        if not value.isalnum():
            non_alphabetic_msg = "Service name must be alphanumeric"
            raise InvalidSeviceDataError(servicename=value, msg=non_alphabetic_msg)

        if len(value) < 3 or len(value) > 32:
            length_msg = "Service name must be at least 3 characters long"
            raise InvalidSeviceDataError(servicename=value, msg=length_msg)


@dataclass(eq=False, slots=True)
class ServiceId(BaseValueObject[UUID]):
    value: UUID
    validators: tuple[IValidator] = field(default_factory=lambda: (UUIDValidator(),), kw_only=True, init=False)


@dataclass(eq=False, slots=True)
class ServiceName(BaseValueObject[str | None]):
    value: str
    validators: tuple[IValidator] = (RegistryServiceNameValidator(),)


@dataclass(eq=False, slots=True)
class ServiceAddress(BaseValueObject[str]):
    value: str
    validators: tuple[IValidator] = tuple[IValidator]()

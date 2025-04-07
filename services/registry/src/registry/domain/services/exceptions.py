from dataclasses import dataclass

from registry.domain.exceptions import DomainError


@dataclass(eq=False, slots=True)
class ServiceWasDeletedError(DomainError):
    servicename: str

    @property
    def description(self) -> str:
        return f"The service with <{self.servicename}> name was deleted"


@dataclass(eq=False, slots=True)
class ServiceNotRegisteredError(DomainError):
    servicename: str

    @property
    def description(self) -> str:
        return f"The service with <{self.servicename}> name was not registered"


@dataclass(eq=False, slots=True)
class ServiceAlreadyExistsError(DomainError):
    servicename: str

    @property
    def description(self) -> str:
        if self.servicename is None:
            return "A service with the servicename already exists"

        return f"A service with the <{self.servicename}> servicename already exists."


@dataclass(eq=False, slots=True)
class InvalidSeviceDataError(DomainError):
    servicename: str
    msg: str = "Bad value"

    @property
    def description(self) -> str:
        return f"Can't create service with data: {self.msg}"


@dataclass(eq=False, slots=True)
class ServiceCreationError(DomainError):
    servicename: str

    @property
    def description(self) -> str:
        return "unexpected error"

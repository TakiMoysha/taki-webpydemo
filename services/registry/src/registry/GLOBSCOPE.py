from registry.domain.services.utils import ServiceMetadata
from registry.domain.services.value_objects import ServiceAddress, ServiceName

SERVICE_MAP = set[ServiceMetadata]()

DATABASE = dict[str, ServiceMetadata]()

DNS = dict[ServiceName, ServiceAddress]()

from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec.components import Components
from litestar.openapi.spec.security_scheme import SecurityScheme

from messenger.config import get_settings

settings = get_settings()
config = OpenAPIConfig(
    title=settings.app.NAME,
    version=settings.app.version,
    components=Components(
        security_schemes={
            "BearerToken": SecurityScheme(type="oauth2", scheme="bearer"),
        },
    ),
    security=[{"OAuth2": []}],
    use_handler_docstrings=True,
    render_plugins=[ScalarRenderPlugin()],
)

import httpx
from supabase import create_client, Client, ClientOptions

# Configuración personalizada de httpx optimizada para entornos ASGI (Render)
# Usamos límites de conexión más estrictos y desactivamos HTTP/2 para evitar StreamReset.
http_client = httpx.Client(
    http2=False,
    timeout=httpx.Timeout(30.0, connect=10.0),
    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
    verify=True
)

def create_custom_client(url: str, key: str) -> Client:
    """Crea un cliente de Supabase con configuraciones de red optimizadas para producción."""
    options = ClientOptions(
        httpx_client=http_client,
        postgrest_client_timeout=45,
        storage_client_timeout=45
    )
    return create_client(url, key, options=options)

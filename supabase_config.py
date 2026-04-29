import httpx
from supabase import create_client, Client, ClientOptions

# Configuración personalizada de httpx para evitar errores de StreamReset en redes inestables (como Render)
# Usamos HTTP/1.1 explícitamente y aumentamos los timeouts.
http_client = httpx.Client(
    http2=False,  # Desactivar HTTP/2 para evitar errores de multiplexado (StreamReset)
    timeout=httpx.Timeout(30.0, connect=60.0),
    verify=True
)

def create_custom_client(url: str, key: str) -> Client:
    """Crea un cliente de Supabase con configuraciones de red optimizadas usando ClientOptions."""
    options = ClientOptions(
        httpx_client=http_client,
        postgrest_client_timeout=30,
        storage_client_timeout=30
    )
    return create_client(url, key, options=options)

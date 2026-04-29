# App_Fitness - Reglas de Desarrollo

## Tecnologías Principales
- **Framework:** Flet (Python)
- **Backend:** Supabase (Auth + PostgreSQL)
- **Entorno:** Python 3.12+ (Venv habilitado)

## Convenciones de Código
- **Estilo:** Seguir PEP 8.
- **Tipado:** Usar Type Hints en todas las funciones y clases.
- **UI:** Mantener el diseño modular en la carpeta `views/`. Cada vista debe recibir `page` y `user` como parámetros mínimos.
- **Base de Datos:** Centralizar todas las consultas en `db_manager.py`. No hacer llamadas directas a Supabase desde las vistas.
- **Variables de Entorno:** Usar siempre `dotenv` con rutas relativas para el archivo `.env`.

## Flujo de Trabajo
- Antes de cambios estructurales, consultar `models.py`.
- Mantener la compatibilidad con Cursor y Gemini CLI.
- No instalar dependencias nuevas sin registrarlas en `requirements.txt`.

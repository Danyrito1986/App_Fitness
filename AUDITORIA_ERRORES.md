# Desglose y Análisis de Errores - App_Fitness (Flet 0.21.2)

## 1. Errores de Atributos (Sintaxis)
*   **Error:** `AttributeError: module 'flet' has no attribute 'Icons'`
    *   **Causa:** Cambio de nomenclatura en Flet 0.25+. La versión 0.21.2 usa `icons` (minúscula).
    *   **Estado:** CORREGIDO. Se aplicó reversión masiva.
*   **Error:** `AttributeError: 'Page' object has no attribute 'window'`
    *   **Causa:** En 0.21.2, las propiedades de ventana están directamente en `page` (e.g., `page.window_width`), no en un objeto hijo `.window`.
    *   **Estado:** CORREGIDO. Se restauró la sintaxis clásica.
*   **Error:** `AttributeError: module 'flet' has no attribute 'NavigationDestination'`
    *   **Causa:** Problema de empaquetado o visibilidad en instalaciones Cloud.
    *   **Estado:** MITIGADO. Se implementó un "Survivor Import" con fallbacks.

## 2. Errores de Servidor (Despliegue)
*   **Error:** `AttributeError: 'Server' object has no attribute 'servers'`
    *   **Causa:** Incompatibilidad entre el método `ft.app(view=None)` de Flet 0.21.2 y versiones modernas de `uvicorn` (0.29+).
    *   **Estado:** CORREGIDO. Se fijó `uvicorn==0.20.0` y se simplificó el arranque.

## 3. Errores de Interfaz (Renderizado)
*   **Error:** `Container.__init__() got an unexpected keyword argument 'scroll'`
    *   **Causa:** `ft.Container` no soporta `scroll` en versiones recientes de Flet, pero sí en la 0.21.2.
    *   **Estado:** VALIDADO. Al estar en 0.21.2, esta propiedad vuelve a ser válida.

---
## Plan de Pruebas de Descarte
1. **Prueba A (Importaciones):** Verificar que todos los módulos carguen sin `ImportError`.
2. **Prueba B (UI):** Instanciar cada vista (Home, Workout, Diet, Profile, Progress) con mocks de datos.
3. **Prueba C (Conectividad):** Simular ping a Supabase.
4. **Prueba D (Cierre):** Verificar que la app no colapse al cerrar sesiones (Bug de Uvicorn).

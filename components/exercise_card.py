import flet as ft
import threading

def ExerciseCard(ex, is_checked_func, on_check, on_save_peso, on_timer, sugerencia_txt):
    """
    Componente funcional que retorna una tarjeta de ejercicio en Flet con diseño revisado.
    La imagen ahora se sitúa en la parte superior, centrada, y las series debajo.
    """
    lbl_sugerencia = ft.Text(f"Sugerencia: {sugerencia_txt}", size=11, color="#FFD700", weight="bold")
    
    # Fila de series (Checkboxes) centrada
    row_series = ft.Row(wrap=True, spacing=5, alignment="center", vertical_alignment="center")
    
    def create_on_change(ex_id, idx, t):
        def handler(e):
            on_check(ex_id, idx, e.control.value, t)
            e.control.update()
        return handler

    # 1. Añadir Checkboxes
    for s_idx in range(ex.series):
        is_checked = is_checked_func(ex.id, s_idx)
        cb = ft.Checkbox(
            label=f"S{s_idx+1}", 
            value=is_checked,
            fill_color="#FFD700",
            on_change=create_on_change(ex.id, s_idx, ex.descanso)
        )
        row_series.controls.append(cb)

    txt_peso_hoy = ft.TextField(label="Kg", width=70, height=35, text_size=12, border_color="#FFD700")

    def internal_guardar_peso(e):
        on_save_peso(e, ex.nombre, txt_peso_hoy, lbl_sugerencia)

    # RETORNO CON ESTRUCTURA REVISADA (Imagen Arriba, Series Abajo)
    return ft.Container(
        content=ft.Column([
            # Nivel 1: Título y Timer
            ft.Row([
                ft.Text(ex.nombre, weight="bold", size=15, expand=True),
                ft.IconButton(ft.icons.TIMER, icon_color="#FFD700", on_click=lambda _: on_timer(ex.descanso))
            ]),
            
            # Nivel 2: Imagen Técnica (CENTRADA Y ARRIBA - MÁS GRANDE)
            ft.Container(
                content=ft.Image(
                    src=ex.imagen_url,
                    width=180,
                    height=180,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=10,
                ),
                alignment=ft.alignment.center,
                border_radius=10,
                bgcolor="black",
                width=None, # Ocupa el ancho disponible para centrar
                height=200,
                padding=5
            ),
            
            # Nivel 3: Series (Checkboxes)
            row_series,
            
            # Nivel 4: Stats (Reps) y Guardado de Peso
            ft.Row([
                ft.Column([ft.Text(f"Reps: {ex.reps}", size=11, color="white54"), lbl_sugerencia], expand=True),
                txt_peso_hoy,
                ft.IconButton(ft.icons.SAVE, icon_color="#4CAF50", on_click=internal_guardar_peso)
            ])
        ], spacing=10),
        padding=12, bgcolor="#1E1E1E", border_radius=12
    )

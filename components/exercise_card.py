import flet as ft
import threading

def ExerciseCard(ex, is_checked_func, on_check, on_save_peso, on_timer, sugerencia_txt):
    """
    Componente funcional que retorna una tarjeta de ejercicio en Flet.
    """
    lbl_sugerencia = ft.Text(f"Sugerencia: {sugerencia_txt}", size=11, color="#FFD700", weight="bold")
    
    row_series = ft.Row(wrap=True, spacing=5)
    
    def create_on_change(ex_id, idx, t):
        def handler(e):
            on_check(ex_id, idx, e.control.value, t)
            e.control.update()
        return handler

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

    return ft.Container(
        content=ft.Row([
            # Imagen de Referencia (Lado Izquierdo)
            ft.Container(
                content=ft.Image(
                    src=ex.imagen_url,
                    width=100,
                    height=100,
                    fit=ft.ImageFit.COVER,
                    border_radius=10,
                ),
                border_radius=10,
                bgcolor="white10"
            ),
            # Información y Controles (Lado Derecho)
            ft.Column([
                ft.Row([
                    ft.Text(ex.nombre, weight="bold", size=14, expand=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.IconButton(ft.icons.TIMER, icon_color="#FFD700", on_click=lambda _: on_timer(ex.descanso), icon_size=18)
                ], spacing=0),
                row_series,
                ft.Row([
                    ft.Column([ft.Text(f"Reps: {ex.reps}", size=11, color="white54"), lbl_sugerencia], expand=True, spacing=2),
                    txt_peso_hoy,
                    ft.IconButton(ft.icons.SAVE, icon_color="#4CAF50", on_click=internal_guardar_peso, icon_size=20)
                ], alignment="spaceBetween")
            ], spacing=5, expand=True)
        ], alignment="start", vertical_alignment="center", spacing=15),
        padding=12, bgcolor="#1E1E1E", border_radius=12
    )

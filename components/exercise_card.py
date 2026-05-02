import flet as ft
import threading

def ExerciseCard(ex, is_checked_func, on_check, on_save_peso, on_timer, sugerencia_txt):
    """
    Componente funcional que retorna una tarjeta de ejercicio en Flet.
    """
    lbl_sugerencia = ft.Text(f"Sugerencia: {sugerencia_txt}", size=11, color="#FFD700", weight="bold")
    
    row_series = ft.Row(wrap=True, spacing=5)
    for s_idx in range(ex.series):
        is_checked = is_checked_func(ex.id, s_idx)
        cb = ft.Checkbox(
            label=f"S{s_idx+1}", 
            value=is_checked,
            fill_color="#FFD700",
            on_change=lambda e, ex_id=ex.id, idx=s_idx, t=ex.descanso: on_check(ex_id, idx, e.control.value, t)
        )
        row_series.controls.append(cb)

    txt_peso_hoy = ft.TextField(label="Kg", width=70, height=35, text_size=12, border_color="#FFD700")

    def internal_guardar_peso(e):
        on_save_peso(e, ex.nombre, txt_peso_hoy, lbl_sugerencia)

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(ex.nombre, weight="bold", size=15, expand=True),
                ft.Button(icon="timer", icon_color="#FFD700", on_click=lambda _: on_timer(ex.descanso))
            ]),
            row_series,
            ft.Row([
                ft.Column([ft.Text(f"Reps: {ex.reps}", size=11, color="white54"), lbl_sugerencia], expand=True),
                txt_peso_hoy,
                ft.Button(icon="save", icon_color="#4CAF50", on_click=internal_guardar_peso)
            ])
        ], spacing=8),
        padding=12, bgcolor="#1E1E1E", border_radius=12
    )

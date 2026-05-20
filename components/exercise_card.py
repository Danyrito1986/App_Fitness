import flet as ft
import threading

def ExerciseCard(ex, is_checked_func, on_check, on_save_peso, on_timer, sugerencia_txt):
    """
    Componente ExerciseCard REDISEÑADO (Estilo Pro).
    Tarjetas con Glassmorphism, mejores checkboxes y feedback visual.
    """
    lbl_sugerencia = ft.Text(f"SIGUIENTE: {sugerencia_txt}", size=10, weight="bold", color="#FFD700")
    
    # Fila de series con diseño de "Chips"
    row_series = ft.Row(wrap=True, spacing=8, alignment="center")
    
    def on_checkbox_click(e, idx):
        # Efecto visual al marcar
        e.control.scale = 1.2
        e.control.update()
        threading.Timer(0.2, lambda: setattr(e.control, "scale", 1.0) or e.control.update()).start()
        
        on_check(ex.id, idx, e.control.value, ex.descanso)

    for s_idx in range(ex.series):
        is_checked = is_checked_func(ex.id, s_idx)
        cb = ft.Checkbox(
            label=f"{s_idx+1}", 
            value=is_checked,
            fill_color="#FFD700",
            check_color="black",
            on_change=lambda e, idx=s_idx: on_checkbox_click(e, idx),
            scale=1.1
        )
        row_series.controls.append(cb)

    txt_peso_hoy = ft.TextField(
        label="Peso", 
        width=80, 
        height=45, 
        text_size=14, 
        border_color="white24",
        suffix_text="kg",
        content_padding=10
    )

    def internal_guardar_peso(e):
        on_save_peso(e, ex.nombre, txt_peso_hoy, lbl_sugerencia)

    return ft.Container(
        content=ft.Column([
            # Cabecera: Nombre y Timer
            ft.Row([
                ft.Column([
                    ft.Text(ex.nombre.upper(), weight="bold", size=16, color="white", overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                    ft.Text(f"{ex.series} Series • {ex.reps} Reps", size=12, color="white54"),
                ], expand=True),
                ft.Container(
                    content=ft.IconButton(ft.icons.TIMER_OUTLINED, icon_color="#FFD700", icon_size=20, on_click=lambda _: on_timer(ex.descanso)),
                    bgcolor="white10", border_radius=10
                )
            ]),
            
            # Imagen con efecto de profundidad
            ft.Container(
                content=ft.Image(
                    src=ex.imagen_url,
                    width=220,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
                alignment=ft.alignment.center,
                bgcolor="black26",
                border_radius=20,
                padding=10,
                border=ft.border.all(1, "white10")
            ),
            
            # Control de Series
            ft.Container(
                content=ft.Column([
                    ft.Text("MARCAR SERIES COMPLETADAS", size=10, weight="bold", color="white38", text_align="center"),
                    row_series,
                ], horizontal_alignment="center", spacing=5),
                padding=10,
                bgcolor="white05",
                border_radius=15
            ),
            
            # Registro de Peso
            ft.Row([
                ft.Column([lbl_sugerencia], expand=True),
                txt_peso_hoy,
                ft.Container(
                    content=ft.IconButton(ft.icons.SAVE_ROUNDED, icon_color="white", on_click=internal_guardar_peso),
                    bgcolor="#4CAF50", border_radius=10, width=45, height=45
                )
            ], alignment="center")
        ], spacing=15),
        padding=20,
        bgcolor="#1E1E1E",
        border_radius=25,
        border=ft.border.all(1, "white10"),
        margin=ft.margin.only(bottom=10)
    )

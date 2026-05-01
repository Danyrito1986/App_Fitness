import flet as ft

class StatusHeader(ft.Column):
    def __init__(self, user):
        self.user = user
        self.progreso_barra = ft.ProgressBar(value=user.entrenos_mes/20, width=300, color="#FFD700", bgcolor="#333333")
        self.lbl_progreso = ft.Text(f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos", size=12, color="white54")
        self.lbl_rutina_actual = ft.Text("", size=14, weight="bold", color="#FFD700")
        
        super().__init__(
            controls=[
                ft.Column([self.lbl_progreso, self.progreso_barra], horizontal_alignment="center"),
                self.lbl_rutina_actual
            ],
            horizontal_alignment="center",
            spacing=10
        )

    def update_rutina(self, mes, dia):
        self.lbl_rutina_actual.value = f"RUTINA ACTUAL: MES {mes} - DIA {dia}"
        if self.page:
            self.update()

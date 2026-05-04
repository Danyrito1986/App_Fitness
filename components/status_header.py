import flet as ft

class StatusHeader(ft.Column):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.progreso_barra = ft.ProgressBar(value=user.entrenos_mes/20, width=300, color="#FFD700", bgcolor="#333333")
        self.lbl_progreso = ft.Text(f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos", size=12, color="white54")
        self.lbl_rutina_actual = ft.Text("", size=14, weight="bold", color="#FFD700")

        # Configuración de Column
        self.controls = [
            ft.Column([self.lbl_progreso, self.progreso_barra], horizontal_alignment="center"),
            self.lbl_rutina_actual
        ]
        self.horizontal_alignment = "center"
        self.spacing = 10

    def update_progreso(self, mes, total):
        self.lbl_progreso.value = f"Progreso Mes {mes}: {total}/20 entrenos"
        self.progreso_barra.value = total / 20
        if self.page:
            try: self.update()
            except: pass

    def update_rutina(self, mes, semana, dia):
        musculos_map = {
            1: "EMPUJE SUPERIOR ⚡",
            2: "JALÓN SUPERIOR ⚓",
            3: "EMPUJE INFERIOR 🦵",
            4: "JALÓN INFERIOR 🍑",
            5: "CORE 🛡️"
        }
        patron = musculos_map.get(dia, "DESCONOCIDO")
        self.lbl_rutina_actual.value = f"MES {mes} - SEM {semana} - DÍA {dia}\n{patron}"
        if self.page:
            try: self.update()
            except: pass

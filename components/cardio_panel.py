import flet as ft

class CardioPanel(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.lbl_msg = ft.Text("", size=11, color="white70", italic=True)
        self.main_container = ft.Container(
            content=ft.Column([
                ft.Text("SUGERENCIA DE CARDIO", size=12, weight="bold", color="#2196F3"),
                self.lbl_msg
            ], spacing=2),
            padding=10, bgcolor="#1A237E", border_radius=8, visible=False
        )

    def build(self):
        return self.main_container

    def actualizar_cardio(self, objetivo):
        msg = ""
        if objetivo == "Aumento de masa muscular":
            msg = "10-15 min baja intensidad (Caminata) - AL FINAL. Para salud cardíaca sin quemar músculo."
        elif objetivo == "Definición / Quema de Grasa":
            msg = "25-35 min intensidad moderada (LISS) - AL FINAL. Maximiza oxidación de grasas."
        else:
            msg = "20 min HIIT o intervalos - AL FINAL. Mejora resistencia."
        
        self.lbl_msg.value = msg
        self.main_container.visible = True
        if self.page:
            self.update()

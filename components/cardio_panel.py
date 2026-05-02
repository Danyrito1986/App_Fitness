import flet as ft

class CardioPanel(ft.Container):
    def __init__(self):
        super().__init__()
        self.lbl_msg = ft.Text("", size=11, color="white70", italic=True)
        
        # Configuración del Container
        self.content = ft.Column([
            ft.Text("SUGERENCIA DE CARDIO", size=12, weight="bold", color="#2196F3"),
            self.lbl_msg
        ], spacing=2)
        
        self.padding = 10
        self.bgcolor = "#1A237E"
        self.border_radius = 8
        self.visible = False

    def actualizar_cardio(self, objetivo):
        if objetivo == "Definición / Quema de Grasa":
            self.lbl_msg.value = "Hoy: 30 min caminata inclinada o elíptica (Zona 2)"
            self.visible = True
        elif objetivo == "Aumento de masa muscular":
            self.lbl_msg.value = "Hoy: 10 min caminata ligera (calentamiento/salud)"
            self.visible = True
        else:
            self.visible = False
        
        if self.page:
            try:
                self.update()
            except:
                pass

import flet as ft

class MetricSummary(ft.Container):
    def __init__(self, max_width):
        super().__init__()
        self.max_width_val = max_width
        self.lbl_tdee = ft.Text("Mantenimiento: -- kcal", size=14, color="white54")
        self.lbl_ajuste = ft.Text("Ajuste: -- kcal", size=14, weight="bold")
        self.lbl_cal_final = ft.Text("META DIARIA: -- kcal", size=20, weight="bold", color="#FFD700")
        self.lbl_bf = ft.Text("% Grasa: --", size=16, color="white70")
        self.lbl_masa_magra = ft.Text("Masa Magra: -- kg", size=14, color="white38")

        self.content = ft.Column([
            ft.Row([self.lbl_tdee, self.lbl_ajuste], alignment="center", spacing=20),
            ft.Divider(height=1, color="white10"),
            self.lbl_cal_final,
            ft.Row([self.lbl_bf, self.lbl_masa_magra], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=10)
        
        self.padding = 15
        self.bgcolor = "#1E1E1E"
        self.border_radius = 15
        self.width = max_width
        self.border = ft.border.all(1, "white10")

    def actualizar(self, res):
        self.lbl_tdee.value = f"TDEE: {res['tdee']} kcal"
        self.lbl_ajuste.value = f"{'Extra' if res['ajuste'] > 0 else 'Déficit'}: {res['ajuste']} kcal"
        self.lbl_ajuste.color = "#4CAF50" if res['ajuste'] >= 0 else "#FF5252"
        self.lbl_cal_final.value = f"META: {res['cal']} kcal"
        self.lbl_bf.value = f"Grasa: {res['bf']}%"
        self.lbl_masa_magra.value = f"Músculo: {res['masa_magra']} kg"
        if self.page:
            try:
                self.update()
            except:
                pass

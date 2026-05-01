import flet as ft
import time
import threading

class TimerOverlay(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.txt_timer = ft.Text("60", size=40, weight="bold", color="black")
        self.pb_timer = ft.ProgressBar(value=1.0, width=150, color="black", bgcolor="white30")
        
        self.main_container = ft.Container(
            content=ft.Column([
                ft.Text("DESCANSO", size=16, weight="bold", color="black"),
                self.txt_timer,
                self.pb_timer
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#FFD700", padding=20, border_radius=20, 
            width=200, height=180, alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=20, color="black"),
            visible=False, animate_opacity=300, opacity=0
        )

    def build(self):
        return self.main_container

    def iniciar_descanso(self, segundos, page: ft.Page):
        self.main_container.visible = True
        self.main_container.opacity = 1
        page.update()
        
        for i in range(segundos, -1, -1):
            if not self.main_container.visible: break
            self.txt_timer.value = str(i)
            self.pb_timer.value = i / segundos
            page.update()
            time.sleep(1)
        
        if self.main_container.visible:
            self.txt_timer.value = "¡LISTO!"
            page.update()
            time.sleep(1)
            self.main_container.opacity = 0
            page.update()
            time.sleep(0.3)
            self.main_container.visible = False
            page.update()

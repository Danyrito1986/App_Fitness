import flet as ft
import time
import threading
import uuid

class TimerOverlay(ft.Container):
    def __init__(self):
        super().__init__()
        self.current_timer_id = None
        self.txt_timer = ft.Text("60", size=40, weight="bold", color="black")
        self.pb_timer = ft.ProgressBar(value=1.0, width=150, color="black", bgcolor="white30")
        
        # Botón de cierre para permitir al usuario cancelar el descanso
        self.btn_close = ft.IconButton(
            icon=ft.icons.CLOSE,
            icon_color="black",
            icon_size=20,
            on_click=self.cerrar_timer
        )

        self.timer_box = ft.Container(
            content=ft.Stack([
                ft.Column([
                    ft.Text("DESCANSO", size=16, weight="bold", color="black"),
                    self.txt_timer,
                    self.pb_timer
                ], horizontal_alignment="center", spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(content=self.btn_close, alignment=ft.alignment.top_right, padding=ft.padding.only(right=-10, top=-10))
            ]),
            bgcolor="#FFD700", padding=20, border_radius=20, 
            width=220, height=180, alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=20, color="black")
        )
        
        # Configuración del Container principal (anteriormente main_wrapper)
        self.content = self.timer_box
        self.alignment = ft.alignment.center
        self.expand = True
        self.visible = False
        self.animate_opacity = 300
        self.opacity = 0
        self.bgcolor = "#44000000"

    def cerrar_timer(self, e=None):
        """Detiene el cronómetro actual y oculta el componente."""
        self.current_timer_id = None 
        self.opacity = 0
        self.visible = False
        try:
            self.update()
        except:
            pass

    def iniciar_descanso(self, segundos, page: ft.Page):
        """Inicia un nuevo ciclo de descanso, cancelando cualquier hilo anterior."""
        # Generar un ID único para esta tarea
        my_id = str(uuid.uuid4())
        self.current_timer_id = my_id
        
        # Validación de seguridad para el tiempo
        try:
            segundos = int(segundos)
        except:
            segundos = 60
            
        if segundos <= 0:
            return

        # Mostrar el componente
        self.visible = True
        self.opacity = 1
        self.txt_timer.value = str(segundos)
        self.pb_timer.value = 1.0
        
        try:
            self.update()
        except:
            pass
        
        # Bucle del cronómetro
        for i in range(segundos, -1, -1):
            # Verificación de ID: Si cambió, este hilo debe morir (fue reemplazado o cerrado)
            if self.current_timer_id != my_id: 
                return
            
            self.txt_timer.value = str(i)
            # Protección contra división por cero
            self.pb_timer.value = i / segundos if segundos > 0 else 0
            
            try:
                self.update()
            except:
                break
                
            time.sleep(1)
        
        # Finalización exitosa
        if self.current_timer_id == my_id:
            self.txt_timer.value = "¡LISTO!"
            try:
                self.update()
            except: pass
            
            time.sleep(1.2)
            
            if self.current_timer_id == my_id:
                self.cerrar_timer()

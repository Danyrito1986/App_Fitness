import flet as ft
import db_manager as db
import threading
from models import User
from supabase import Client
from services.calculator import calculate_macros
from components.metric_summary import MetricSummary

def profile_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de perfil avanzada con cálculos de grasa y masa muscular responsiva."""
    
    # --- CONFIGURACIÓN DE ANCHO RESPONSIVO ---
    # Eliminamos el ancho fijo estricto para mejor adaptabilidad en móviles
    MAX_WIDTH = 400

    # --- COMPONENTES ---
    metric_summary = MetricSummary(MAX_WIDTH)
    debounce_timer = None

    # --- CAMPOS DE ENTRADA ---
    txt_nombre = ft.TextField(label="Nombre", value=user.nombre, max_length=50, border_color="#FFD700", width=MAX_WIDTH)
    txt_edad = ft.TextField(label="Edad", value=str(user.edad), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo_debouced())
    txt_peso = ft.TextField(label="Peso (kg)", value=str(user.peso_actual), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo_debouced())
    txt_altura = ft.TextField(label="Altura (cm)", value=str(user.altura), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo_debouced())
    
    dd_genero = ft.Dropdown(
        label="Género",
        value=user.genero,
        options=[ft.dropdown.Option("Hombre"), ft.dropdown.Option("Mujer")],
        border_color="#FFD700", width=MAX_WIDTH,
        on_change=lambda _: actualizar_ui()
    )

    dd_nivel = ft.Dropdown(
        label="Nivel de Experiencia",
        value=user.nivel,
        options=[
            ft.dropdown.Option("Novato"),
            ft.dropdown.Option("Intermedio"),
            ft.dropdown.Option("Pro")
        ],
        border_color="#FFD700", width=MAX_WIDTH,
        on_change=lambda _: calcular_en_vivo_debouced()
    )

    dd_objetivo = ft.Dropdown(
        label="Objetivo Fitness",
        value=user.objetivo,
        options=[
            ft.dropdown.Option("Aumento de masa muscular"),
            ft.dropdown.Option("Definición / Quema de Grasa"),
            ft.dropdown.Option("Resistencia"),
        ],
        border_color="#FFD700", width=MAX_WIDTH,
        on_change=lambda _: calcular_en_vivo_debouced()
    )
    
    # Medidas para Grasa Corporal
    txt_cuello = ft.TextField(label="Cuello (cm)", value=str(user.cuello), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo_debouced())
    txt_cintura = ft.TextField(label="Cintura (cm)", value=str(user.cintura), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo_debouced())
    txt_cadera = ft.TextField(label="Cadera (cm)", value=str(user.cadera), width=120, border_color="#FFD700", visible=(user.genero == "Mujer"), on_change=lambda _: calcular_en_vivo_debouced())

    # Medidas Adicionales de Control
    txt_bicep = ft.TextField(label="Bíceps", value=str(user.bicep), width=90, border_color="#2196F3")
    txt_pecho = ft.TextField(label="Pecho", value=str(user.pecho), width=90, border_color="#2196F3")
    txt_gluteo = ft.TextField(label="Glúteo", value=str(user.gluteo), width=90, border_color="#2196F3")
    txt_muslo = ft.TextField(label="Muslo", value=str(user.muslo), width=90, border_color="#2196F3")

    def safe_float(value, default):
        try:
            return float(value) if value and str(value).strip() else default
        except ValueError:
            return default

    def calcular_en_vivo_debouced():
        nonlocal debounce_timer
        if debounce_timer:
            debounce_timer.cancel()
        debounce_timer = threading.Timer(0.5, calcular_en_vivo)
        debounce_timer.start()

    def calcular_en_vivo(init=False):
        try:
            # Validar campos numéricos con feedback visual
            invalid = False
            campos_num = [txt_edad, txt_peso, txt_altura, txt_cuello, txt_cintura]
            if dd_genero.value == "Mujer":
                campos_num.append(txt_cadera)
                
            for c in campos_num:
                try:
                    float(c.value)
                    c.border_color = "#FFD700"
                except:
                    c.border_color = "red700"
                    invalid = True

            if invalid:
                if not init: page.update()
                return

            val_genero = dd_genero.value
            val_altura = safe_float(txt_altura.value, user.altura)
            val_peso = safe_float(txt_peso.value, user.peso_actual)
            val_cuello = safe_float(txt_cuello.value, user.cuello)
            val_cintura = safe_float(txt_cintura.value, user.cintura)
            val_cadera = safe_float(txt_cadera.value, user.cadera)
            val_objetivo = dd_objetivo.value
            val_nivel = dd_nivel.value
            val_edad = int(safe_float(txt_edad.value, user.edad))

            temp_user = User(
                id=user.id, nombre=user.nombre, objetivo=val_objetivo, nivel=val_nivel,
                peso_actual=val_peso, genero=val_genero, altura=val_altura,
                cuello=val_cuello, cintura=val_cintura, cadera=val_cadera, edad=val_edad
            )
            
            res = calculate_macros(temp_user)
            metric_summary.actualizar(res)
        except Exception as e:
            print(f"Error en calculo en vivo: {e}")
        
        if not init: page.update()

    def actualizar_ui():
        txt_cadera.visible = (dd_genero.value == "Mujer")
        calcular_en_vivo()

    def guardar_perfil(e):
        try:
            # Validar antes de guardar
            try:
                data_to_save = {
                    'nombre': txt_nombre.value, 'objetivo': dd_objetivo.value,
                    'nivel': dd_nivel.value, 'peso': float(txt_peso.value),
                    'genero': dd_genero.value, 'altura': float(txt_altura.value),
                    'cuello': float(txt_cuello.value), 'cintura': float(txt_cintura.value),
                    'cadera': float(txt_cadera.value), 'pecho': float(txt_pecho.value),
                    'gluteo': float(txt_gluteo.value), 'bicep': float(txt_bicep.value),
                    'muslo': float(txt_muslo.value), 'edad': int(txt_edad.value)
                }
            except:
                show_snackbar("Por favor corrige los campos en rojo", True)
                return

            success = db.update_user_profile(client, user.id, data_to_save)
            if success:
                # Actualizar objeto user local (referencia compartida)
                user.nombre, user.objetivo, user.nivel = txt_nombre.value, dd_objetivo.value, dd_nivel.value
                user.peso_actual, user.genero, user.altura = float(txt_peso.value), dd_genero.value, float(txt_altura.value)
                user.cuello, user.cintura, user.cadera = float(txt_cuello.value), float(txt_cintura.value), float(txt_cadera.value)
                user.pecho, user.gluteo, user.bicep, user.muslo, user.edad = float(txt_pecho.value), float(txt_gluteo.value), float(txt_bicep.value), float(txt_muslo.value), int(txt_edad.value)
                
                db.log_weight(client, user.id, user.peso_actual)
                show_snackbar("¡Perfil guardado y sincronizado! ✨", False)
                calcular_en_vivo()
            else:
                show_snackbar("Error al guardar en la nube.", True)
        except Exception as ex:
            show_snackbar(f"Error crítico: {ex}", True)

    calcular_en_vivo(init=True)

    return ft.Column([
        ft.Container(height=10),
        ft.Text("MI PERFIL FITNESS", size=24, weight="bold", color="#FFD700"),
        
        # --- SECCIÓN 1: DATOS PERSONALES ---
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON_OUTLINE, color="#FFD700"),
                        title=ft.Text("DATOS PERSONALES", weight="bold"),
                        subtitle=ft.Text("Identidad y experiencia", size=12, color="white54")
                    ),
                    ft.Container(
                        content=ft.Column([
                            txt_nombre,
                            ft.Row([txt_edad, dd_genero], spacing=10, expand=True),
                            dd_nivel,
                            dd_objetivo,
                        ], spacing=10),
                        padding=ft.padding.only(left=15, right=15, bottom=20)
                    )
                ]),
                bgcolor="#1E1E1E", border_radius=12
            ),
            width=MAX_WIDTH
        ),

        # --- SECCIÓN 2: COMPOSICIÓN CORPORAL ---
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.FITNESS_CENTER, color="#FFD700"),
                        title=ft.Text("COMPOSICIÓN CORPORAL", weight="bold"),
                        subtitle=ft.Text("Base para cálculo de macros", size=12, color="white54")
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([txt_peso, txt_altura], spacing=10, alignment="center"),
                            ft.Row([txt_cuello, txt_cintura, txt_cadera], spacing=10, alignment="center", wrap=True),
                        ], spacing=10),
                        padding=ft.padding.only(left=15, right=15, bottom=20)
                    )
                ]),
                bgcolor="#1E1E1E", border_radius=12
            ),
            width=MAX_WIDTH
        ),

        # --- SECCIÓN 3: SEGUIMIENTO MUSCULAR (COLAPSABLE) ---
        ft.ExpansionTile(
            title=ft.Text("CONTROL DE VOLUMEN (CM)", weight="bold", size=14, color="#2196F3"),
            leading=ft.Icon(ft.icons.SQUARE_FOOT, color="#2196F3"),
            bgcolor="transparent",
            collapsed_bgcolor="transparent",
            controls=[
                ft.Container(
                    content=ft.Row([txt_bicep, txt_pecho, txt_gluteo, txt_muslo], alignment="center", wrap=True, spacing=10),
                    padding=20, bgcolor="#1A1A1A", border_radius=12
                )
            ]
        ),
        
        # --- RESUMEN DE MÉTRICAS (AUTOMÁTICO) ---
        metric_summary,
        
        ft.Container(height=10),
        
        ft.ElevatedButton(
            "GUARDAR CAMBIOS", 
            icon=ft.icons.SAVE, 
            on_click=guardar_perfil,
            style=ft.ButtonStyle(color="black", bgcolor="#FFD700", shape=ft.RoundedRectangleBorder(radius=8)),
            width=MAX_WIDTH, height=55
        ),
        ft.Container(height=30)
    ], expand=True, horizontal_alignment="center", scroll="adaptive")

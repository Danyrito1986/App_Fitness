import flet as ft
import db_manager as db
from models import User
from supabase import Client
from services.calculator import calculate_macros
from components.metric_summary import MetricSummary

def profile_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de perfil avanzada con cálculos de grasa y masa muscular responsiva."""
    
    # --- CONFIGURACIÓN DE ANCHO RESPONSIVO ---
    MAX_WIDTH = 400

    # --- COMPONENTES ---
    metric_summary = MetricSummary(MAX_WIDTH)

    # --- CAMPOS DE ENTRADA ---
    txt_nombre = ft.TextField(label="Nombre", value=user.nombre, max_length=50, border_color="#FFD700", width=MAX_WIDTH)
    txt_edad = ft.TextField(label="Edad", value=str(user.edad), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_peso = ft.TextField(label="Peso (kg)", value=str(user.peso_actual), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_altura = ft.TextField(label="Altura (cm)", value=str(user.altura), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    
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
        on_change=lambda _: calcular_en_vivo()
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
        on_change=lambda _: calcular_en_vivo()
    )
    
    # Medidas para Grasa Corporal
    txt_cuello = ft.TextField(label="Cuello (cm)", value=str(user.cuello), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_cintura = ft.TextField(label="Cintura (cm)", value=str(user.cintura), width=120, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_cadera = ft.TextField(label="Cadera (cm)", value=str(user.cadera), width=120, border_color="#FFD700", visible=(user.genero == "Mujer"), on_change=lambda _: calcular_en_vivo())

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

    def calcular_en_vivo(init=False):
        try:
            campos_num = [txt_edad, txt_peso, txt_altura, txt_cuello, txt_cintura]
            for c in campos_num:
                try:
                    float(c.value)
                    c.border_color = "#FFD700"
                except:
                    c.border_color = "red700" if c.value else "#FFD700"

            val_genero = dd_genero.value
            val_altura = safe_float(txt_altura.value, user.altura)
            val_peso = safe_float(txt_peso.value, user.peso_actual)
            val_cuello = safe_float(txt_cuello.value, user.cuello)
            val_cintura = safe_float(txt_cintura.value, user.cintura)
            val_cadera = safe_float(txt_cadera.value, user.cadera)
            val_objetivo = dd_objetivo.value
            val_edad = int(safe_float(txt_edad.value, user.edad))

            temp_user = User(
                id=user.id, nombre=user.nombre, objetivo=val_objetivo,
                peso_actual=val_peso, genero=val_genero, altura=val_altura,
                cuello=val_cuello, cintura=val_cintura, cadera=val_cadera, edad=val_edad
            )
            
            res = calculate_macros(temp_user)
            metric_summary.actualizar(res)
        except Exception as e:
            print(f"Error: {e}")
        
        if not init: page.update()

    def actualizar_ui():
        txt_cadera.visible = (dd_genero.value == "Mujer")
        calcular_en_vivo()

    def guardar_perfil(e):
        try:
            success = db.update_user_profile(client, user.id, {
                'nombre': txt_nombre.value, 'objetivo': dd_objetivo.value,
                'nivel': dd_nivel.value, 'peso': float(txt_peso.value),
                'genero': dd_genero.value, 'altura': float(txt_altura.value),
                'cuello': float(txt_cuello.value), 'cintura': float(txt_cintura.value),
                'cadera': float(txt_cadera.value), 'pecho': float(txt_pecho.value),
                'gluteo': float(txt_gluteo.value), 'bicep': float(txt_bicep.value),
                'muslo': float(txt_muslo.value), 'edad': int(txt_edad.value)
            })
            if success:
                user.nombre, user.objetivo, user.nivel = txt_nombre.value, dd_objetivo.value, dd_nivel.value
                user.peso_actual, user.genero, user.altura = float(txt_peso.value), dd_genero.value, float(txt_altura.value)
                user.cuello, user.cintura, user.cadera = float(txt_cuello.value), float(txt_cintura.value), float(txt_cadera.value)
                user.pecho, user.gluteo, user.bicep, user.muslo, user.edad = float(txt_pecho.value), float(txt_gluteo.value), float(txt_bicep.value), float(txt_muslo.value), int(txt_edad.value)
                
                db.log_weight(client, user.id, user.peso_actual)
                show_snackbar("¡Perfil guardado! ✨", False)
                calcular_en_vivo()
            else:
                show_snackbar("Error al guardar.", True)
        except Exception as ex:
            show_snackbar(f"Error: {ex}", True)

    calcular_en_vivo(init=True)

    return ft.Column([
        ft.Container(height=10),
        ft.Text("MI PERFIL FITNESS", size=24, weight="bold", color="#FFD700"),
        
        ft.Column([
            txt_nombre, dd_genero, dd_nivel, dd_objetivo,
            ft.Row([txt_edad, txt_peso, txt_altura], alignment="center", wrap=True),
        ], horizontal_alignment="center", spacing=10),
        
        ft.Divider(height=20, color="white12"),
        ft.Text("MEDIDAS DE GRASA", size=14, weight="bold"),
        ft.Row([txt_cuello, txt_cintura, txt_cadera], alignment="center", wrap=True),
        
        ft.Divider(height=20, color="white12"),
        ft.Text("CONTROL VOLUMEN", size=14, weight="bold", color="#2196F3"),
        ft.Row([txt_bicep, txt_pecho, txt_gluteo, txt_muslo], alignment="center", wrap=True),
        
        metric_summary,
        
        ft.ElevatedButton(
            "GUARDAR CAMBIOS", 
            icon=ft.icons.SAVE, 
            on_click=guardar_perfil,
            style=ft.ButtonStyle(color="black", bgcolor="#FFD700"),
            width=MAX_WIDTH, height=50
        ),
        ft.Container(height=20)
    ], expand=True, horizontal_alignment="center", scroll="adaptive")

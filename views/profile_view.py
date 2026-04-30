import flet as ft
import db_manager as db
from models import User

from supabase import Client

def profile_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de perfil avanzada con cálculos de grasa y masa muscular."""
    
    # --- CAMPOS DE ENTRADA ---
    txt_nombre = ft.TextField(label="Nombre", value=user.nombre, width=350, border_color="#FFD700")
    txt_edad = ft.TextField(label="Edad", value=str(user.edad), width=110, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_peso = ft.TextField(label="Peso (kg)", value=str(user.peso_actual), width=110, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_altura = ft.TextField(label="Altura (cm)", value=str(user.altura), width=110, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    
    dd_genero = ft.Dropdown(
        label="Género",
        value=user.genero,
        options=[ft.dropdown.Option("Hombre"), ft.dropdown.Option("Mujer")],
        width=350, border_color="#FFD700",
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
        width=350, border_color="#FFD700",
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
        width=350, border_color="#FFD700",
        on_change=lambda _: calcular_en_vivo()
    )
    
    # Medidas para Grasa Corporal
    txt_cuello = ft.TextField(label="Cuello (cm)", value=str(user.cuello), width=110, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_cintura = ft.TextField(label="Cintura (cm)", value=str(user.cintura), width=110, border_color="#FFD700", on_change=lambda _: calcular_en_vivo())
    txt_cadera = ft.TextField(label="Cadera (cm)", value=str(user.cadera), width=110, border_color="#FFD700", visible=(user.genero == "Mujer"), on_change=lambda _: calcular_en_vivo())

    # Medidas Adicionales de Control
    txt_bicep = ft.TextField(label="Bíceps (cm)", value=str(user.bicep), width=110, border_color="#2196F3")
    txt_pecho = ft.TextField(label="Pecho (cm)", value=str(user.pecho), width=110, border_color="#2196F3")
    txt_gluteo = ft.TextField(label="Glúteo (cm)", value=str(user.gluteo), width=110, border_color="#2196F3")
    txt_muslo = ft.TextField(label="Muslo (cm)", value=str(user.muslo), width=110, border_color="#2196F3")

    # --- PANEL DE RESULTADOS ---
    lbl_tdee = ft.Text("Mantenimiento: -- kcal", size=14, color="white54")
    lbl_ajuste = ft.Text("Ajuste: -- kcal", size=14, weight="bold")
    lbl_cal_final = ft.Text("META DIARIA: -- kcal", size=20, weight="bold", color="#FFD700")
    lbl_bf = ft.Text("% Grasa: --", size=16, color="white70")
    lbl_masa_magra = ft.Text("Masa Magra: -- kg", size=14, color="white38")

    def safe_float(value, default):
        """Convierte a float de forma segura para evitar errores en tiempo real."""
        try:
            return float(value) if value and str(value).strip() else default
        except ValueError:
            return default

    def calcular_en_vivo(init=False):
        try:
            # Validaciones de color sutiles para indicar campos requeridos/erróneos
            campos_num = [txt_edad, txt_peso, txt_altura, txt_cuello, txt_cintura]
            for c in campos_num:
                try:
                    float(c.value)
                    c.border_color = "#FFD700"
                except:
                    c.border_color = "red700" if c.value else "#FFD700"

            # Obtenemos valores de los campos (sin mutar el objeto 'user' real todavía)
            val_genero = dd_genero.value
            val_altura = safe_float(txt_altura.value, user.altura or 170.0)
            val_peso = safe_float(txt_peso.value, user.peso_actual or 70.0)
            val_cuello = safe_float(txt_cuello.value, user.cuello or 40.0)
            val_cintura = safe_float(txt_cintura.value, user.cintura or 85.0)
            val_cadera = safe_float(txt_cadera.value, user.cadera or 90.0)
            val_objetivo = dd_objetivo.value
            val_edad = int(safe_float(txt_edad.value, user.edad or 25))

            # Creamos un usuario temporal para el cálculo de macros
            temp_user = User(
                id=user.id,
                nombre=user.nombre,
                objetivo=val_objetivo,
                peso_actual=val_peso,
                genero=val_genero,
                altura=val_altura,
                cuello=val_cuello,
                cintura=val_cintura,
                cadera=val_cadera,
                edad=val_edad
            )
            
            res = temp_user.get_macros()
            
            lbl_tdee.value = f"Quemado Diario (TDEE): {res['tdee']} kcal"
            
            if res['ajuste'] > 0:
                lbl_ajuste.value = f"Consumir Extra: +{res['ajuste']} kcal"
                lbl_ajuste.color = "#4CAF50" # Verde para superávit
            elif res['ajuste'] < 0:
                lbl_ajuste.value = f"Déficit Sugerido: {res['ajuste']} kcal"
                lbl_ajuste.color = "#FF5252" # Rojo para déficit
            else:
                lbl_ajuste.value = "Mantener Peso: 0 kcal"
                lbl_ajuste.color = "white"

            lbl_cal_final.value = f"META DIARIA: {res['cal']} kcal"
            lbl_bf.value = f"Grasa Corporal: {res['bf']}%"
            lbl_masa_magra.value = f"Masa Muscular: {res['masa_magra']} kg"
        except Exception as e:
            print(f"Error en calculo_en_vivo: {e}")
        
        if not init: page.update()

    def actualizar_ui():
        txt_cadera.visible = (dd_genero.value == "Mujer")
        calcular_en_vivo()

    def guardar_perfil(e):
        try:
            success = db.update_user_profile(client, user.id, {
                'nombre': txt_nombre.value,
                'objetivo': dd_objetivo.value,
                'nivel': dd_nivel.value,
                'peso': float(txt_peso.value),
                'genero': dd_genero.value,
                'altura': float(txt_altura.value),
                'cuello': float(txt_cuello.value),
                'cintura': float(txt_cintura.value),
                'cadera': float(txt_cadera.value),
                'pecho': float(txt_pecho.value),
                'gluteo': float(txt_gluteo.value),
                'bicep': float(txt_bicep.value),
                'muslo': float(txt_muslo.value),
                'edad': int(txt_edad.value)
            })
            if success:
                # Actualizar el objeto user en memoria (ahora sí es oficial)
                user.nombre = txt_nombre.value
                user.objetivo = dd_objetivo.value
                user.nivel = dd_nivel.value
                user.peso_actual = float(txt_peso.value)
                user.genero = dd_genero.value
                user.altura = float(txt_altura.value)
                user.cuello = float(txt_cuello.value)
                user.cintura = float(txt_cintura.value)
                user.cadera = float(txt_cadera.value)
                user.pecho = float(txt_pecho.value)
                user.gluteo = float(txt_gluteo.value)
                user.bicep = float(txt_bicep.value)
                user.muslo = float(txt_muslo.value)
                user.edad = int(txt_edad.value)
                
                db.log_weight(client, user.id, user.peso_actual)
                show_snackbar("¡Perfil y medidas actualizados con éxito! ✨", False)
                calcular_en_vivo()
            else:
                show_snackbar("No se pudo guardar. Verifica tu conexión.", True)
        except Exception as ex:
            show_snackbar(f"Error: {ex}", True)

    calcular_en_vivo(init=True)

    return ft.Column([
        ft.Container(height=10),
        ft.Text("Configuración de Perfil", size=24, weight="bold", color="#FFD700"),
        txt_nombre,
        dd_genero,
        dd_nivel,
        dd_objetivo,
        ft.Row([txt_edad, txt_peso, txt_altura], alignment="center", spacing=10, wrap=True),
        
        ft.Divider(height=20, color="white12"),
        ft.Text("Medidas para Grasa Corporal (Marina)", size=14, weight="bold"),
        ft.Row([txt_cuello, txt_cintura, txt_cadera], alignment="center", spacing=10, wrap=True),
        
        ft.Divider(height=20, color="white12"),
        ft.Text("Control de Volumen Muscular", size=14, weight="bold", color="#2196F3"),
        ft.Row([txt_bicep, txt_pecho, txt_gluteo, txt_muslo], alignment="center", spacing=10, wrap=True),
        
        ft.Container(
            content=ft.Column([
                lbl_tdee,
                lbl_ajuste,
                ft.Divider(height=10, color="white10"),
                lbl_cal_final,
                ft.Row([lbl_bf, lbl_masa_magra], alignment="center", spacing=20)
            ], horizontal_alignment="center"),
            padding=20, bgcolor="#1E1E1E", border_radius=15, width=350,
            border=ft.border.all(1, "white10")
        ),
        
        ft.Container(height=10),
        ft.ElevatedButton(
            "GUARDAR PERFIL Y MEDIDAS", 
            icon="save", 
            on_click=guardar_perfil,
            style=ft.ButtonStyle(color="black", bgcolor="#FFD700"),
            width=350, height=50
        ),
        ft.Container(height=20)
    ], expand=True, horizontal_alignment="center", scroll="adaptive")

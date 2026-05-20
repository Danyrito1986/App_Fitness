import flet as ft
import db_manager as db
import threading
import copy
from models import User, Exercise
from supabase import Client
from datetime import datetime
from components.timer_overlay import TimerOverlay
from components.exercise_card import ExerciseCard
from components.cardio_panel import CardioPanel
from components.status_header import StatusHeader

def workout_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de entrenamiento avanzada blindada contra fallos de renderizado y concurrencia."""
    
    try:
        # --- COMPONENTES ---
        timer_overlay = TimerOverlay()
        cardio_panel = CardioPanel()
        status_header = StatusHeader(user)
        save_timer = None
        
        # --- INDICADOR DE GUARDADO ASÍNCRONO (PREMIUM FEEDBACK) ---
        sync_icon = ft.Icon(name=ft.icons.CLOUD_DONE, color="#4CAF50", size=14)
        sync_txt = ft.Text("Sincronizado", size=11, color="white54", weight="bold")
        sync_indicator = ft.Container(
            content=ft.Row(
                [sync_icon, sync_txt],
                alignment="center",
                spacing=5
            ),
            padding=ft.padding.only(right=10)
        )
        
        # --- ESTADO Y PERSISTENCIA ---
        mes_seleccionado = user.mes_actual
        semana_seleccionada = (user.entrenos_mes // 5) % 4 + 1
        dia_seleccionado = (user.entrenos_mes % 5) + 1
        nivel_seleccionado = user.nivel
        
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        
        # --- BARRA DE PROGRESO DE ENTRENAMIENTO ---
        progress_bar = ft.ProgressBar(value=0, color="#FFD700", bgcolor="white10", height=4)
        lbl_percent = ft.Text("0%", size=12, color="white54", weight="bold")
        
        def update_overall_progress():
            try:
                total_exs = len(lista_ejercicios.controls)
                if total_exs == 0: return
                
                # Cálculo preciso basado en progreso_local para el día actual
                keys_hoy = [k for k in progreso_local.get("completados", {}).keys() 
                           if k.startswith(f"{mes_seleccionado}_{semana_seleccionada}_{dia_seleccionado}_")]
                
                # Si hay ejercicios cargados, calculamos el % de ejercicios que tienen al menos 1 serie marcada
                unique_ex_ids = set([k.split("_")[-1] for k in keys_hoy])
                percent = len(unique_ex_ids) / total_exs if total_exs > 0 else 0
                progress_bar.value = min(percent, 1.0)
                lbl_percent.value = f"{int(percent * 100)}%"
                page.update()
            except: pass

        # ... (rest of storage logic remains the same)
        try:
            raw_progress = page.client_storage.get("workout_progress")
            progreso_local = raw_progress if isinstance(raw_progress, dict) else {}
        except Exception as e:
            print(f"DEBUG_ERR: Error leyendo client_storage: {e}")
            progreso_local = {}
        
        if not isinstance(progreso_local.get("completados"), dict) or progreso_local.get("fecha") != hoy_str:
            try:
                datos_nube = db.get_workout_progress(client, user.id, hoy_str)
                
                # BLINDAJE: Solo sobrescribir si la respuesta es válida (no None)
                if datos_nube is not None:
                    if isinstance(datos_nube, dict):
                        progreso_local = {"fecha": hoy_str, "completados": datos_nube}
                    else:
                        progreso_local = {"fecha": hoy_str, "completados": {}}
                    
                    # Persistir el nuevo estado válido en local
                    try:
                        page.client_storage.set("workout_progress", progreso_local)
                    except Exception as e:
                        print(f"DEBUG_ERR: Error escribiendo en client_storage (init): {e}")
                else:
                    # Si datos_nube es None, hubo un error de red. 
                    # Mantenemos lo que hay en progreso_local (caché) para no borrar nada.
                    print("DEBUG_ERR: Fallo de red detectado. Manteniendo caché local de seguridad.")
                    if "fecha" not in progreso_local:
                        progreso_local = {"fecha": hoy_str, "completados": {}}
            except Exception as e:
                print(f"DEBUG_ERR: Error crítico recuperando de nube: {e}")
                if "fecha" not in progreso_local:
                    progreso_local = {"fecha": hoy_str, "completados": {}}

        lista_ejercicios = ft.Column(spacing=15, horizontal_alignment="center")

        def debounced_save():
            nonlocal save_timer
            try:
                sync_icon.name = ft.icons.SYNC
                sync_icon.color = "#FFD700"
                sync_txt.value = "Guardando..."
                sync_txt.color = "#FFD700"
                page.update()
            except: pass
            
            if save_timer:
                save_timer.cancel()
            save_timer = threading.Timer(0.1, persistir_nube)
            save_timer.start()

        def persistir_nube():
            try:
                print(f"DEBUG_PRO: Sincronizando progreso con nube...")
                datos_a_guardar = copy.deepcopy(progreso_local["completados"])
                if db.save_workout_progress(client, user.id, hoy_str, datos_a_guardar):
                    print("DEBUG_PRO: Sincronización exitosa ✅")
                    try:
                        sync_icon.name = ft.icons.CLOUD_DONE
                        sync_icon.color = "#4CAF50"
                        sync_txt.value = "Sincronizado"
                        sync_txt.color = "white54"
                        page.update()
                    except: pass
                else:
                    print("DEBUG_PRO: Error en la sincronización de nube ❌")
                    try:
                        sync_icon.name = ft.icons.CLOUD_OFF
                        sync_icon.color = "#F44336"
                        sync_txt.value = "Offline / Sin Nube"
                        sync_txt.color = "#F44336"
                        page.update()
                    except: pass
            except Exception as e:
                print(f"DEBUG_ERR: Error persistiendo en nube: {e}")
                try:
                    sync_icon.name = ft.icons.CLOUD_OFF
                    sync_icon.color = "#F44336"
                    sync_txt.value = "Error Sincro"
                    sync_txt.color = "#F44336"
                    page.update()
                except: pass

        def guardar_progreso_serie(ex_id, serie_idx, valor, t_descanso):
            try:
                key = f"{mes_seleccionado}_{semana_seleccionada}_{dia_seleccionado}_{ex_id}"
                if key not in progreso_local["completados"]:
                    progreso_local["completados"][key] = []
                
                if valor:
                    if serie_idx not in progreso_local["completados"][key]:
                        progreso_local["completados"][key].append(serie_idx)
                    threading.Thread(target=timer_overlay.iniciar_descanso, args=(t_descanso, page), daemon=True).start()
                else:
                    if serie_idx in progreso_local["completados"][key]:
                        progreso_local["completados"][key].remove(serie_idx)
                
                try:
                    page.client_storage.set("workout_progress", progreso_local)
                except Exception as e:
                    print(f"DEBUG_ERR: Error persistencia local: {e}")
                
                debounced_save()
            except Exception as e:
                print(f"Error en guardar_progreso_serie: {e}")

        def obtener_progreso_serie(ex_id, serie_idx):
            try:
                key = f"{mes_seleccionado}_{semana_seleccionada}_{dia_seleccionado}_{ex_id}"
                completados = progreso_local.get("completados", {}).get(key, [])
                return serie_idx in completados
            except:
                return False

        # --- OVERLAY DE RESUMEN FINAL ---
        lbl_resumen_ejercicios = ft.Text("0", size=20, weight="bold")
        lbl_resumen_series = ft.Text("0", size=20, weight="bold")
        lbl_resumen_calorias = ft.Text("~350", size=20, weight="bold")

        summary_overlay = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.EMOJI_EVENTS, color="#FFD700", size=80),
                    ft.Text("¡ENTRENAMIENTO COMPLETADO!", size=22, weight="bold", color="white", text_align="center"),
                    ft.Divider(color="white10"),
                    ft.Row([
                        ft.Column([ft.Text("EJERCICIOS", size=10, color="white54"), lbl_resumen_ejercicios], horizontal_alignment="center"),
                        ft.Column([ft.Text("SERIES", size=10, color="white54"), lbl_resumen_series], horizontal_alignment="center"),
                        ft.Column([ft.Text("CALORÍAS", size=10, color="white54"), lbl_resumen_calorias], horizontal_alignment="center"),
                    ], alignment="spaceAround", width=300),
                    ft.Container(height=10),
                    ft.ElevatedButton("COMPARTIR LOGRO", icon=ft.icons.SHARE, bgcolor="white10"),
                    ft.TextButton("CERRAR", on_click=lambda _: setattr(summary_overlay, "visible", False) or page.update())
                ], horizontal_alignment="center", spacing=20),
                bgcolor="#1E1E1E", padding=30, border_radius=30, border=ft.border.all(1, "white10"),
                width=350, height=450, alignment=ft.alignment.center
            ),
            expand=True, bgcolor="#CC000000", visible=False, alignment=ft.alignment.center
        )

        def mostrar_resumen():
            # Contar datos reales de la sesión
            keys_hoy = [k for k in progreso_local.get("completados", {}).keys() 
                       if k.startswith(f"{mes_seleccionado}_{semana_seleccionada}_{dia_seleccionado}_")]
            
            num_ex = len(set([k.split("_")[-1] for k in keys_hoy]))
            num_series = sum([len(progreso_local["completados"][k]) for k in keys_hoy])
            
            # Actualizar textos del resumen (Seguro y directo)
            lbl_resumen_ejercicios.value = str(num_ex)
            lbl_resumen_series.value = str(num_series)
            
            summary_overlay.visible = True
            page.update()

        def finalizar_entreno(e):
            try:
                rutina_act = f"M{mes_seleccionado}-S{semana_seleccionada}-D{dia_seleccionado}"
                if db.log_workout(client, user.id, rutina_act):
                    # Forzar refresco de datos del usuario
                    new_stats = db.get_workout_stats(client, user.id)
                    user.entrenos_mes = new_stats % 20 
                    user.mes_actual = (new_stats // 20) + 1
                    
                    # Actualizar UI
                    status_header.update_progreso(user.mes_actual, user.entrenos_mes)
                    db.save_workout_progress(client, user.id, hoy_str, progreso_local["completados"])
                    mostrar_resumen()
                else:
                    show_snackbar("Error al guardar en la nube", True)
                page.update()
            except Exception as ex:
                show_snackbar(f"Error al finalizar: {ex}", True)

        def on_timer_click(t):
            threading.Thread(target=timer_overlay.iniciar_descanso, args=(t, page), daemon=True).start()

        def set_mes(n):
            nonlocal mes_seleccionado
            mes_seleccionado = n
            actualizar_ui_meses()
            update_workout_list()

        def set_semana(n):
            nonlocal semana_seleccionada
            semana_seleccionada = n
            actualizar_ui_semanas()
            update_workout_list()

        def update_workout_list(dia=None, init=False):
            nonlocal dia_seleccionado
            if dia: dia_seleccionado = dia
            
            try:
                status_header.update_rutina(mes_seleccionado, semana_seleccionada, dia_seleccionado)
                actualizar_ui_dias()
                cardio_panel.actualizar_cardio(user.objetivo)
                
                exs = db.get_dynamic_exercises(client, user.genero, nivel_seleccionado, mes_seleccionado, dia_seleccionado, user.objetivo, semana_seleccionada)
                lista_ejercicios.controls.clear()
                
                if not exs:
                    lista_ejercicios.controls.append(ft.Container(content=ft.Text("No hay ejercicios para hoy.", color="white54"), padding=20))
                else:
                    for ex in exs:
                        last_w = db.get_last_weight(client, user.id, ex.nombre)
                        sugerencia_txt = f"{last_w + 2.5}kg" if last_w > 0 else "Peso moderado"
                        
                        def on_save_peso(e, nombre_ex, field, lbl):
                            try:
                                peso = float(field.value)
                                if db.log_pr(client, user.id, nombre_ex, peso):
                                    show_snackbar(f"¡{nombre_ex} guardado!", False)
                                    lbl.value = f"Sugerencia: {peso + 2.5}kg"
                                    page.update()
                            except: show_snackbar("Valor inválido", True)

                        card = ExerciseCard(ex, obtener_progreso_serie, guardar_progreso_serie, on_save_peso, on_timer_click, sugerencia_txt)
                        lista_ejercicios.controls.append(card)
                
                # Actualizar barra de progreso al cargar
                update_overall_progress()
            except Exception as e:
                print(f"Error en update_workout_list: {e}")
                lista_ejercicios.controls.append(ft.Text("Error al cargar la rutina.", color="red"))

            if not init: page.update()

        row_meses = ft.Row(scroll="auto", spacing=10)
        def actualizar_ui_meses():
            row_meses.controls = [
                ft.ElevatedButton(
                    f"MES {i}", 
                    on_click=lambda e, n=i: set_mes(n) if n <= user.mes_actual else show_snackbar("Mes bloqueado", True),
                    bgcolor="#FFD700" if i == mes_seleccionado else "#333333",
                    color="black" if i == mes_seleccionado else "white"
                ) for i in range(1, 7)
            ]

        row_semanas = ft.Row(scroll="auto", spacing=10)
        def actualizar_ui_semanas():
            row_semanas.controls = [
                ft.TextButton(
                    f"SEM {i}", 
                    on_click=lambda e, n=i: set_semana(n)
                ) for i in range(1, 5)
            ]

        row_dias = ft.Row(scroll="auto", spacing=8, alignment="center")
        def actualizar_ui_dias():
            row_dias.controls = [
                ft.TextButton(
                    f"DÍA {i}", 
                    on_click=lambda e, n=i: update_workout_list(n)
                ) for i in range(1, 6)
            ]

        actualizar_ui_meses()
        actualizar_ui_semanas()
        update_workout_list(init=True)

        content_area = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("ENTRENAMIENTO", size=22, weight="bold", color="#FFD700"),
                    sync_indicator
                ], alignment="spaceBetween"),
                status_header,
                ft.Divider(height=10, color="transparent"),
                # BARRA DE PROGRESO DE RUTINA (INYECCIÓN DE FIX)
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("PROGRESO HOY", size=10, color="white54", weight="bold"),
                            lbl_percent
                        ], alignment="spaceBetween"),
                        progress_bar
                    ], spacing=5),
                    padding=ft.padding.only(left=20, right=20)
                ),
                ft.Divider(height=10, color="transparent"),
                row_meses,
                row_semanas,
                ft.Divider(height=10, color="white12"),
                row_dias,
                cardio_panel,
                lista_ejercicios,
                ft.Container(height=20),
                ft.ElevatedButton("FINALIZAR ENTRENAMIENTO", icon=ft.icons.CHECK_CIRCLE, on_click=finalizar_entreno,
                                bgcolor="#4CAF50", color="white", width=350, height=50),
                ft.Container(height=40)
            ], horizontal_alignment="center", scroll=ft.ScrollMode.ADAPTIVE),
            expand=True,
        )

        return ft.Stack([
            content_area,
            timer_overlay,
            summary_overlay
        ], expand=True)

    except Exception as e:
        print(f"FATAL_ERROR_VIEW: {e}")
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.ERROR_OUTLINE, color="red", size=50),
                ft.Text("Error al cargar el módulo de entrenamiento.", color="white", size=18, weight="bold"),
                ft.Text(f"Detalle: {str(e)}", color="white54", text_align="center"),
                ft.ElevatedButton(
                    "Regresar a Inicio", 
                    on_click=lambda _: setattr(page.navigation_bar, "selected_index", 0) or page.navigation_bar.on_change(ft.ControlEvent(target=page.navigation_bar.uid, name="change", data="0", control=page.navigation_bar, page=page))
                )
            ], alignment="center", horizontal_alignment="center"),
            expand=True, bgcolor="#121212", padding=40
        )


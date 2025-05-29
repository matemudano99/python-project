import tkinter as tk
from tkinter import messagebox
import time


class MineroEspacial:
    def __init__(self, ventana_juego):
        self.ventana_juego = ventana_juego
        ventana_juego.title("⭐ Minero Espacial ⭐")
        ventana_juego.geometry("400x500")
        ventana_juego.resizable(False, False)

        # Colores temáticos espaciales
        self.color_fondo = "#0B1609"
        self.color_texto = "#ffffff"
        self.color_boton_fondo = "#013314"
        self.color_boton_texto = "#ffffff"
        self.color_boton_especial = "#2d7231"
        self.color_cristales = "#00ffaa"

        ventana_juego.config(bg=self.color_fondo)

        # Variables del juego
        self.cristales = 0
        self.nivel_taladro = 1
        self.costo_mejora_taladro = 15
        self.cristales_base_por_extraccion = 1

        self.nivel_robot_minero = 0
        self.costo_robot_minero = 50
        self.cristales_por_robot = 2
        self.ingreso_automatico = 0

        self.nivel_scanner = 0
        self.costo_scanner = 100
        self.eficiencia_scanner = 0  # Cristales extra por extracción

        self.cristales_para_victoria = 25000
        self.tiempo_inicio = time.time()
        self.juego_activo = True
        self.modo_infinito = False

        # Contadores para efectos visuales
        self.clicks_totales = 0
        self.asteroides_minados = 0

        self._configurar_interfaz()
        self._actualizar_interfaz()
        self._iniciar_mineria_automatica()
        self._iniciar_temporizador()

    def _configurar_interfaz(self):
        # Título del juego
        titulo = tk.Label(
            self.ventana_juego,
            text="🚀 MINERO ESPACIAL 🚀",
            font=("Arial", 18, "bold"),
            bg=self.color_fondo,
            fg=self.color_cristales,
        )
        titulo.pack(pady=10)

        # Contador principal de cristales
        self.etiqueta_cristales = tk.Label(
            self.ventana_juego,
            text="",
            font=("Arial", 24, "bold"),
            bg=self.color_fondo,
            fg=self.color_cristales,
        )
        self.etiqueta_cristales.pack(pady=5)

        # Información de extracción
        self.etiqueta_extraccion = tk.Label(
            self.ventana_juego,
            text="",
            font=("Arial", 10),
            bg=self.color_fondo,
            fg=self.color_texto,
        )
        self.etiqueta_extraccion.pack()

        # Información de minería automática
        self.etiqueta_automatica = tk.Label(
            self.ventana_juego,
            text="",
            font=("Arial", 10),
            bg=self.color_fondo,
            fg=self.color_texto,
        )
        self.etiqueta_automatica.pack(pady=(0, 5))

        # Estadísticas del jugador
        self.etiqueta_stats = tk.Label(
            self.ventana_juego,
            text="",
            font=("Arial", 9),
            bg=self.color_fondo,
            fg="#cccccc",
        )
        self.etiqueta_stats.pack(pady=(0, 10))

        # Temporizador
        self.etiqueta_temporizador = tk.Label(
            self.ventana_juego,
            text="Tiempo: 0s",
            font=("Arial", 12),
            bg=self.color_fondo,
            fg=self.color_texto,
        )
        self.etiqueta_temporizador.pack()

        # Botón principal de minería
        self.boton_minar = tk.Button(
            self.ventana_juego,
            text="⛏️ MINAR ASTEROIDE ⛏️",
            command=self._minar_asteroide,
            font=("Arial", 14, "bold"),
            width=20,
            height=1,
            bg=self.color_boton_especial,
            fg=self.color_texto,
        )
        self.boton_minar.pack(pady=15)

        # Botones de mejoras
        self.boton_mejorar_taladro = tk.Button(
            self.ventana_juego,
            text="",
            command=self._mejorar_taladro,
            font=("Arial", 10),
            width=35,
            bg=self.color_boton_fondo,
            fg=self.color_texto,
        )
        self.boton_mejorar_taladro.pack(pady=3)

        self.boton_comprar_robot = tk.Button(
            self.ventana_juego,
            text="",
            command=self._comprar_robot,
            font=("Arial", 10),
            width=35,
            bg=self.color_boton_fondo,
            fg=self.color_texto,
        )
        self.boton_comprar_robot.pack(pady=3)

        self.boton_mejorar_scanner = tk.Button(
            self.ventana_juego,
            text="",
            command=self._mejorar_scanner,
            font=("Arial", 10),
            width=35,
            bg=self.color_boton_fondo,
            fg=self.color_texto,
        )
        self.boton_mejorar_scanner.pack(pady=3)

        # Botón de victoria
        self.boton_victoria = tk.Button(
            self.ventana_juego,
            text=f"🏆 COMPLETAR MISIÓN 🏆\n({self.cristales_para_victoria:,} cristales)",
            command=self._completar_mision,
            font=("Arial", 11, "bold"),
            width=35,
            bg="#2a5a2a",
            fg=self.color_texto,
        )
        self.boton_victoria.pack(pady=10)

        # Botón modo infinito (oculto inicialmente)
        self.boton_infinito = tk.Button(
            self.ventana_juego,
            text="🌌 EXPLORACIÓN INFINITA 🌌",
            command=self._activar_modo_infinito,
            font=("Arial", 12, "bold"),
            width=35,
            bg="#1a1a5a",
            fg=self.color_texto,
            state=tk.DISABLED,
        )
        self.boton_infinito.pack_forget()

    def _obtener_cristales_por_extraccion(self):
        base = self.cristales_base_por_extraccion + (self.nivel_taladro - 1) * 2
        # Bonus fijo del scanner
        bonus_scanner = self.nivel_scanner * self.eficiencia_scanner
        return base + bonus_scanner

    def _minar_asteroide(self):
        cristales_obtenidos = self._obtener_cristales_por_extraccion()
        self.cristales += cristales_obtenidos
        self.clicks_totales += 1
        self.asteroides_minados += 1

        # Cambiar temporalmente el texto del botón para dar feedback
        texto_original = self.boton_minar.cget("text")
        self.boton_minar.config(text=f"💎 +{cristales_obtenidos} cristales! 💎")
        self._restaurar_texto_boton(texto_original)

        self._actualizar_interfaz()

    def _restaurar_texto_boton(self, texto_original):
        self.ventana_juego.after(300, self._cambiar_texto_boton_original)
        self.texto_boton_original = texto_original

    def _cambiar_texto_boton_original(self):
        self.boton_minar.config(text=self.texto_boton_original)

    def _mejorar_taladro(self):
        if self.cristales >= self.costo_mejora_taladro:
            self.cristales -= self.costo_mejora_taladro
            self.nivel_taladro += 1
            self.costo_mejora_taladro = int(self.costo_mejora_taladro * 2.2)
            self._actualizar_interfaz()

    def _comprar_robot(self):
        if self.cristales >= self.costo_robot_minero:
            self.cristales -= self.costo_robot_minero
            self.nivel_robot_minero += 1
            self.costo_robot_minero = int(self.costo_robot_minero * 2.5)
            self._recalcular_mineria_automatica()
            self._actualizar_interfaz()

    def _mejorar_scanner(self):
        if self.cristales >= self.costo_scanner:
            self.cristales -= self.costo_scanner
            self.nivel_scanner += 1
            self.eficiencia_scanner = 2  # +2 cristales extra por extracción por nivel
            self.costo_scanner = int(self.costo_scanner * 3.0)
            self._actualizar_interfaz()

    def _recalcular_mineria_automatica(self):
        self.ingreso_automatico = self.nivel_robot_minero * self.cristales_por_robot

    def _iniciar_mineria_automatica(self):
        self._tick_mineria_automatica()

    def _tick_mineria_automatica(self):
        if self.juego_activo or self.modo_infinito:
            self.cristales += self.ingreso_automatico
            self._actualizar_interfaz()
        self.ventana_juego.after(1000, self._tick_mineria_automatica)

    def _iniciar_temporizador(self):
        if self.juego_activo:
            tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            minutos = tiempo_transcurrido // 60
            segundos = tiempo_transcurrido % 60
            self.etiqueta_temporizador.config(text=f"Tiempo: {minutos}m {segundos}s")
            self.ventana_juego.after(1000, self._iniciar_temporizador)
        elif self.modo_infinito:
            self.etiqueta_temporizador.config(text="🌌 Exploración Infinita Activa 🌌")

    def _completar_mision(self):
        if self.cristales >= self.cristales_para_victoria and not self.modo_infinito:
            self.juego_activo = False
            tiempo_final = int(time.time() - self.tiempo_inicio)
            minutos = tiempo_final // 60
            segundos = tiempo_final % 60

            ventana_victoria = tk.Toplevel(self.ventana_juego)
            ventana_victoria.title("🏆 ¡MISIÓN COMPLETADA! 🏆")
            ventana_victoria.geometry("350x200")
            ventana_victoria.resizable(False, False)
            ventana_victoria.config(bg=self.color_fondo)

            mensaje = f"🎉 ¡FELICIDADES, MINERO! 🎉\n\n"
            mensaje += f"⏱️ Tiempo: {minutos}m {segundos}s\n"
            mensaje += f"⛏️ Asteroides minados: {self.asteroides_minados}\n"
            mensaje += f"🤖 Robots desplegados: {self.nivel_robot_minero}\n"
            mensaje += f"💎 Cristales totales: {int(self.cristales):,}"

            etiqueta_victoria = tk.Label(
                ventana_victoria,
                text=mensaje,
                font=("Arial", 12, "bold"),
                bg=self.color_fondo,
                fg=self.color_cristales,
                justify=tk.CENTER,
            )
            etiqueta_victoria.pack(pady=20)

            self.boton_infinito.pack(pady=5)
            self.boton_victoria.config(state=tk.DISABLED)

        elif self.modo_infinito:
            messagebox.showinfo(
                "Exploración Infinita",
                "🌌 Ya estás explorando el espacio infinito.\n¡Sigue minando y mejorando tu equipo!",
            )
        else:
            faltante = self.cristales_para_victoria - self.cristales
            messagebox.showinfo(
                "Misión Incompleta",
                f"❗ Necesitas {faltante:,} cristales más\npara completar la misión.",
            )

    def _activar_modo_infinito(self):
        self.modo_infinito = True
        self.juego_activo = False
        self.etiqueta_temporizador.config(text="🌌 Exploración Infinita Activa 🌌")
        self.boton_victoria.config(state=tk.DISABLED)
        self.boton_infinito.config(state=tk.DISABLED)
        messagebox.showinfo(
            "Modo Infinito Activado",
            "🚀 ¡Bienvenido a la exploración infinita!\n\n"
            "Ahora puedes seguir minando sin límites.\n"
            "¡Conviértete en el mejor minero espacial!",
        )

    def _actualizar_interfaz(self):
        # Actualizar contador principal
        self.etiqueta_cristales.config(text=f"💎 {int(self.cristales):,} Cristales")

        # Información de extracción
        cristales_por_click = self._obtener_cristales_por_extraccion()
        self.etiqueta_extraccion.config(
            text=f"⛏️ Por extracción: {cristales_por_click} cristales"
        )

        # Información automática
        self.etiqueta_automatica.config(
            text=f"🤖 Minería automática: {self.ingreso_automatico:,} cristales/seg"
        )

        # Estadísticas
        progreso = min(100, (self.cristales / self.cristales_para_victoria) * 100)
        stats_text = f"📊 Progreso: {progreso:.1f}% | Asteroides: {self.asteroides_minados} | Clicks: {self.clicks_totales}"
        self.etiqueta_stats.config(text=stats_text)

        # Botón de taladro
        self.boton_mejorar_taladro.config(
            text=f"🔧 Mejorar Taladro (Nivel {self.nivel_taladro})\nCoste: {self.costo_mejora_taladro:,} cristales",
            state=(
                tk.NORMAL
                if self.cristales >= self.costo_mejora_taladro
                and (self.juego_activo or self.modo_infinito)
                else tk.DISABLED
            ),
        )

        # Botón de robot
        self.boton_comprar_robot.config(
            text=f"🤖 Comprar Robot Minero (Tienes: {self.nivel_robot_minero})\nCoste: {self.costo_robot_minero:,} cristales",
            state=(
                tk.NORMAL
                if self.cristales >= self.costo_robot_minero
                and (self.juego_activo or self.modo_infinito)
                else tk.DISABLED
            ),
        )

        # Botón de scanner
        bonus_scanner = (
            self.nivel_scanner * self.eficiencia_scanner
            if self.nivel_scanner > 0
            else 0
        )
        texto_scanner = f"📡 Mejorar Scanner (Nivel {self.nivel_scanner}"
        if self.nivel_scanner > 0:
            texto_scanner += f" - +{bonus_scanner} cristales"
        texto_scanner += f")\nCoste: {self.costo_scanner:,} cristales"

        self.boton_mejorar_scanner.config(
            text=texto_scanner,
            state=(
                tk.NORMAL
                if self.cristales >= self.costo_scanner
                and (self.juego_activo or self.modo_infinito)
                else tk.DISABLED
            ),
        )

        # Botón de victoria
        if not self.modo_infinito:
            self.boton_victoria.config(
                state=(
                    tk.NORMAL
                    if self.cristales >= self.cristales_para_victoria
                    else tk.DISABLED
                )
            )
        else:
            self.boton_victoria.config(state=tk.DISABLED)


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    juego = MineroEspacial(ventana_principal)
    ventana_principal.mainloop()

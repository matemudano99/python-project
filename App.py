import tkinter as tk
from tkinter import messagebox
import random

class Carta:
    def __init__(self, nombre, coste, ataque, salud):
        self.nombre = nombre
        self.coste = coste
        self.ataque = ataque
        self.salud = salud
        self.puede_atacar = False

    def atacar(self, objetivo):
        # Esta función ahora solo maneja el daño de UNA carta a su objetivo.
        # La lógica de daño mutuo entre cartas se manejará en Juego._resolver_ataques.
        if hasattr(objetivo, 'ataque'): # Si el objetivo es una carta
            # El daño mutuo se gestiona en _resolver_ataques
            pass 
        else: # Si el objetivo es un jugador
            objetivo.salud -= self.ataque
        self.puede_atacar = False

class Jugador:
    def __init__(self, nombre, mazo, juego_ref):
        self.nombre = nombre
        self.salud = 30
        self.mana_max = 1 
        self.mana = 1     
        self.mano = []
        self.banco = []
        self.tablero = []
        self.mazo = mazo[:]
        random.shuffle(self.mazo)
        self.pasado_turno = False
        self.fase = "Ataque"
        self.juego = juego_ref 

    def cambiar_fase(self):
        if self.fase == "Ataque":
            self.fase = "Defensa"
        else:
            self.fase = "Ataque"

    def robar(self):
        if self.mazo:
            self.mano.append(self.mazo.pop())

    def mover_a_banco(self, indice):
        if indice < len(self.mano):
            carta = self.mano[indice]
            if carta.coste <= self.mana:
                self.mana -= carta.coste
                self.banco.append(self.mano.pop(indice))
                return True
            else:
                return False
        return False

    def desplegar(self, indice):
        if indice < len(self.banco) and len(self.tablero) < 7:
            carta = self.banco.pop(indice)
            if self.juego.fase_defensa_activa and self.fase == "Defensa":
                carta.puede_atacar = False
            else:
                carta.puede_atacar = True
            self.tablero.append(carta)

    def tablero_a_banco(self):
        self.banco.extend(self.tablero)
        self.tablero = []

    def iniciar_turno(self):
        if self.mana_max < 10: 
            self.mana_max += 1
        self.mana = self.mana_max
        self.robar()
        self.pasado_turno = False
        for c in self.tablero:
            c.puede_atacar = True

class Juego:
    def __init__(self, root):
        self.root = root
        nombres = ['Tralalelo Tralala', 'Bombardino cocodrillo', 'Bombombini Gusini',
                   'Trippi Troppi', 'Burbaloni Luliloli', 'Tracotocutulo Lirilì Larilà',
                   'Brr brr Patapim', 'Trulimero Trulicina', 'Bobrini Cocosini',
                   'Frigo Camello', 'Frulli Frulla', 'La vaca saturno saturnita',
                   'Crocodildo Penisini', 'Bobritto bandito', 'Giraffa Celeste',
                   'Cappuccino Assassino', 'Glorbo Fruttodrillo', 'Camelrino Tazzino',
                   'Ambatron', 'Kaktus tus tus kutus kutus']
        
        mazo_base = []
        for n in nombres:
            carta = Carta(n, random.randint(1,5), random.randint(1,5), random.randint(1,6))
            mazo_base.append(carta)

        self.jugadores = [Jugador('Jugador 1', mazo_base, self), Jugador('Jugador 2', mazo_base, self)]
        self.turno = 0
        self.fase_defensa_activa = False 
        self.configurar()
        for j in self.jugadores:
            for _ in range(3): j.robar()
        
        self.jugadores[0].iniciar_turno() 
        self.jugadores[1].pasado_turno = True 
        self.actualizar()
        root.mainloop()

    def configurar(self):
        self.root.title('Mini CCG')
        self.root.geometry('1200x600')
        self.lst_mano = []
        self.lst_banco = []
        self.lst_tablero = []
        self.lbl_stats = []
        self.lbl_fase = []
        self.btn_atacar_jugador = []
        self.btn_pasar_turno_jugador = []

        for i in [0,1]:
            panel = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            tk.Label(panel, text=self.jugadores[i].nombre, font=('Arial',16)).pack()

            fase_frame = tk.Frame(panel, bg="lightgray", bd=1, relief=tk.RAISED)
            fase_frame.pack(fill=tk.X, pady=5)
            lbl_fase = tk.Label(fase_frame, text="FASE: ATAQUE", font=('Arial', 12, 'bold'), fg="red")
            lbl_fase.pack(pady=3)
            self.lbl_fase.append(lbl_fase)

            botones_frame = tk.Frame(panel)
            botones_frame.pack(fill=tk.X, pady=5)
            
            def crear_funcion_atacar(idx_jugador):
                def funcion_atacar():
                    self.atacar_cartas(idx_jugador)
                return funcion_atacar
            
            btn_atacar = tk.Button(botones_frame, text=f'Atacar', 
                                   command=crear_funcion_atacar(i))
            btn_atacar.pack(side=tk.LEFT, padx=5)
            self.btn_atacar_jugador.append(btn_atacar)

            def crear_funcion_pasar_turno(idx_jugador):
                def funcion_pasar_turno():
                    self.pasar_turno(idx_jugador)
                return funcion_pasar_turno

            btn_pasar = tk.Button(botones_frame, text=f'Finalizar Turno', 
                                  command=crear_funcion_pasar_turno(i))
            btn_pasar.pack(side=tk.RIGHT, padx=5)
            self.btn_pasar_turno_jugador.append(btn_pasar)

            tk.Label(panel, text='Mano', font=('Arial',14)).pack()
            lm = tk.Listbox(panel, height=6)
            lm.pack(fill=tk.X)
            
            def crear_funcion_mano_doble(idx_jugador):
                def funcion_mano_doble(event):
                    self.on_mano_doble(idx_jugador)
                return funcion_mano_doble

            lm.bind('<Double-1>', crear_funcion_mano_doble(i))
            self.lst_mano.append(lm)

            tk.Label(panel, text='Banco', font=('Arial',14)).pack()
            lb = tk.Listbox(panel, height=6)
            lb.pack(fill=tk.X)
            
            def crear_funcion_banco_doble(idx_jugador):
                def funcion_banco_doble(event):
                    self.on_banco_doble(idx_jugador)
                return funcion_banco_doble

            lb.bind('<Double-1>', crear_funcion_banco_doble(i))
            self.lst_banco.append(lb)

            tk.Label(panel, text='Campo', font=('Arial',14)).pack()
            lt = tk.Listbox(panel, height=6)
            lt.pack(fill=tk.X)
            self.lst_tablero.append(lt)

            lbl = tk.Label(panel, text='')
            lbl.pack(pady=5)
            self.lbl_stats.append(lbl)

        self.actualizar_botones()

    def actualizar_botones(self):
        for i in range(2):
            jugador_actual = self.jugadores[i]
            es_turno_actual = (not jugador_actual.pasado_turno)
            
            if es_turno_actual and jugador_actual.fase == "Ataque" and not self.fase_defensa_activa:
                self.btn_atacar_jugador[i].config(state=tk.NORMAL)
            else:
                self.btn_atacar_jugador[i].config(state=tk.DISABLED)
            
            if es_turno_actual or (self.fase_defensa_activa and jugador_actual.fase == "Defensa"):
                 self.btn_pasar_turno_jugador[i].config(state=tk.NORMAL)
            else:
                self.btn_pasar_turno_jugador[i].config(state=tk.DISABLED)

            fase_texto = "FASE: " + jugador_actual.fase.upper()
            color = "red" if jugador_actual.fase == "Ataque" else "blue"
            if self.fase_defensa_activa:
                if jugador_actual.fase == "Defensa":
                    color = "purple"
                    fase_texto = "FASE: DEFENSA (PREPARA)"
                else: 
                    color = "orange"
                    fase_texto = "FASE: ESPERANDO RESOLUCIÓN"

            self.lbl_fase[i].config(text=fase_texto, fg=color)

    def actualizar(self):
        for i,j in enumerate(self.jugadores):
            self.lst_mano[i].delete(0, tk.END)
            for c in j.mano:
                estado_mana = ""
                if c.coste <= j.mana:
                    estado_mana = "✅"
                else:
                    estado_mana = "❌"
                self.lst_mano[i].insert(tk.END, f"{estado_mana} {c.nombre} ⚔️{c.ataque} ❤️{c.salud} (🔮{c.coste})")

            self.lst_banco[i].delete(0, tk.END)
            for c in j.banco:
                self.lst_banco[i].insert(tk.END, f"{c.nombre} ⚔️{c.ataque} ❤️{c.salud}")

            self.lst_tablero[i].delete(0, tk.END)
            for c in j.tablero:
                status = ""
                if c.puede_atacar and not self.fase_defensa_activa:
                    status = "🟢"
                else:
                    status = "🔴"
                self.lst_tablero[i].insert(tk.END, f"{status} {c.nombre} ⚔️{c.ataque} ❤️{c.salud}")

            self.lbl_stats[i].config(text=f"❤️{j.salud} ⚡{j.mana}/{j.mana_max}")

        self.verificar_fin_juego()
        self.actualizar_botones()

    def on_mano_doble(self, jugador_idx):
        jugador_actual = self.jugadores[jugador_idx]
        if jugador_actual.pasado_turno or self.fase_defensa_activa:
            messagebox.showinfo("Aviso", "No es tu turno o no puedes jugar cartas de la mano ahora.")
            return

        sel = self.lst_mano[jugador_idx].curselection()
        if sel:
            result = jugador_actual.mover_a_banco(sel[0])
            if not result:
                messagebox.showinfo("Aviso", "No tienes suficiente mana para jugar esta carta")
                return
            self.actualizar()

    def on_banco_doble(self, jugador_idx):
        jugador_actual = self.jugadores[jugador_idx]

        if jugador_actual.pasado_turno and not self.fase_defensa_activa:
            messagebox.showinfo("Aviso", "No es tu turno.")
            return
        
        if not ( (not jugador_actual.pasado_turno and jugador_actual.fase == "Ataque") or \
                 (self.fase_defensa_activa and jugador_actual.fase == "Defensa") ):
            messagebox.showinfo("Aviso", "No puedes desplegar cartas en este momento.")
            return

        sel = self.lst_banco[jugador_idx].curselection()
        if sel:
            jugador_actual.desplegar(sel[0])
            self.actualizar()

    def atacar_cartas(self, jugador_idx):
        atacante = self.jugadores[jugador_idx]
        defensor = self.jugadores[1 - jugador_idx]

        if atacante.pasado_turno:
            messagebox.showinfo("Aviso", "No es tu turno")
            return
        
        if atacante.fase != "Ataque":
            messagebox.showinfo("Aviso", "¡No puedes atacar en esta fase!")
            return
        
        if not atacante.tablero:
            messagebox.showinfo("Aviso", "No tienes cartas en el campo para atacar.")
            return

        self.fase_defensa_activa = True
        
        atacante.fase = "Esperando Resolución" 
        atacante.pasado_turno = True 

        defensor.fase = "Defensa"
        defensor.pasado_turno = False 
        
        defensor.mana += 1 
        
        messagebox.showinfo("Fase de Defensa", 
                             f"¡{defensor.nombre}, es tu turno de organizar la defensa!\n"
                             f"Tienes {defensor.mana}/{defensor.mana_max} de Maná. Pulsa 'Finalizar Turno' cuando estés listo.")
        self.actualizar()
        self.actualizar_botones()

    def _resolver_ataques(self, atacante, defensor):
        """Lógica para resolver los ataques después de la fase de defensa."""
        ataques_realizados = []

        # Es crucial crear una copia del tablero del atacante para poder modificarlo
        # (moviendo cartas al banco) mientras se itera sobre él.
        # Las cartas que estaban en el tablero del atacante al momento de pulsar "Atacar" son las que atacan.
        # Las cartas que fueron movidas al tablero del defensor durante la fase de defensa serán las que defiendan.
        cartas_atacantes_al_inicio = atacante.tablero[:] 
        atacante.tablero = [] # Vacía el tablero del atacante, ya que las cartas atacantes irán al banco.

        # Iterar sobre las cartas atacantes
        for carta_atacante in cartas_atacantes_al_inicio:
            # Si el defensor tiene cartas en su tablero para bloquear
            if defensor.tablero:
                # Tomar la primera carta del defensor como objetivo de bloqueo
                carta_defensora = defensor.tablero[0]

                # ¡Aquí es donde se aplica el daño mutuo!
                # El atacante daña al defensor
                carta_defensora.salud -= carta_atacante.ataque
                # El defensor daña al atacante
                carta_atacante.salud -= carta_defensora.ataque 

                ataques_realizados.append(f"{carta_atacante.nombre} (⚔️{carta_atacante.ataque}) atacó a {carta_defensora.nombre} (⚔️{carta_defensora.ataque}).")
                
                # Después de la batalla, las cartas atacantes vuelven al banco
                carta_atacante.puede_atacar = False
                atacante.banco.append(carta_atacante)

            else:
                # Si no hay cartas defensoras, el ataque va directo al jugador
                carta_atacante.atacar(defensor) # Llama al método atacar para dañar directamente al jugador
                ataques_realizados.append(f"{carta_atacante.nombre} (⚔️{carta_atacante.ataque}) atacó directamente a {defensor.nombre}.")
                
                # Después de atacar al jugador, la carta atacante vuelve al banco
                carta_atacante.puede_atacar = False
                atacante.banco.append(carta_atacante)

        # Después de que todas las batallas se hayan resuelto, limpiar las cartas muertas del tablero del defensor.
        cartas_defensor_vivas = []
        for c_defensor in defensor.tablero:
            if c_defensor.salud > 0:
                cartas_defensor_vivas.append(c_defensor)
        defensor.tablero = cartas_defensor_vivas

        # También limpiar las cartas muertas del atacante que podrían haber quedado en su banco después de recibir daño.
        # (Aunque en la lógica actual se añaden al banco incluso si mueren, es buena práctica limpiar).
        cartas_atacante_vivas_en_banco = []
        for c_atacante in atacante.banco:
            if c_atacante.salud > 0:
                cartas_atacante_vivas_en_banco.append(c_atacante)
        atacante.banco = cartas_atacante_vivas_en_banco


        if ataques_realizados:
            messagebox.showinfo("Resumen de Ataques", "\n".join(ataques_realizados))

        # Restablecer fases y turnos después de la resolución
        self.fase_defensa_activa = False
        atacante.fase = "Defensa" 
        defensor.fase = "Ataque"  
        
        # Restablecer el maná actual del defensor a su máximo después de la fase de defensa
        defensor.mana = defensor.mana_max 

        self.actualizar()
        self.actualizar_botones()


    def limpiar(self):
        # Esta función asegura que solo las cartas con salud positiva permanezcan en el tablero
        # (la eliminación de cartas muertas ya se hace en _resolver_ataques, esto es una capa extra)
        
        cartas_vivas_jugador1 = []
        for c in self.jugadores[0].tablero:
            if c.salud > 0:
                cartas_vivas_jugador1.append(c)
        self.jugadores[0].tablero = cartas_vivas_jugador1

        cartas_vivas_jugador2 = []
        for c in self.jugadores[1].tablero:
            if c.salud > 0:
                cartas_vivas_jugador2.append(c)
        self.jugadores[1].tablero = cartas_vivas_jugador2


    def pasar_turno(self, jugador_idx):
        jugador_que_paso = self.jugadores[jugador_idx]
        
        if self.fase_defensa_activa and jugador_que_paso.fase == "Defensa":
            atacante = self.jugadores[1-jugador_idx] 
            defensor = jugador_que_paso 

            messagebox.showinfo("Fase de Defensa Terminada", f"¡{defensor.nombre} ha organizado su defensa! Resolviendo ataques...")
            
            self._resolver_ataques(atacante, defensor)

            atacante.pasado_turno = True
            defensor.pasado_turno = True
            self.actualizar_botones() 

            if atacante.pasado_turno and defensor.pasado_turno:
                for j in self.jugadores:
                    j.tablero_a_banco() 
                    j.iniciar_turno()   
                self.actualizar()
                messagebox.showinfo("Inicio de Turno", "¡Un nuevo turno ha comenzado!")
        else:
            jugador_que_paso.pasado_turno = True
            self.actualizar_botones()
            
            todos_pasaron = True
            for j in self.jugadores:
                if not j.pasado_turno:
                    todos_pasaron = False
                    break

            if todos_pasaron:
                self.limpiar()
                for j in self.jugadores:
                    j.tablero_a_banco()
                    j.iniciar_turno() 
                self.actualizar()
                messagebox.showinfo("Inicio de Turno", "¡Un nuevo turno ha comenzado!")
            else:
                messagebox.showinfo("Turno", f"El {self.jugadores[jugador_idx].nombre} ha pasado su turno")

    def verificar_fin_juego(self):
        for i, j in enumerate(self.jugadores):
            if j.salud <= 0:
                ganador = self.jugadores[1-i].nombre
                messagebox.showinfo("Fin del juego", f"¡{ganador} ha ganado!")
                self.root.quit()
                return True
        return False

if __name__=='__main__':
    Juego(tk.Tk())
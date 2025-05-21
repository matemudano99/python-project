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
        objetivo.salud -= self.ataque
        if hasattr(objetivo, 'ataque'):
            self.salud -= objetivo.ataque
        self.puede_atacar = False

class Jugador:
    def __init__(self, nombre, mazo):
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
        self.fase = "Ataque"  # Fase inicial: "Ataque" o "Defensa"
        
    def cambiar_fase(self):
        self.fase = "Defensa" if self.fase == "Ataque" else "Ataque"

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
            self.tablero.append(carta)
            
    def tablero_a_banco(self):
        # Devolver todas las cartas del tablero al banco
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
        mazo_base = [Carta(n, random.randint(1,5), random.randint(1,5), random.randint(1,6)) for n in nombres]
        self.jugadores = [Jugador('Jugador 1', mazo_base), Jugador('Jugador 2', mazo_base)]
        self.turno = 0
        self.configurar()
        for j in self.jugadores:
            for _ in range(3): j.robar()
        self.jugadores[self.turno].iniciar_turno()
        self.actualizar()
        root.mainloop()

    def configurar(self):
        self.root.title('Mini CCG')
        self.root.geometry('1200x600')
        frames = []
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
            
            # Indicador de fase (ataque/defensa)
            fase_frame = tk.Frame(panel, bg="lightgray", bd=1, relief=tk.RAISED)
            fase_frame.pack(fill=tk.X, pady=5)
            lbl_fase = tk.Label(fase_frame, text="FASE: ATAQUE", font=('Arial', 12, 'bold'), fg="red")
            lbl_fase.pack(pady=3)
            self.lbl_fase.append(lbl_fase)
            
            # Botones específicos para cada jugador en su propio HUD
            botones_frame = tk.Frame(panel)
            botones_frame.pack(fill=tk.X, pady=5)
            btn_atacar = tk.Button(botones_frame, text=f'Atacar', 
                                   command=lambda idx=i: self.atacar_cartas(idx))
            btn_atacar.pack(side=tk.LEFT, padx=5)
            self.btn_atacar_jugador.append(btn_atacar)
            
            btn_pasar = tk.Button(botones_frame, text=f'Finalizar Turno', 
                                 command=lambda idx=i: self.pasar_turno(idx))
            btn_pasar.pack(side=tk.RIGHT, padx=5)
            self.btn_pasar_turno_jugador.append(btn_pasar)
            
            tk.Label(panel, text='Mano', font=('Arial',14)).pack()
            lm = tk.Listbox(panel, height=6)
            lm.pack(fill=tk.X)
            lm.bind('<Double-1>', lambda e, idx=i: self.on_mano_doble(idx))
            self.lst_mano.append(lm)
            
            tk.Label(panel, text='Banco', font=('Arial',14)).pack()
            lb = tk.Listbox(panel, height=6)
            lb.pack(fill=tk.X)
            lb.bind('<Double-1>', lambda e, idx=i: self.on_banco_doble(idx))
            self.lst_banco.append(lb)
            
            tk.Label(panel, text='Campo', font=('Arial',14)).pack()
            lt = tk.Listbox(panel, height=6)
            lt.pack(fill=tk.X)
            self.lst_tablero.append(lt)
            
            lbl = tk.Label(panel, text='')
            lbl.pack(pady=5)
            self.lbl_stats.append(lbl)
        
        # Actualizar botones según el turno actual
        self.actualizar_botones()

    def actualizar_botones(self):
        # Habilitar/deshabilitar botones según el turno y fase
        for i in range(2):
            es_turno_actual = (not self.jugadores[i].pasado_turno)
            puede_atacar = es_turno_actual and self.jugadores[i].fase == "Ataque"
            
            # Actualizar botón de ataque según la fase
            self.btn_atacar_jugador[i].config(state=tk.NORMAL if puede_atacar else tk.DISABLED)
            self.btn_pasar_turno_jugador[i].config(state=tk.NORMAL if es_turno_actual else tk.DISABLED)
            
            # Actualizar etiqueta de fase
            fase_texto = f"FASE: {self.jugadores[i].fase.upper()}"
            color = "red" if self.jugadores[i].fase == "Ataque" else "blue"
            self.lbl_fase[i].config(text=fase_texto, fg=color)

    def actualizar(self):
        for i,j in enumerate(self.jugadores):
            self.lst_mano[i].delete(0, tk.END)
            for c in j.mano:
                estado_mana = "✅" if c.coste <= j.mana else "❌"
                self.lst_mano[i].insert(tk.END, f"{estado_mana} {c.nombre} ⚔️{c.ataque} ❤️{c.salud} (🔮{c.coste})")
            
            self.lst_banco[i].delete(0, tk.END)
            for c in j.banco:
                self.lst_banco[i].insert(tk.END, f"{c.nombre} ⚔️{c.ataque} ❤️{c.salud}")
            
            self.lst_tablero[i].delete(0, tk.END)
            for c in j.tablero:
                status = "🟢" if c.puede_atacar else "🔴"
                self.lst_tablero[i].insert(tk.END, f"{status} {c.nombre} ⚔️{c.ataque} ❤️{c.salud}")
            
            self.lbl_stats[i].config(text=f"❤️{j.salud} ⚡{j.mana}/{j.mana_max}")
        
        # Verificar si el juego ha terminado
        self.verificar_fin_juego()
        
        # Actualizar estados de los botones y fases
        self.actualizar_botones()

    def on_mano_doble(self, jugador):
        if self.jugadores[jugador].pasado_turno:
            messagebox.showinfo("Aviso", "No es tu turno")
            return
            
        sel = self.lst_mano[jugador].curselection()
        if sel:
            # Mover carta de la mano al banco
            result = self.jugadores[jugador].mover_a_banco(sel[0])
            
            # Si no tenía suficiente mana
            if not result:
                messagebox.showinfo("Aviso", "No tienes suficiente mana para jugar esta carta")
                return
                
            # Pasar el turno al oponente sin cambiar las fases
            self.jugadores[jugador].pasado_turno = True
            oponente = 1 - jugador
            self.jugadores[oponente].pasado_turno = False
            
            messagebox.showinfo("Cambio de Turno", f"Turno del {self.jugadores[oponente].nombre}")
            self.actualizar_botones()
            self.actualizar()

    def on_banco_doble(self, jugador):
        if self.jugadores[jugador].pasado_turno:
            messagebox.showinfo("Aviso", "No es tu turno")
            return
            
        sel = self.lst_banco[jugador].curselection()
        if sel:
            self.jugadores[jugador].desplegar(sel[0])
            self.actualizar()

    def atacar_cartas(self, jugador):
        # Sistema de batalla automático - cada carta ataca a la que está en su misma posición
        if self.jugadores[jugador].pasado_turno:
            messagebox.showinfo("Aviso", "No es tu turno")
            return
            
        atacante = self.jugadores[jugador]
        defensor = self.jugadores[1-jugador]
        
        # Verificar si es fase de ataque
        if atacante.fase != "Ataque":
            messagebox.showinfo("Aviso", "¡No puedes atacar en fase de defensa!")
            return
        
        # Verificar si hay cartas que pueden atacar
        cartas_atacantes = [c for c in atacante.tablero if c.puede_atacar]
        if not cartas_atacantes:
            messagebox.showinfo("Aviso", "No tienes cartas que puedan atacar")
            return
            
        # Realizar ataques
        ataques_realizados = []
        for i, carta in enumerate(atacante.tablero[:]):
            if not carta.puede_atacar:
                continue
                
            # Si hay una carta enemiga en la misma posición, atacarla
            if i < len(defensor.tablero):
                carta_enemiga = defensor.tablero[i]
                carta.atacar(carta_enemiga)
                ataques_realizados.append(f"{carta.nombre} ha atacado a {carta_enemiga.nombre}")
            else:
                # Si no hay carta enemiga, atacar directamente al jugador
                carta.atacar(defensor)
                ataques_realizados.append(f"{carta.nombre} ha atacado directamente al {defensor.nombre}")
        
        # Mostrar resumen de los ataques
        if ataques_realizados:
            messagebox.showinfo("Resumen de Ataques", "\n".join(ataques_realizados))
        
        # Limpieza después del ataque
        self.limpiar()
        
        # Devolver todas las cartas al banco después del ataque
        atacante.tablero_a_banco()
        defensor.tablero_a_banco()
        
        # Alternar las fases de ambos jugadores después del ataque
        atacante.fase = "Defensa"
        defensor.fase = "Ataque"
        
        # Pasar el turno al oponente
        oponente = 1 - jugador
        atacante.pasado_turno = True
        defensor.pasado_turno = False
        
        messagebox.showinfo("Cambio de Fase", f"¡Cambio de fase!\n{atacante.nombre}: {atacante.fase}\n{defensor.nombre}: {defensor.fase}")
        
        self.actualizar_botones()
        self.actualizar()

    def limpiar(self):
        for j in self.jugadores:
            j.tablero = [c for c in j.tablero if c.salud > 0]

    def pasar_turno(self, jugador):
        self.jugadores[jugador].pasado_turno = True
        self.actualizar_botones()
        
        if all(j.pasado_turno for j in self.jugadores):
            self.limpiar()
            for j in self.jugadores:
                j.iniciar_turno()
            self.actualizar()
        else:
            messagebox.showinfo("Turno", f"El {self.jugadores[jugador].nombre} ha pasado su turno")

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
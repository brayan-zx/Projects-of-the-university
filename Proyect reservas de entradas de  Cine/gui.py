import tkinter as tk
from tkinter import messagebox, ttk

class CineAppGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Sistema de Cine - MVP")
        self.root.geometry("850x550")
        self.root.config(bg="#f0f2f5")

        style = ttk.Style()
        style.theme_use("clam")

        tk.Label(
            root,
            text="🎬 Plataforma de Reservas de Salas de Cine",
            font=("Arial", 16, "bold"),
            bg="#f0f2f5",
        ).pack(pady=15)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        self.tab1 = ttk.Frame(notebook)
        notebook.add(self.tab1, text="🎫 Registrar Reserva")
        self.crear_pestana_compras()

        self.tab2 = ttk.Frame(notebook)
        notebook.add(self.tab2, text="❌ Cancelar Reserva")
        self.crear_pestana_cancelaciones()

        self.tab3 = ttk.Frame(notebook)
        notebook.add(self.tab3, text="📊 Ver Reservas")
        self.crear_pestana_consultas()

    def crear_pestana_compras(self):
        f = tk.Frame(self.tab1, bg="white", padx=20, pady=20)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="Nombre del Cliente:", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        self.txt_cliente = ttk.Entry(f, width=35)
        self.txt_cliente.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(f, text="Teléfono del Cliente:", bg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        self.txt_telefono = ttk.Entry(f, width=35)
        self.txt_telefono.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(f, text="Seleccionar Función:", bg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=8)
        
        self.combo_fun = ttk.Combobox(
            f,
            values=[f"{fx.obtener_id_funcion()} - {fx.obtener_pelicula()} | {fx.obtener_sala_tipo()} | {fx.obtener_horario()}" for fx in self.manager.funciones],
            width=55,
            state="readonly",
        )
        self.combo_fun.grid(row=2, column=1, pady=8, padx=10)
        if self.manager.funciones:
            self.combo_fun.current(0)

        tk.Label(f, text="Cantidad de Entradas:", bg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        self.txt_cant = ttk.Entry(f, width=35)
        self.txt_cant.grid(row=3, column=1, pady=8, padx=10)

        tk.Button(
            f,
            text="Confirmar Reserva",
            bg="#28a745",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.procesar_compra,
        ).grid(row=4, column=0, columnspan=2, pady=25)

    def procesar_compra(self):
        nombre = self.txt_cliente.get().strip()
        telefono = self.txt_telefono.get().strip()
        cant_str = self.txt_cant.get().strip()

        try:
            if not nombre or not telefono or not cant_str:
                raise ValueError("Por favor completa todos los campos del formulario.")
            
            try:
                cant = int(cant_str)
            except ValueError:
                raise ValueError("La cantidad de entradas debe ser un número entero.")

            if cant <= 0:
                raise ValueError("La cantidad de entradas debe ser mayor a cero.")

            id_fun = self.combo_fun.get().split(" - ")[0]

            msg = self.manager.registrar_compra(nombre, telefono, id_fun, cant)
            
            messagebox.showinfo("Reserva Exitosa", msg)
            self.txt_cliente.delete(0, tk.END)
            self.txt_telefono.delete(0, tk.END)
            self.txt_cant.delete(0, tk.END)
            self.cargar_tabla()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))

    def crear_pestana_cancelaciones(self):
        f = tk.Frame(self.tab2, bg="white", padx=20, pady=20)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="Selecciona la Reserva a Cancelar:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=10)
        self.combo_reservas = ttk.Combobox(f, width=70, state="readonly")
        self.combo_reservas.pack(anchor="w", pady=10)
        self.actualizar_combos()

        tk.Button(f, text="Cancelar Reserva", bg="#dc3545", fg="white", font=("Arial", 10, "bold"), command=self.procesar_cancelacion).pack(anchor="w", pady=20)

    def actualizar_combos(self):
        activas = [
            f"{c.obtener_id_compra()} - Cliente: {c.obtener_cliente_nombre()} ({c.obtener_cliente_telefono()}) - Función: {c.obtener_id_funcion()}"
            for c in self.manager.compras if c.obtener_estado() == "ACTIVA"
        ]
        self.combo_reservas["values"] = activas
        if activas:
            self.combo_reservas.current(0)
        else:
            self.combo_reservas.set("")

    def procesar_cancelacion(self):
        sel = self.combo_reservas.get()
        try:
            if not sel:
                raise ValueError("No hay reservas seleccionadas para cancelar.")
            
            id_r = sel.split(" - ")[0]

            confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas cancelar la reserva {id_r}?")
            
            if not confirmacion:
                return 

            msg = self.manager.cancelar_compra(id_r)
            messagebox.showinfo("Éxito", msg)
            self.actualizar_combos()
            self.cargar_tabla()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def crear_pestana_consultas(self):
        f = tk.Frame(self.tab3, bg="white", padx=10, pady=10)
        f.pack(fill="both", expand=True)

        tk.Button(f, text="Actualizar Tabla", bg="#007bff", fg="white", command=self.cargar_tabla).pack(anchor="w", pady=5)

        cols = ("ID Reserva", "Cliente y Teléfono", "Información de la Película", "Entradas", "Estado")
        self.tree = ttk.Treeview(f, columns=cols, show="headings", height=12)
        
        self.tree.heading("ID Reserva", text="ID")
        self.tree.column("ID Reserva", width=70, anchor="center")
        
        self.tree.heading("Cliente y Teléfono", text="Cliente (Teléfono)")
        self.tree.column("Cliente y Teléfono", width=180)
        
        self.tree.heading("Información de la Película", text="Película | Sala | Horario")
        self.tree.column("Información de la Película", width=380)
        
        self.tree.heading("Entradas", text="Entradas")
        self.tree.column("Entradas", width=70, anchor="center")
        
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Estado", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=5)
        self.cargar_tabla()

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for c in self.manager.compras:
            funcion = next((f for f in self.manager.funciones if f.obtener_id_funcion() == c.obtener_id_funcion()), None)
            info_pelicula = f"{funcion.obtener_pelicula()} | {funcion.obtener_sala_tipo()} | {funcion.obtener_horario()}" if funcion else "Función Desconocida"
            info_cliente = f"{c.obtener_cliente_nombre()} ({c.obtener_cliente_telefono()})"
            
            self.tree.insert("", "end", values=(c.obtener_id_compra(), info_cliente, info_pelicula, c.obtener_cantidad_asientos(), c.obtener_estado()))
            
        try:
            self.actualizar_combos()
        except:
            pass

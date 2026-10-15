from modelos import Cliente, Compra, Funcion

class CineManager:
    def __init__(self):
        self.funciones = []
        self.clientes = []
        self.compras = []
        self.inicializar_datos_por_defecto()

    def inicializar_datos_por_defecto(self):
        # Datos iniciales que se cargarán cada vez que se abra el programa
        if not self.funciones:
            self.funciones.append(Funcion("F1", "Other Mommy (94 min)", "Sala 1 - 2D", "14:00", 170))
            self.funciones.append(Funcion("F2", "Tadeo el Explorador y la Lámpara Maravillosa (95 min)", "Sala 2 - 3D", "16:15", 170))
            self.funciones.append(Funcion("F3", "Avengers: Endgame (reestreno / 182 min)", "Sala 3 - 3D", "18:00", 170))
            self.funciones.append(Funcion("F4", "Coyote vs. Acme (103 min)", "Sala 4 - 2D", "20:30", 170))
            self.funciones.append(Funcion("F5", "Resident Evil (97 min)", "Sala 5 - 3D", "22:45", 170))

    def generar_id_reserva(self):
        if not self.compras:
            return "R00001"
        max_num = 0
        for compra in self.compras:
            try:
                num = int(compra.obtener_id_compra().replace("R", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
        return f"R{max_num + 1:05d}"

    def registrar_compra(self, cliente_nombre, cliente_telefono, id_funcion, cantidad):
        nombre_limpio = cliente_nombre.strip()
        if not nombre_limpio:
            raise ValueError("Debes ingresar el nombre del cliente.")
        
        if not nombre_limpio.replace(" ", "").isalpha():
            raise ValueError("El nombre del cliente es inválido. Solo debe contener letras.")

        tel_limpio = cliente_telefono.strip()
        if not tel_limpio:
            raise ValueError("Debes ingresar el teléfono del cliente.")
        if not tel_limpio.isdigit():
            raise ValueError("El teléfono es inválido. Solo puede contener números.")

        funcion = next((f for f in self.funciones if f.obtener_id_funcion() == id_funcion), None)
        if not funcion:
            raise ValueError("La función seleccionada no existe en el sistema.")

        ocupados = len(funcion.obtener_asientos_vendidos())
        
        if ocupados >= funcion.obtener_capacidad():
            raise ValueError(f"¡Aviso! Ya no hay más entradas disponibles para '{funcion.obtener_pelicula()}'. Sala LLENA.")
            
        if cantidad > 170:
            raise ValueError("No puedes reservar más de 170 sillas por transacción.")
            
        if ocupados + cantidad > funcion.obtener_capacidad():
            raise ValueError(f"Capacidad excedida. Solo quedan {funcion.obtener_capacidad() - ocupados} entradas disponibles.")

        nuevo_id = self.generar_id_reserva()
        nueva_compra = Compra(nuevo_id, nombre_limpio, tel_limpio, id_funcion, cantidad)
        
        # Se agrega a la colección en memoria
        self.compras.append(nueva_compra)

        for i in range(cantidad):
            funcion.registrar_asiento_vendido(ocupados + i + 1)

        return f"¡Éxito! Reserva registrada con el ID: {nuevo_id}"

    def cancelar_compra(self, id_compra):
        compra = next((c for c in self.compras if c.obtener_id_compra() == id_compra), None)
        
        if not compra:
            raise ValueError("La reserva solicitada no existe.")
        if compra.obtener_estado() == "CANCELADA":
            raise ValueError("Esta reserva ya se encontraba cancelada.")

        # Modifica el estado del objeto existente
        compra.actualizar_estado("CANCELADA")
        
        funcion = next((f for f in self.funciones if f.obtener_id_funcion() == compra.obtener_id_funcion()), None)
        if funcion:
            for _ in range(compra.obtener_cantidad_asientos()):
                funcion.eliminar_ultimo_asiento_vendido()

        return f"Reserva {id_compra} cancelada correctamente. Entradas liberadas."
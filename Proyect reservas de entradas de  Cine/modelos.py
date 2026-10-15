
# 3 CLASES DEL DOMINIO (ENCAPSULADAS TRADICIONAL)


class Funcion:
    def __init__(self, id_funcion, pelicula, sala_tipo, horario, capacidad=170):
        self.__id_funcion = id_funcion
        self.__pelicula = pelicula
        self.__sala_tipo = sala_tipo
        self.__horario = horario
        self.__capacidad = capacidad
        self.__asientos_vendidos = []

    # Operaciones públicas de consulta (Getters tradicionales)
    def obtener_id_funcion(self):
        return self.__id_funcion

    def obtener_pelicula(self):
        return self.__pelicula

    def obtener_sala_tipo(self):
        return self.__sala_tipo

    def obtener_horario(self):
        return self.__horario

    def obtener_capacidad(self):
        return self.__capacidad

    def obtener_asientos_vendidos(self):
        return self.__asientos_vendidos

    def registrar_asiento_vendido(self, numero_asiento):
        self.__asientos_vendidos.append(numero_asiento)

    def eliminar_ultimo_asiento_vendido(self):
        if self.__asientos_vendidos:
            self.__asientos_vendidos.pop()

    def to_dict(self):
        return {
            "id_funcion": self.__id_funcion,
            "pelicula": self.__pelicula,
            "sala_tipo": self.__sala_tipo,
            "horario": self.__horario,
            "capacidad": self.__capacidad,
            "asientos_vendidos": self.__asientos_vendidos,
        }

class Cliente:
    def __init__(self, nombre, telefono):
        self.__nombre = nombre
        self.__telefono = telefono

    def obtener_nombre(self):
        return self.__nombre

    def obtener_telefono(self):
        return self.__telefono

    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "telefono": self.__telefono,
        }
class Compra:
    def __init__(self, id_compra, cliente_nombre, cliente_telefono, id_funcion, cantidad_asientos, estado="ACTIVA"):
        self.__id_compra = id_compra
        self.__cliente_nombre = cliente_nombre
        self.__cliente_telefono = cliente_telefono  
        self.__id_funcion = id_funcion
        self.__cantidad_asientos = cantidad_asientos
        self.__estado = estado

    def obtener_id_compra(self):
        return self.__id_compra

    def obtener_cliente_nombre(self):
        return self.__cliente_nombre

    def obtener_cliente_telefono(self):
        return self.__cliente_telefono

    def obtener_id_funcion(self):
        return self.__id_funcion

    def obtener_cantidad_asientos(self):
        return self.__cantidad_asientos

    def obtener_estado(self):
        return self.__estado

    def actualizar_estado(self, nuevo_estado):
        self.__estado = nuevo_estado

    def to_dict(self):
        return {
            "id_compra": self.__id_compra,
            "cliente_nombre": self.__cliente_nombre,
            "cliente_telefono": self.__cliente_telefono,
            "id_funcion": self.__id_funcion,
            "cantidad_asientos": self.__cantidad_asientos,
            "estado": self.__estado,
        }

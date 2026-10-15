import os
from gestor import CineManager

def limpiar_pantalla():
    """Limpia la consola dependiendo del sistema operativo."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print("\n" + "="*50)
    print("🎬 PLATAFORMA DE RESERVAS DE CINE - CONSOLA 🎬")
    print("="*50)
    print("1. Registrar una nueva reserva")
    print("2. Cancelar una reserva existente")
    print("3. Ver todas las reservas")
    print("0. Salir")
    print("="*50)

def iniciar_consola():
    manager = CineManager()
    limpiar_pantalla()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        limpiar_pantalla()

        if opcion == "1":
            print("--- 🎫 REGISTRAR RESERVA ---")
            
            # 1. Ciclo infinito para el Nombre
            while True:
                try:
                    nombre = input("Ingresa el nombre del cliente (solo letras): ").strip()
                    if not nombre:
                        raise ValueError("El nombre no puede estar vacío.")
                    if not nombre.replace(" ", "").isalpha():
                        raise ValueError("Nombre inválido. Solo debe contener letras.")
                    break # Si pasa las validaciones, rompe el ciclo y sigue al teléfono
                except ValueError as e:
                    print(f"❌ Error: {e} ¡Intenta nuevamente!\n")

            # 2. Ciclo infinito para el Teléfono
            while True:
                try:
                    telefono = input("Ingresa el teléfono del cliente (solo números): ").strip()
                    if not telefono:
                        raise ValueError("El teléfono no puede estar vacío.")
                    if not telefono.isdigit():
                        raise ValueError("Teléfono inválido. Solo puede contener números.")
                    break # Si pasa las validaciones, rompe el ciclo
                except ValueError as e:
                    print(f"❌ Error: {e} ¡Intenta nuevamente!\n")
            
            # Mostrar películas
            print("\nPelículas Disponibles:")
            for f in manager.funciones:
                print(f"[{f.obtener_id_funcion()}] {f.obtener_pelicula()} | {f.obtener_sala_tipo()} | {f.obtener_horario()}")
            
            # 3. Ciclo infinito para el ID de la película
            while True:
                try:
                    id_fun = input("\nDigita el ID de la película (ej. F1, F2): ").upper().strip()
                    funcion_existe = any(f.obtener_id_funcion() == id_fun for f in manager.funciones)
                    if not funcion_existe:
                        raise ValueError(f"La función con ID '{id_fun}' no existe en el catálogo.")
                    break # Si el ID existe, avanza
                except ValueError as e:
                    print(f"❌ Error: {e} ¡Intenta nuevamente!")

            # 4. Ciclo infinito para la Cantidad de Entradas y Guardado Final
            while True:
                try:
                    cant_str = input("\n¿Cuántas entradas deseas reservar?: ").strip()
                    if not cant_str.isdigit() or int(cant_str) <= 0:
                        raise ValueError("La cantidad debe ser un número entero mayor a cero.")
                    
                    cant = int(cant_str)
                    
                    # Intentamos guardar con el Gestor (Aquí el gestor evalúa si hay capacidad)
                    msg = manager.registrar_compra(nombre, telefono, id_fun, cant)
                    
                    limpiar_pantalla()
                    print(f"✅ {msg}")
                    break # Si el gestor dice que todo está perfecto, rompe el ciclo y termina
                    
                except ValueError as e:
                    # Si el gestor detecta que no hay sillas, lo atrapamos aquí y le volvemos a preguntar
                    print(f"❌ Error del sistema: {e} ¡Intenta nuevamente con otra cantidad!")
                
            input("\nPresiona Enter para continuar...")
            limpiar_pantalla()

        elif opcion == "2":
            print("--- ❌ CANCELAR RESERVA ---")
            activas = [c for c in manager.compras if c.obtener_estado() == "ACTIVA"]
            
            if not activas:
                print("⚠️ No hay reservas activas en este momento.")
                input("\nPresiona Enter para continuar...")
                limpiar_pantalla()
                continue
            
            for c in activas:
                print(f"ID: {c.obtener_id_compra()} | Cliente: {c.obtener_cliente_nombre()} | Función: {c.obtener_id_funcion()}")
            
            while True:
                try:
                    id_r = input("\nIngresa el ID de la reserva que deseas cancelar (ej. R00001): ").upper().strip()
                    reserva_existe = any(c.obtener_id_compra() == id_r and c.obtener_estado() == "ACTIVA" for c in activas)
                    
                    if not reserva_existe:
                        raise ValueError("Ese ID no corresponde a ninguna reserva activa.")
                    break
                except ValueError as e:
                    print(f"❌ Error: {e} ¡Intenta nuevamente!")
            
            confirmacion = input(f"¿Estás seguro de que deseas cancelar la reserva {id_r}? (s/n): ").lower()
            
            limpiar_pantalla()
            if confirmacion == 's':
                try:
                    msg = manager.cancelar_compra(id_r)
                    print(f"✅ {msg}")
                except ValueError as e:
                    print(f"❌ Error: {e}")
            else:
                print("⚠️ Operación cancelada. La reserva se conserva intacta.")
                
            input("\nPresiona Enter para continuar...")
            limpiar_pantalla()

        elif opcion == "3":
            print("--- 📊 LISTADO DE RESERVAS ---")
            if not manager.compras:
                print("Todavía no hay reservas registradas.")
            else:
                for c in manager.compras:
                    funcion = next((f for f in manager.funciones if f.obtener_id_funcion() == c.obtener_id_funcion()), None)
                    nombre_peli = funcion.obtener_pelicula() if funcion else "Desconocida"
                    
                    print(f"[{c.obtener_id_compra()}] Cliente: {c.obtener_cliente_nombre()} ({c.obtener_cliente_telefono()}) | Película: {nombre_peli} | Entradas: {c.obtener_cantidad_asientos()} | Estado: {c.obtener_estado()}")
            
            input("\nPresiona Enter para volver al menú principal...")
            limpiar_pantalla()
        
        elif opcion == "0":
            print("Saliendo del sistema de consola... ¡Hasta pronto! 🍿\n")
            break
            
        else:
            print("❌ Opción inválida. Por favor, selecciona un número del menú.")
            input("\nPresiona Enter para continuar...")
            limpiar_pantalla()

if __name__ == "__main__":
    iniciar_consola()
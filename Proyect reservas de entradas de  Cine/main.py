from gestor import CineManager
from gui import CineAppGUI
from consola import iniciar_consola
import tkinter as tk

def main():
    print("¿Cómo deseas iniciar el sistema de cine?")
    print("1. Interfaz Gráfica (Ventanas y Botones)")
    print("2. Consola de Texto (Terminal)")
    
    opcion = input("Ingresa 1 o 2: ").strip()
    
    if opcion == "1":
        # Iniciar modo Gráfico
        manager = CineManager()
        root = tk.Tk()
        app = CineAppGUI(root, manager)
        root.mainloop()
    elif opcion == "2":
        # Iniciar modo Consola
        iniciar_consola()
    else:
        print("Opción no válida. Ejecuta de nuevo.")

if __name__ == "__main__":
    main()

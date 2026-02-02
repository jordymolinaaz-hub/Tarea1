import os
import subprocess

"""
Dashboard de Programación Orientada a Objetos
Permite visualizar y ejecutar scripts organizados por unidades y subcarpetas.
Autor: Jordy Molina
Curso: Programación Orientada a Objetos
"""

def mostrar_codigo(ruta_script):
    """
    Muestra el contenido del script seleccionado.
    """
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {os.path.basename(ruta_script)} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("❌ El archivo no se encontró.")
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
    return None


def ejecutar_codigo(ruta_script):
    """
    Ejecuta el script seleccionado en una nueva ventana de consola.
    """
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Linux / macOS
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"❌ Error al ejecutar el script: {e}")


def mostrar_menu():
    """
    Menú principal del dashboard.
    """
    ruta_base = os.path.dirname(__file__)

    # Se pueden agregar más unidades fácilmente
    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2',
        '3': 'Proyectos Personales'
    }

    while True:
        print("\n===== DASHBOARD PRINCIPAL =====")
        for key, value in unidades.items():
            print(f"{key} - {value}")
        print("0 - Salir")

        eleccion = input("Seleccione una opción: ")

        if eleccion == '0':
            print("👋 Saliendo del dashboard...")
            break
        elif eleccion in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion])
            mostrar_sub_menu(ruta_unidad)
        else:
            print("⚠ Opción no válida.")


def mostrar_sub_menu(ruta_unidad):
    """
    Muestra las subcarpetas de una unidad.
    """
    if not os.path.exists(ruta_unidad):
        print("⚠ La unidad no existe.")
        return

    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print("\n--- Submenú ---")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Volver al menú principal")

        opcion = input("Seleccione una subcarpeta: ")

        if opcion == '0':
            break
        try:
            index = int(opcion) - 1
            if 0 <= index < len(sub_carpetas):
                mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[index]))
            else:
                print("⚠ Opción inválida.")
        except ValueError:
            print("⚠ Ingrese un número válido.")


def mostrar_scripts(ruta_sub_carpeta):
    """
    Muestra los scripts Python disponibles en la carpeta.
    """
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta)
               if f.is_file() and f.name.endswith('.py')]

    while True:
        print("\n--- Scripts disponibles ---")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Volver")
        print("9 - Menú principal")

        opcion = input("Seleccione un script: ")

        if opcion == '0':
            break
        elif opcion == '9':
            return
        try:
            index = int(opcion) - 1
            if 0 <= index < len(scripts):
                ruta_script = os.path.join(ruta_sub_carpeta, scripts[index])
                codigo = mostrar_codigo(ruta_script)

                if codigo:
                    ejecutar = input("¿Desea ejecutar el script? (1 = Sí / 0 = No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
                    input("\nPresione Enter para continuar...")
            else:
                print("⚠ Opción inválida.")
        except ValueError:
            print("⚠ Ingrese un número válido.")


# Punto de entrada del programa
if __name__ == "__main__":
    mostrar_menu()

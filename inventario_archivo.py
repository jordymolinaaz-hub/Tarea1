"""
Autor: Jordy Molina
Asignatura: POO
Descripción:
Sistema avanzado de gestión de inventarios con base de datos SQLite.
Utiliza colecciones (dict, set, list, tuple) y persistencia en SQLite.
"""

import json
import os


# ═══════════════════════════════════════════════
# Clase Producto
# ═══════════════════════════════════════════════

class Producto:

    def __init__(self, id: int, nombre: str, cantidad: int, precio: float):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            data["id"],
            data["nombre"],
            data["cantidad"],
            data["precio"]
        )


# ═══════════════════════════════════════════════
# Clase Inventario
# ═══════════════════════════════════════════════

class Inventario:

    ARCHIVO = "inventario.json"

    def __init__(self):
        self.productos = {}      # diccionario → búsqueda rápida por ID
        self.ids = set()         # conjunto → control de IDs únicos
        self._cargar()

    # ─────────────────────────────
    # Gestión de archivo
    # ─────────────────────────────

    def _guardar(self):
        datos = [p.to_dict() for p in self.productos.values()]
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    def _cargar(self):
        if os.path.exists(self.ARCHIVO):
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    p = Producto.from_dict(item)
                    self.productos[p.id] = p
                    self.ids.add(p.id)

    # ─────────────────────────────
    # Métodos CRUD
    # ─────────────────────────────

    def agregar(self, producto):
        if producto.id in self.ids:
            return False, "El ID ya existe."

        self.productos[producto.id] = producto
        self.ids.add(producto.id)
        self._guardar()
        return True, "Producto agregado correctamente."

    def eliminar(self, id):
        if id not in self.ids:
            return False, "Producto no encontrado."

        del self.productos[id]
        self.ids.remove(id)
        self._guardar()
        return True, "Producto eliminado."

    def actualizar(self, id, cantidad, precio):
        if id not in self.ids:
            return False, "Producto no encontrado."

        self.productos[id].cantidad = cantidad
        self.productos[id].precio = precio
        self._guardar()
        return True, "Producto actualizado."

    def buscar_por_nombre(self, nombre):
        nombre = nombre.lower()
        return [
            p for p in self.productos.values()
            if nombre in p.nombre.lower()
        ]

    def mostrar_todos(self):
        return sorted(self.productos.values(), key=lambda p: p.id)


# ═══════════════════════════════════════════════
# Menú
# ═══════════════════════════════════════════════

class Menu:

    OPCIONES = (
        ("1", "Agregar producto"),
        ("2", "Eliminar producto"),
        ("3", "Actualizar producto"),
        ("4", "Buscar producto por nombre"),
        ("5", "Mostrar todos los productos"),
        ("6", "Salir"),
    )

    def __init__(self):
        self.inventario = Inventario()

    def mostrar_menu(self):
        print("\n════ SISTEMA DE INVENTARIO ════")
        for numero, texto in self.OPCIONES:
            print(f"{numero}. {texto}")
        print("══════════════════════════════")

    def ejecutar(self):

        while True:
            self.mostrar_menu()
            opcion = input("Seleccione opción: ")

            if opcion == "1":
                id_ = int(input("ID: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))

                p = Producto(id_, nombre, cantidad, precio)
                exito, msg = self.inventario.agregar(p)
                print(msg)

            elif opcion == "2":
                id_ = int(input("ID a eliminar: "))
                exito, msg = self.inventario.eliminar(id_)
                print(msg)

            elif opcion == "3":
                id_ = int(input("ID a actualizar: "))
                cantidad = int(input("Nueva cantidad: "))
                precio = float(input("Nuevo precio: "))
                exito, msg = self.inventario.actualizar(id_, cantidad, precio)
                print(msg)

            elif opcion == "4":
                nombre = input("Nombre a buscar: ")
                resultados = self.inventario.buscar_por_nombre(nombre)
                for p in resultados:
                    print(f"{p.id} | {p.nombre} | {p.cantidad} | ${p.precio}")

            elif opcion == "5":
                productos = self.inventario.mostrar_todos()
                for p in productos:
                    print(f"{p.id} | {p.nombre} | {p.cantidad} | ${p.precio}")

            elif opcion == "6":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida.")


# ═══════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar()
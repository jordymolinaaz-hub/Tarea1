"""
Autor: Jordy Molina
Asignatura: POO
Descripción:
Este programa permite gestionar un inventario de productos mediante un
menú interactivo en consola. Se pueden agregar, eliminar, actualizar,
buscar y mostrar productos.
"""


import os

ARCHIVO_INVENTARIO = "inventario.txt"


class Producto:
    """
    Clase Producto
    Representa un producto dentro del inventario.
    """

    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def actualizar(self, cantidad, precio):
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"

    def a_linea(self):
        """Serializa el producto a una línea de texto para guardar en archivo."""
        return f"{self.id},{self.nombre},{self.cantidad},{self.precio}\n"

    @staticmethod
    def desde_linea(linea):
        """Crea un Producto a partir de una línea de texto del archivo."""
        partes = linea.strip().split(",")
        if len(partes) != 4:
            raise ValueError(f"Línea con formato inválido: '{linea.strip()}'")
        id_ = int(partes[0])
        nombre = partes[1]
        cantidad = int(partes[2])
        precio = float(partes[3])
        return Producto(id_, nombre, cantidad, precio)


class Inventario:
    """
    Clase Inventario
    Gestiona la lista de productos y su persistencia en archivo.
    """

    def __init__(self, archivo=ARCHIVO_INVENTARIO):
        self.archivo = archivo
        self.productos = []
        self._cargar_desde_archivo()

    # ------------------------------------------------------------------ #
    #  Persistencia                                                        #
    # ------------------------------------------------------------------ #

    def _cargar_desde_archivo(self):
        """Carga los productos desde el archivo al iniciar el programa."""
        if not os.path.exists(self.archivo):
            # El archivo no existe: se creará vacío la primera vez que se guarde
            print(f"[INFO] Archivo '{self.archivo}' no encontrado. Se creará uno nuevo.")
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            errores = 0
            for i, linea in enumerate(lineas, start=1):
                if linea.strip() == "":
                    continue
                try:
                    producto = Producto.desde_linea(linea)
                    self.productos.append(producto)
                except ValueError as e:
                    print(f"[ADVERTENCIA] Línea {i} ignorada: {e}")
                    errores += 1

            print(f"[INFO] Inventario cargado: {len(self.productos)} producto(s)"
                  + (f", {errores} línea(s) con error ignorada(s)." if errores else "."))

        except PermissionError:
            print(f"[ERROR] Sin permiso para leer '{self.archivo}'. El inventario comenzará vacío.")
        except OSError as e:
            print(f"[ERROR] No se pudo leer '{self.archivo}': {e}. El inventario comenzará vacío.")

    def _guardar_en_archivo(self):
        """Escribe todos los productos en el archivo (sobreescritura completa)."""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for p in self.productos:
                    f.write(p.a_linea())
            return True
        except PermissionError:
            print(f"[ERROR] Sin permiso para escribir en '{self.archivo}'.")
            return False
        except OSError as e:
            print(f"[ERROR] No se pudo guardar en '{self.archivo}': {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Operaciones CRUD                                                    #
    # ------------------------------------------------------------------ #

    def agregar_producto(self, producto):
        """Agrega un producto al inventario validando que el ID sea único."""
        for p in self.productos:
            if p.id == producto.id:
                return False, "ID duplicado."

        self.productos.append(producto)

        if self._guardar_en_archivo():
            return True, "Producto agregado y guardado en archivo correctamente."
        else:
            # Se revierte la adición en memoria para mantener consistencia
            self.productos.remove(producto)
            return False, "No se pudo guardar el producto en el archivo."

    def eliminar_producto(self, id):
        """Elimina un producto del inventario por su ID."""
        for p in self.productos:
            if p.id == id:
                self.productos.remove(p)
                if self._guardar_en_archivo():
                    return True, "Producto eliminado y archivo actualizado."
                else:
                    # Revertir
                    self.productos.append(p)
                    return False, "No se pudo actualizar el archivo tras eliminar."
        return False, "Producto no encontrado."

    def actualizar_producto(self, id, cantidad, precio):
        """Actualiza la cantidad y el precio de un producto por su ID."""
        for p in self.productos:
            if p.id == id:
                cantidad_anterior = p.cantidad
                precio_anterior = p.precio
                p.actualizar(cantidad, precio)
                if self._guardar_en_archivo():
                    return True, "Producto actualizado y archivo guardado."
                else:
                    # Revertir
                    p.actualizar(cantidad_anterior, precio_anterior)
                    return False, "No se pudo guardar el archivo tras actualizar."
        return False, "Producto no encontrado."

    def buscar_por_nombre(self, nombre):
        """Busca productos cuyo nombre coincida total o parcialmente."""
        encontrados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """Muestra todos los productos del inventario."""
        if not self.productos:
            print("Inventario vacío.")
        else:
            for p in self.productos:
                print(p)


class Menu:
    """
    Clase Menu
    Controla la interacción con el usuario.
    """

    def __init__(self):
        self.inventario = Inventario()

    def mostrar_menu(self):
        print("\n=== MENÚ DE INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar inventario")
        print("6. Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.eliminar_producto()
            elif opcion == "3":
                self.actualizar_producto()
            elif opcion == "4":
                self.buscar_producto()
            elif opcion == "5":
                self.mostrar_inventario()
            elif opcion == "6":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    # ------------------------------------------------------------------ #
    #  Helpers de entrada con validación                                  #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _leer_entero(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("[ERROR] Debe ingresar un número entero válido.")

    @staticmethod
    def _leer_flotante(prompt):
        while True:
            try:
                valor = float(input(prompt))
                if valor < 0:
                    print("[ERROR] El valor no puede ser negativo.")
                else:
                    return valor
            except ValueError:
                print("[ERROR] Debe ingresar un número válido.")

    # ------------------------------------------------------------------ #
    #  Acciones del menú                                                  #
    # ------------------------------------------------------------------ #

    def agregar_producto(self):
        print("\n--- Agregar Producto ---")
        id_ = self._leer_entero("ID: ")
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("[ERROR] El nombre no puede estar vacío.")
            return
        cantidad = self._leer_entero("Cantidad: ")
        precio = self._leer_flotante("Precio: ")

        producto = Producto(id_, nombre, cantidad, precio)
        exito, mensaje = self.inventario.agregar_producto(producto)
        print(f"[{'OK' if exito else 'ERROR'}] {mensaje}")

    def eliminar_producto(self):
        print("\n--- Eliminar Producto ---")
        id_ = self._leer_entero("ID del producto a eliminar: ")
        exito, mensaje = self.inventario.eliminar_producto(id_)
        print(f"[{'OK' if exito else 'ERROR'}] {mensaje}")

    def actualizar_producto(self):
        print("\n--- Actualizar Producto ---")
        id_ = self._leer_entero("ID del producto: ")
        cantidad = self._leer_entero("Nueva cantidad: ")
        precio = self._leer_flotante("Nuevo precio: ")
        exito, mensaje = self.inventario.actualizar_producto(id_, cantidad, precio)
        print(f"[{'OK' if exito else 'ERROR'}] {mensaje}")

    def buscar_producto(self):
        print("\n--- Buscar Producto ---")
        nombre = input("Nombre a buscar: ").strip()
        self.inventario.buscar_por_nombre(nombre)

    def mostrar_inventario(self):
        print("\n--- Inventario Completo ---")
        self.inventario.mostrar_todos()


# Punto de entrada del programa
if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar()
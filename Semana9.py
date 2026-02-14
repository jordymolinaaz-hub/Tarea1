"""
Autor: Jordy Molina
Asignatura: POO
Descripción:
Este programa permite gestionar un inventario de productos mediante un
menú interactivo en consola. Se pueden agregar, eliminar, actualizar,
buscar y mostrar productos.
"""


class Producto:
    """
    Clase Producto
    Representa un producto dentro del inventario.
    """

    def __init__(self, id, nombre, cantidad, precio):
        """
        Constructor de la clase Producto
        :param id: Identificador único del producto
        :param nombre: Nombre del producto
        :param cantidad: Cantidad disponible
        :param precio: Precio del producto
        """
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def actualizar(self, cantidad, precio):
        """
        Actualiza la cantidad y el precio del producto
        """
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        """
        Retorna la información del producto en formato texto
        """
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio}"


class Inventario:
    """
    Clase Inventario
    Gestiona la lista de productos
    """

    def __init__(self):
        """
        Constructor de la clase Inventario
        """
        self.productos = []

    def agregar_producto(self, producto):
        """
        Agrega un producto al inventario validando que el ID sea único
        """
        for p in self.productos:
            if p.id == producto.id:
                return False
        self.productos.append(producto)
        return True

    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario por su ID
        """
        for p in self.productos:
            if p.id == id:
                self.productos.remove(p)
                return True
        return False

    def actualizar_producto(self, id, cantidad, precio):
        """
        Actualiza la cantidad y el precio de un producto por su ID
        """
        for p in self.productos:
            if p.id == id:
                p.actualizar(cantidad, precio)
                return True
        return False

    def buscar_por_nombre(self, nombre):
        """
        Busca productos cuyo nombre coincida total o parcialmente
        """
        encontrado = False
        for p in self.productos:
            if nombre.lower() in p.nombre.lower():
                print(p)
                encontrado = True
        if not encontrado:
            print("No se encontraron productos.")

    def mostrar_todos(self):
        """
        Muestra todos los productos del inventario
        """
        if not self.productos:
            print("Inventario vacío.")
        else:
            for p in self.productos:
                print(p)


class Menu:
    """
    Clase Menu
    Controla la interacción con el usuario
    """

    def __init__(self):
        """
        Constructor de la clase Menu
        """
        self.inventario = Inventario()

    def mostrar_menu(self):
        """
        Muestra las opciones del menú
        """
        print("\n=== MENÚ DE INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar inventario")
        print("6. Salir")

    def ejecutar(self):
        """
        Ejecuta el menú principal
        """
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

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
                print("Opción inválida.")

    def agregar_producto(self):
        """
        Solicita datos y agrega un producto
        """
        id = int(input("ID: "))
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))

        producto = Producto(id, nombre, cantidad, precio)
        if self.inventario.agregar_producto(producto):
            print("Producto agregado correctamente.")
        else:
            print("Error: ID duplicado.")

    def eliminar_producto(self):
        """
        Elimina un producto por ID
        """
        id = int(input("ID del producto a eliminar: "))
        if self.inventario.eliminar_producto(id):
            print("Producto eliminado.")
        else:
            print("Producto no encontrado.")

    def actualizar_producto(self):
        """
        Actualiza un producto existente
        """
        id = int(input("ID del producto: "))
        cantidad = int(input("Nueva cantidad: "))
        precio = float(input("Nuevo precio: "))

        if self.inventario.actualizar_producto(id, cantidad, precio):
            print("Producto actualizado.")
        else:
            print("Producto no encontrado.")

    def buscar_producto(self):
        """
        Busca productos por nombre
        """
        nombre = input("Nombre a buscar: ")
        self.inventario.buscar_por_nombre(nombre)

    def mostrar_inventario(self):
        """
        Muestra todos los productos
        """
        self.inventario.mostrar_todos()


# Punto de entrada del programa
if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar()

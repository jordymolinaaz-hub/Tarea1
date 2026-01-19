"""
Programa: Sistema de Gestión de Biblioteca
Autor: Jordy Molina
Descripción:
Este programa simula una biblioteca básica utilizando
los conceptos de herencia, encapsulación
y polimorfismo.
"""

class MaterialBiblioteca:

    def __init__(self, titulo, codigo):
        # Encapsulación: atributos privados
        self.__titulo = titulo
        self.__codigo = codigo

    # Métodos getters
    def get_titulo(self):
        """Devuelve el título del material."""
        return self.__titulo

    def get_codigo(self):
        """Devuelve el código del material."""
        return self.__codigo

    def calcular_multa(self, dias_retraso):
        """
        Método genérico que será sobrescrito.
        Ejemplo de polimorfismo.
        """
        return 0

    def mostrar_info(self):
        """Muestra la información básica del material."""
        return f"Título: {self.__titulo} | Código: {self.__codigo}"


# ==================================
# Clase derivada: Libro
# ==================================
class Libro(MaterialBiblioteca):
    """
    Representa un libro dentro de la biblioteca.
    """

    def __init__(self, titulo, codigo, autor):
        super().__init__(titulo, codigo)
        self.autor = autor

    def calcular_multa(self, dias_retraso):
        """
        Polimorfismo:
        Multa por retraso de libros: $0.50 por día
        """
        return dias_retraso * 0.50


# ==================================
# Clase derivada: Revista
# ==================================
class Revista(MaterialBiblioteca):
    """
    Representa una revista dentro de la biblioteca.
    """

    def __init__(self, titulo, codigo, numero_edicion):
        super().__init__(titulo, codigo)
        self.numero_edicion = numero_edicion

    def calcular_multa(self, dias_retraso):
        """
        Polimorfismo:
        Multa por retraso de revistas: $0.30 por día
        """
        return dias_retraso * 0.30


# ==================================
# Programa principal
# ==================================
if __name__ == "__main__":
    """
    Creación de objetos y demostración del polimorfismo
    """

    # Instancias de materiales
    libro1 = Libro("Cien años de soledad", "L001", "Gabriel García Márquez")
    revista1 = Revista("National Geographic", "R101", 245)

    materiales = [libro1, revista1]

    dias_retraso = 4

    # Uso polimórfico del método calcular_multa
    for material in materiales:
        print(material.mostrar_info())
        print(f"Multa por {dias_retraso} días de retraso: "
              f"${material.calcular_multa(dias_retraso)}")
        print("-" * 45)

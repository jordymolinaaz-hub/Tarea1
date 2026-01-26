class Libro:
    """
    Nombre: Jordy Molina
    Tema: Constructores y Destructores

    Clase que representa un libro físico en la biblioteca.
    Maneja la información básica y el estado de préstamo de los libros.
    """

    def __init__(self, codigo, titulo, autor, paginas):
        """
        Inicializa un nuevo libro con sus datos básicos.

        Args:
            codigo (int): Identificador único del libro
            titulo (str): Título del libro
            autor (str): Nombre del autor
            paginas (int): Número de páginas
        """
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.prestado = False
        print(f"Libro '{self.titulo}' registrado en la biblioteca")

    def mostrar_info(self):
        """Muestra toda la información del libro incluyendo su estado."""
        estado = "Prestado" if self.prestado else "Disponible"
        print(f"Código: {self.codigo}")
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Páginas: {self.paginas}")
        print(f"Estado: {estado}")

    def prestar(self):
        """Registra el préstamo del libro si está disponible."""
        if not self.prestado:
            self.prestado = True
            print(f"El libro '{self.titulo}' ha sido prestado")
        else:
            print(f"El libro '{self.titulo}' ya está prestado")

    def devolver(self):
        """Registra la devolución del libro si estaba prestado."""
        if self.prestado:
            self.prestado = False
            print(f"El libro '{self.titulo}' ha sido devuelto")
        else:
            print(f"El libro '{self.titulo}' no estaba prestado")

    def __del__(self):
        print(f"Libro '{self.titulo}' eliminado del sistema")


class LibroDigital(Libro):
    """
    Clase que representa un libro digital.
    Hereda de Libro y añade características de archivos digitales.
    """

    def __init__(self, codigo, titulo, autor, paginas, formato, tamaño_mb):
        """
        Inicializa un libro digital con información del archivo.

        Args:
            formato (str): Formato del archivo (PDF, EPUB, etc.)
            tamaño_mb (float): Tamaño del archivo en megabytes
        """
        super().__init__(codigo, titulo, autor, paginas)
        self.formato = formato
        self.tamaño_mb = tamaño_mb

    def mostrar_info(self):
        """Muestra información del libro digital incluyendo formato y tamaño."""
        super().mostrar_info()
        print(f"Formato: {self.formato}")
        print(f"Tamaño: {self.tamaño_mb}MB")

    def descargar(self):
        """Simula la descarga del archivo digital."""
        print(f"Descargando '{self.titulo}' ({self.tamaño_mb}MB)...")

    def __del__(self):
        print(f"Libro digital '{self.titulo}' eliminado del sistema")


if __name__ == "__main__":
    print("=== Inicio del Sistema de Biblioteca ===\n")

    libro1 = Libro(101, "Cien Años de Soledad", "Gabriel García Márquez", 471)
    libro2 = Libro(102, "Don Quijote de la Mancha", "Miguel de Cervantes", 863)
    libro3 = Libro(103, "1984", "George Orwell", 328)
    libro_digital = LibroDigital(201, "El Principito", "Antoine de Saint-Exupéry", 96, "PDF", 2.5)

    print("\n=== Información de libros ===")
    libro1.mostrar_info()
    print("------------------------")
    libro2.mostrar_info()
    print("------------------------")
    libro3.mostrar_info()
    print("------------------------")
    libro_digital.mostrar_info()

    print("\n=== Préstamos y devoluciones ===")
    libro1.prestar()
    libro2.prestar()
    libro1.devolver()

    print("\n=== Descarga de libro digital ===")
    libro_digital.descargar()

    print("\n=== Finalizando sistema ===")
    del libro1
    del libro2
    del libro3
    del libro_digital

    print("\n=== Biblioteca cerrada ===")
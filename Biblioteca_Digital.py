# ============================================================
# SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL
# ============================================================
# Estructura de datos utilizada:
#   - Tuplas:       atributos inmutables del libro (título, autor)
#   - Diccionarios: catálogo de libros indexado por ISBN
#   - Conjuntos:    IDs de usuario únicos
#   - Listas:       libros prestados por usuario
# ============================================================


# ──────────────────────────────────────────────
# CLASE: Libro
# ──────────────────────────────────────────────
class Libro:
    """
    Representa un libro de la biblioteca.

    Se usa una TUPLA para (titulo, autor) porque son datos
    inmutables: una vez publicado el libro, esos valores no cambian.
    """

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):
        # Tupla inmutable: garantiza que título y autor no se modifiquen
        self._info_inmutable = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn
        self.disponible = True          # True = en estante, False = prestado

    # Propiedades para acceder cómodamente a los datos de la tupla
    @property
    def titulo(self) -> str:
        return self._info_inmutable[0]

    @property
    def autor(self) -> str:
        return self._info_inmutable[1]

    def __str__(self) -> str:
        estado = "✅ Disponible" if self.disponible else "📤 Prestado"
        return (f"[{self.isbn}] '{self.titulo}' — {self.autor} "
                f"| Categoría: {self.categoria} | {estado}")


# ──────────────────────────────────────────────
# CLASE: Usuario
# ──────────────────────────────────────────────
class Usuario:
    """
    Representa a un usuario registrado en la biblioteca.

    Se usa una LISTA para libros_prestados porque el conjunto
    de libros prestados cambia con frecuencia (préstamos/devoluciones).
    """

    def __init__(self, nombre: str, id_usuario: str):
        self.nombre = nombre
        self.id_usuario = id_usuario
        # Lista mutable: refleja los cambios en los préstamos activos
        self.libros_prestados: list[Libro] = []

    def __str__(self) -> str:
        n = len(self.libros_prestados)
        return f"Usuario [{self.id_usuario}]: {self.nombre} | Libros en préstamo: {n}"


# ──────────────────────────────────────────────
# CLASE: Biblioteca
# ──────────────────────────────────────────────
class Biblioteca:
    """
    Gestiona el catálogo, los usuarios y los préstamos.

    Estructuras internas:
      - catalogo (dict):    {isbn: Libro}  → búsqueda O(1) por ISBN
      - usuarios (dict):    {id: Usuario}  → acceso directo por ID
      - ids_registrados (set): IDs únicos → evita duplicados
      - historial (list):   registro de todas las operaciones
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        # DICCIONARIO: clave=ISBN, valor=objeto Libro
        self.catalogo: dict[str, Libro] = {}
        # DICCIONARIO: clave=id_usuario, valor=objeto Usuario
        self.usuarios: dict[str, Usuario] = {}
        # CONJUNTO: garantiza IDs únicos, O(1) para comprobación
        self.ids_registrados: set[str] = set()
        # Historial de operaciones
        self.historial: list[str] = []

    # ── Registro de operaciones ──────────────────
    def _registrar(self, mensaje: str):
        """Guarda un evento en el historial interno."""
        self.historial.append(mensaje)
        print(f"  ✔ {mensaje}")

    # ════════════════════════════════════════════
    # GESTIÓN DE LIBROS
    # ════════════════════════════════════════════

    def agregar_libro(self, libro: Libro) -> bool:
        """Añade un libro al catálogo usando su ISBN como clave."""
        if libro.isbn in self.catalogo:
            print(f"  ⚠ El ISBN {libro.isbn} ya existe en el catálogo.")
            return False
        self.catalogo[libro.isbn] = libro
        self._registrar(f"Libro agregado: '{libro.titulo}' (ISBN: {libro.isbn})")
        return True

    def quitar_libro(self, isbn: str) -> bool:
        """Elimina un libro del catálogo solo si no está prestado."""
        if isbn not in self.catalogo:
            print(f"  ⚠ ISBN {isbn} no encontrado.")
            return False
        libro = self.catalogo[isbn]
        if not libro.disponible:
            print(f"  ⚠ '{libro.titulo}' está prestado y no puede eliminarse.")
            return False
        del self.catalogo[isbn]
        self._registrar(f"Libro eliminado: '{libro.titulo}' (ISBN: {isbn})")
        return True

    # ════════════════════════════════════════════
    # GESTIÓN DE USUARIOS
    # ════════════════════════════════════════════

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un usuario nuevo.
        El CONJUNTO ids_registrados asegura que no haya IDs duplicados.
        """
        if usuario.id_usuario in self.ids_registrados:
            print(f"  ⚠ ID '{usuario.id_usuario}' ya está en uso.")
            return False
        self.ids_registrados.add(usuario.id_usuario)    # O(1) en conjunto
        self.usuarios[usuario.id_usuario] = usuario
        self._registrar(f"Usuario registrado: {usuario.nombre} (ID: {usuario.id_usuario})")
        return True

    def dar_de_baja_usuario(self, id_usuario: str) -> bool:
        """Da de baja a un usuario solo si no tiene libros pendientes."""
        if id_usuario not in self.ids_registrados:
            print(f"  ⚠ Usuario '{id_usuario}' no encontrado.")
            return False
        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            titulos = ", ".join(f"'{l.titulo}'" for l in usuario.libros_prestados)
            print(f"  ⚠ {usuario.nombre} tiene libros pendientes: {titulos}")
            return False
        self.ids_registrados.discard(id_usuario)        # O(1) en conjunto
        del self.usuarios[id_usuario]
        self._registrar(f"Usuario dado de baja: {usuario.nombre} (ID: {id_usuario})")
        return True

    # ════════════════════════════════════════════
    # PRÉSTAMOS Y DEVOLUCIONES
    # ════════════════════════════════════════════

    def prestar_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Presta un libro disponible a un usuario registrado.
        Actualiza tanto el estado del libro como la lista del usuario.
        """
        # Validaciones
        if isbn not in self.catalogo:
            print(f"  ⚠ Libro con ISBN {isbn} no existe.")
            return False
        if id_usuario not in self.ids_registrados:
            print(f"  ⚠ Usuario '{id_usuario}' no registrado.")
            return False

        libro = self.catalogo[isbn]
        usuario = self.usuarios[id_usuario]

        if not libro.disponible:
            print(f"  ⚠ '{libro.titulo}' no está disponible actualmente.")
            return False

        # Actualizar estado
        libro.disponible = False
        usuario.libros_prestados.append(libro)          # append O(1) en lista
        self._registrar(f"Préstamo: '{libro.titulo}' → {usuario.nombre}")
        return True

    def devolver_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Registra la devolución de un libro por parte de un usuario.
        Busca y elimina el libro de la lista del usuario.
        """
        if isbn not in self.catalogo:
            print(f"  ⚠ Libro con ISBN {isbn} no existe.")
            return False
        if id_usuario not in self.ids_registrados:
            print(f"  ⚠ Usuario '{id_usuario}' no registrado.")
            return False

        libro = self.catalogo[isbn]
        usuario = self.usuarios[id_usuario]

        # Buscar el libro en la lista de préstamos del usuario
        if libro not in usuario.libros_prestados:
            print(f"  ⚠ {usuario.nombre} no tiene '{libro.titulo}' en préstamo.")
            return False

        usuario.libros_prestados.remove(libro)          # eliminar de la lista
        libro.disponible = True
        self._registrar(f"Devolución: '{libro.titulo}' ← {usuario.nombre}")
        return True

    # ════════════════════════════════════════════
    # BÚSQUEDAS
    # ════════════════════════════════════════════

    def buscar_por_titulo(self, texto: str) -> list[Libro]:
        """Busca libros cuyo título contenga el texto (sin distinción de mayúsculas)."""
        texto = texto.lower()
        return [l for l in self.catalogo.values() if texto in l.titulo.lower()]

    def buscar_por_autor(self, texto: str) -> list[Libro]:
        """Busca libros por nombre de autor (parcial, sin distinción de mayúsculas)."""
        texto = texto.lower()
        return [l for l in self.catalogo.values() if texto in l.autor.lower()]

    def buscar_por_categoria(self, categoria: str) -> list[Libro]:
        """Busca libros que pertenezcan a una categoría específica."""
        categoria = categoria.lower()
        return [l for l in self.catalogo.values() if categoria in l.categoria.lower()]

    # ════════════════════════════════════════════
    # REPORTES
    # ════════════════════════════════════════════

    def listar_prestamos_usuario(self, id_usuario: str):
        """Muestra todos los libros actualmente prestados a un usuario."""
        if id_usuario not in self.ids_registrados:
            print(f"  ⚠ Usuario '{id_usuario}' no encontrado.")
            return
        usuario = self.usuarios[id_usuario]
        print(f"\n📚 Libros prestados a {usuario.nombre}:")
        if not usuario.libros_prestados:
            print("   (ninguno)")
        else:
            for libro in usuario.libros_prestados:
                print(f"   • {libro}")

    def mostrar_catalogo(self):
        """Imprime el catálogo completo de la biblioteca."""
        print(f"\n📖 Catálogo de '{self.nombre}' ({len(self.catalogo)} libros):")
        for libro in self.catalogo.values():
            print(f"   • {libro}")

    def mostrar_historial(self):
        """Imprime el historial de operaciones."""
        print(f"\n🗂 Historial de operaciones ({len(self.historial)} eventos):")
        for i, evento in enumerate(self.historial, 1):
            print(f"   {i:02d}. {evento}")


# ============================================================
# MENÚ INTERACTIVO
# ============================================================

def pausar():
    input("\n  Presiona Enter para continuar...")

def mostrar_menu():
    print("\n" + "═" * 50)
    print("   📚 BIBLIOTECA DIGITAL — MENÚ PRINCIPAL")
    print("═" * 50)
    print("  LIBROS")
    print("   1. Agregar libro")
    print("   2. Eliminar libro")
    print("   3. Ver catálogo completo")
    print("   4. Buscar libro")
    print()
    print("  USUARIOS")
    print("   5. Registrar usuario")
    print("   6. Dar de baja usuario")
    print("   7. Ver usuarios registrados")
    print()
    print("  PRÉSTAMOS")
    print("   8. Prestar libro")
    print("   9. Devolver libro")
    print("  10. Ver libros prestados a un usuario")
    print()
    print("  OTROS")
    print("  11. Ver historial de operaciones")
    print("   0. Salir")
    print("═" * 50)


def menu_buscar(bib: "Biblioteca"):
    print("\n  Buscar por:")
    print("   1. Título")
    print("   2. Autor")
    print("   3. Categoría")
    opcion = input("  Opción: ").strip()
    texto = input("  Ingresa el texto a buscar: ").strip()

    if opcion == "1":
        resultados = bib.buscar_por_titulo(texto)
    elif opcion == "2":
        resultados = bib.buscar_por_autor(texto)
    elif opcion == "3":
        resultados = bib.buscar_por_categoria(texto)
    else:
        print("  ⚠ Opción inválida.")
        return

    print(f"\n  🔍 Resultados ({len(resultados)}):")
    if not resultados:
        print("   (sin resultados)")
    for l in resultados:
        print(f"   • {l}")


if __name__ == "__main__":

    # Crear biblioteca con datos de ejemplo precargados
    bib = Biblioteca("Biblioteca Nacional Digital")

    # Libros iniciales
    for libro in [
        Libro("Cien años de soledad",     "Gabriel García Márquez",  "Ficción",  "ISBN-001"),
        Libro("1984",                     "George Orwell",           "Distopía", "ISBN-002"),
        Libro("El principito",            "Antoine de Saint-Exupéry","Infantil", "ISBN-003"),
        Libro("Sapiens",                  "Yuval Noah Harari",       "Historia", "ISBN-004"),
        Libro("Don Quijote de la Mancha", "Miguel de Cervantes",     "Ficción",  "ISBN-005"),
    ]:
        bib.agregar_libro(libro)

    # Usuarios iniciales
    for u in [
        Usuario("Ana García",   "U001"),
        Usuario("Carlos López", "U002"),
    ]:
        bib.registrar_usuario(u)

    print("\n  ✅ Sistema iniciado con datos de ejemplo.")

    # ── Bucle principal del menú ─────────────────
    while True:
        mostrar_menu()
        opcion = input("  Elige una opción: ").strip()

        # ── LIBROS ──────────────────────────────
        if opcion == "1":
            print("\n  ── Agregar libro ──")
            titulo    = input("  Título:    ").strip()
            autor     = input("  Autor:     ").strip()
            categoria = input("  Categoría: ").strip()
            isbn      = input("  ISBN:      ").strip()
            bib.agregar_libro(Libro(titulo, autor, categoria, isbn))
            pausar()

        elif opcion == "2":
            print("\n  ── Eliminar libro ──")
            bib.mostrar_catalogo()
            isbn = input("\n  ISBN del libro a eliminar: ").strip()
            bib.quitar_libro(isbn)
            pausar()

        elif opcion == "3":
            bib.mostrar_catalogo()
            pausar()

        elif opcion == "4":
            menu_buscar(bib)
            pausar()

        # ── USUARIOS ────────────────────────────
        elif opcion == "5":
            print("\n  ── Registrar usuario ──")
            nombre = input("  Nombre:     ").strip()
            id_u   = input("  ID usuario: ").strip()
            bib.registrar_usuario(Usuario(nombre, id_u))
            pausar()

        elif opcion == "6":
            print("\n  ── Dar de baja usuario ──")
            id_u = input("  ID usuario: ").strip()
            bib.dar_de_baja_usuario(id_u)
            pausar()

        elif opcion == "7":
            print(f"\n  👥 Usuarios registrados ({len(bib.usuarios)}):")
            if not bib.usuarios:
                print("   (ninguno)")
            for u in bib.usuarios.values():
                print(f"   • {u}")
            pausar()

        # ── PRÉSTAMOS ───────────────────────────
        elif opcion == "8":
            print("\n  ── Prestar libro ──")
            bib.mostrar_catalogo()
            isbn = input("\n  ISBN del libro: ").strip()
            id_u = input("  ID del usuario: ").strip()
            bib.prestar_libro(isbn, id_u)
            pausar()

        elif opcion == "9":
            print("\n  ── Devolver libro ──")
            id_u = input("  ID del usuario: ").strip()
            bib.listar_prestamos_usuario(id_u)
            isbn = input("\n  ISBN del libro a devolver: ").strip()
            bib.devolver_libro(isbn, id_u)
            pausar()

        elif opcion == "10":
            print("\n  ── Libros prestados ──")
            id_u = input("  ID del usuario: ").strip()
            bib.listar_prestamos_usuario(id_u)
            pausar()

        # ── OTROS ───────────────────────────────
        elif opcion == "11":
            bib.mostrar_historial()
            pausar()

        elif opcion == "0":
            print("\n  👋 ¡Hasta luego!\n")
            break

        else:
            print("  ⚠ Opción no válida. Intenta de nuevo.")
            pausar()
# ============================================
#          CLASE PADRE: Usuario
# ============================================

class Usuario:
    def __init__(self, nombre, edad):
        # ENCAPSULAMIENTO: datos protegidos
        self._nombre = nombre
        self._edad = edad

    # Método general (abstracción)
    def descripcion(self):
        return f"Usuario: {self._nombre} ({self._edad} años)"


# ============================================
#          HERENCIA: Programador y Admin
# ============================================

class Programador(Usuario):
    def __init__(self, nombre, edad, lenguaje):
        # Llamamos al constructor del padre
        super().__init__(nombre, edad)
        self.lenguaje = lenguaje

    # POLIMORFISMO: redefinir descripcion()
    def descripcion(self):
        return (f"Programador: {self._nombre} ({self._edad} años) "
                f"- Lenguaje principal: {self.lenguaje}")


class Administrador(Usuario):
    def __init__(self, nombre, edad, nivel_acceso):
        super().__init__(nombre, edad)
        self.nivel_acceso = nivel_acceso

    # Polimorfismo nuevamente
    def descripcion(self):
        return (f"Administrador: {self._nombre} ({self._edad} años) "
                f"- Nivel de acceso: {self.nivel_acceso}")


# ============================================
#       PROGRAMA PRINCIPAL
# ============================================

u1 = Usuario("Carlos", 25)
p1 = Programador("María", 30, "Python")
a1 = Administrador("Luis", 40, "Alto")

print(u1.descripcion())  # método del padre
print(p1.descripcion())  # polimorfismo
print(a1.descripcion())  # polimorfismo

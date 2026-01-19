"""
Programa: Calculadora de Gastos Mensuales (POO)
Autor: Jordy Molina
Fecha: 11 de enero de 2026
Descripción: Programa que calcula y analiza gastos mensuales utilizando
             Programación Orientada a Objetos (clases y objetos).
"""


class Validador:
    """
    Clase para validar entradas del usuario
    """

    @staticmethod
    def validar_numero(valor, nombre_campo="valor"):
        """
        Valida que el valor sea un número positivo

        Parámetros:
        valor (string): Valor a validar
        nombre_campo (string): Nombre del campo para mensajes

        Retorna:
        tuple: (boolean, float) - Es válido y número convertido
        """
        try:
            numero = float(valor)
            if numero >= 0:
                return True, numero
            else:
                print(f"Error: {nombre_campo} debe ser positivo o cero.")
                return False, 0
        except ValueError:
            print(f"Error: {nombre_campo} debe ser un número válido.")
            return False, 0


class CategoriaGasto:
    """
    Clase que representa una categoría de gasto
    """

    def __init__(self, nombre, monto):
        """
        Constructor de la categoría de gasto

        Parámetros:
        nombre (string): Nombre de la categoría
        monto (float): Monto gastado en la categoría
        """
        self.nombre = nombre
        self.monto = monto

    def calcular_porcentaje(self, total):
        """
        Calcula el porcentaje que representa del total

        Parámetros:
        total (float): Total de gastos

        Retorna:
        float: Porcentaje de esta categoría
        """
        if total > 0:
            return (self.monto / total) * 100
        return 0

    def mostrar_informacion(self, total):
        """
        Muestra la información de la categoría

        Parámetros:
        total (float): Total de gastos para calcular porcentaje
        """
        porcentaje = self.calcular_porcentaje(total)
        print(f"{self.nombre:20} ${self.monto:8.2f} ({porcentaje:5.1f}%)")


class Usuario:
    """
    Clase que representa un usuario con sus ingresos
    """

    def __init__(self, nombre, ingresos_mensuales):
        """
        Constructor del usuario

        Parámetros:
        nombre (string): Nombre del usuario
        ingresos_mensuales (float): Ingresos mensuales del usuario
        """
        self.nombre = nombre
        self.ingresos_mensuales = ingresos_mensuales

    def mostrar_informacion(self):
        """
        Muestra la información básica del usuario
        """
        print(f"Usuario: {self.nombre}")
        print(f"Ingresos mensuales: ${self.ingresos_mensuales:.2f}")


class PresupuestoMensual:
    """
    Clase principal que gestiona el presupuesto mensual
    """

    def __init__(self, usuario):
        """
        Constructor del presupuesto

        Parámetros:
        usuario (Usuario): Objeto Usuario que posee este presupuesto
        """
        self.usuario = usuario
        self.categorias = []  # Lista de objetos CategoriaGasto

    def agregar_categoria(self, categoria):
        """
        Agrega una categoría de gasto al presupuesto

        Parámetros:
        categoria (CategoriaGasto): Categoría a agregar
        """
        self.categorias.append(categoria)

    def calcular_total_gastos(self):
        """
        Calcula el total de todos los gastos

        Retorna:
        float: Suma de todos los gastos
        """
        total = 0
        for categoria in self.categorias:
            total += categoria.monto
        return total

    def calcular_saldo(self):
        """
        Calcula el dinero restante (ingresos - gastos)

        Retorna:
        float: Dinero restante o déficit
        """
        total_gastos = self.calcular_total_gastos()
        return self.usuario.ingresos_mensuales - total_gastos

    def esta_ahorrando(self):
        """
        Determina si el usuario está ahorrando

        Retorna:
        boolean: True si ahorra, False si no
        """
        return self.calcular_saldo() > 0

    def obtener_categoria_mayor_gasto(self):
        """
        Encuentra la categoría con mayor gasto

        Retorna:
        CategoriaGasto: Categoría con el monto más alto
        """
        if not self.categorias:
            return None

        categoria_maxima = self.categorias[0]
        for categoria in self.categorias:
            if categoria.monto > categoria_maxima.monto:
                categoria_maxima = categoria

        return categoria_maxima

    def calcular_porcentaje_ahorro(self):
        """
        Calcula el porcentaje de ahorro respecto a los ingresos

        Retorna:
        float: Porcentaje de ahorro
        """
        saldo = self.calcular_saldo()
        if self.usuario.ingresos_mensuales > 0:
            return (saldo / self.usuario.ingresos_mensuales) * 100
        return 0

    def mostrar_resumen(self):
        """
        Muestra el resumen completo del presupuesto
        """
        total_gastos = self.calcular_total_gastos()
        saldo = self.calcular_saldo()

        print("\n" + "=" * 60)
        print(f"RESUMEN DE GASTOS - {self.usuario.nombre.upper()}")
        print("=" * 60)

        print(f"\nIngresos mensuales: ${self.usuario.ingresos_mensuales:.2f}")

        print(f"\n{'CATEGORÍA':<20} {'MONTO':>8}  {'%':>5}")
        print("-" * 60)

        # Mostrar cada categoría
        for categoria in self.categorias:
            categoria.mostrar_informacion(total_gastos)

        print("-" * 60)
        print(f"{'TOTAL GASTOS':<20} ${total_gastos:8.2f}")
        print(f"{'SALDO':<20} ${saldo:8.2f}")

        # Análisis de ahorro o déficit
        if self.esta_ahorrando():
            print("\n✅ ¡Felicidades! Estás ahorrando dinero este mes.")
            porcentaje = self.calcular_porcentaje_ahorro()
            print(f"   Estás ahorrando el {porcentaje:.1f}% de tus ingresos.")
        else:
            print("\n⚠️  Atención: Estás gastando más de lo que ganas.")
            deficit = abs(saldo)
            print(f"   Déficit: ${deficit:.2f}")

        # Mostrar mayor gasto
        categoria_mayor = self.obtener_categoria_mayor_gasto()
        if categoria_mayor:
            print(f"\nTu mayor gasto es: {categoria_mayor.nombre} (${categoria_mayor.monto:.2f})")

        print("\n" + "=" * 60 + "\n")


class AplicacionGastos:
    """
    Clase principal que controla la aplicación
    """

    def __init__(self):
        """
        Constructor de la aplicación
        """
        self.validador = Validador()
        self.presupuesto = None

    def mostrar_titulo(self):
        """
        Muestra el título de la aplicación
        """
        print("\n" + "=" * 60)
        print("💰 CALCULADORA DE GASTOS MENSUALES - POO")
        print("=" * 60 + "\n")

    def solicitar_datos_usuario(self):
        """
        Solicita y crea el objeto Usuario con sus datos

        Retorna:
        Usuario: Objeto usuario creado o None si hay error
        """
        nombre = input("¿Cuál es tu nombre? ").strip()

        if not nombre:
            print("Error: Debes ingresar un nombre.")
            return None

        ingresos_input = input(f"\nHola {nombre}, ¿cuál es tu ingreso mensual? $")
        es_valido, ingresos = self.validador.validar_numero(ingresos_input, "Ingreso mensual")

        if not es_valido:
            return None

        # Crear y retornar objeto Usuario
        return Usuario(nombre, ingresos)

    def solicitar_categorias(self):
        """
        Solicita las categorías de gastos al usuario

        Retorna:
        list: Lista de objetos CategoriaGasto
        """
        categorias = []
        nombres_categorias = ["Alquiler/Vivienda", "Comida", "Transporte", "Entretenimiento"]

        print("\n--- Ingresa tus gastos mensuales ---")

        for nombre_categoria in nombres_categorias:
            monto_input = input(f"{nombre_categoria}: $")
            es_valido, monto = self.validador.validar_numero(monto_input, nombre_categoria)

            if not es_valido:
                return None

            # Crear objeto CategoriaGasto y agregarlo a la lista
            categoria = CategoriaGasto(nombre_categoria, monto)
            categorias.append(categoria)

        return categorias

    def ejecutar(self):
        """
        Método principal que ejecuta toda la aplicación
        """
        self.mostrar_titulo()

        # Crear usuario
        usuario = self.solicitar_datos_usuario()
        if not usuario:
            print("Programa terminado por entrada inválida.")
            return

        # Crear presupuesto para el usuario
        self.presupuesto = PresupuestoMensual(usuario)

        # Solicitar categorías de gastos
        categorias = self.solicitar_categorias()
        if not categorias:
            print("Programa terminado por entrada inválida.")
            return

        # Agregar cada categoría al presupuesto
        for categoria in categorias:
            self.presupuesto.agregar_categoria(categoria)

        # Mostrar resumen completo
        self.presupuesto.mostrar_resumen()


def main():
    """
    Función principal que inicia la aplicación
    """
    # Crear instancia de la aplicación
    app = AplicacionGastos()

    # Ejecutar la aplicación
    app.ejecutar()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
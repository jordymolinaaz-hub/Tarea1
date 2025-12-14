
#Programa: Promedio semanal del clima
#Paradigma: Programación Tradicional


# def ingresar_temperaturas():
#     """Solicita las temperaturas diarias de una semana."""
#     temperaturas = []
#     for dia in range(1, 8):
#         temperaturas.append(float(input(f"Ingrese la temperatura del día {dia}: ")))
#     return temperaturas


# def calcular_promedio(temperaturas):

#     return sum(temperaturas) / len(temperaturas) #Calcula el promedio de una lista de temperaturas.


# def main():
#     """Función principal del programa."""
#     temps = ingresar_temperaturas()
#     print(f"Promedio semanal del clima: {calcular_promedio(temps):.2f} °C")


# main()



#Ejercicio 2 POO

#Programa: Promedio semanal del clima
#Paradigma: Programación Orientada a Objetos (POO)


from abc import ABC, abstractmethod


class Clima(ABC):
    """
    Clase abstracta que representa el clima.
    Aplica abstracción y sirve como clase base.
    """

    def __init__(self):
        self._temperaturas = []

    @abstractmethod
    def ingresar_temperaturas(self):
        """
        Método abstracto que debe ser implementado por la clase hija.
        """
        pass

    def calcular_promedio(self):
        
        return sum(self._temperaturas) / len(self._temperaturas) ##Calcula el promedio semanal de las temperaturas.


class ClimaSemanal(Clima):
    """
    Clase hija que hereda de Clima.
    Aplica herencia y polimorfismo.
    """

    def ingresar_temperaturas(self):
        """
        Solicita las temperaturas diarias al usuario.
        """
        for dia in range(1, 8):
            temp = float(input(f"Ingrese la temperatura del día {dia}: "))
            self._temperaturas.append(temp)


def main():
    """
    Función principal que utiliza polimorfismo.
    """
    clima = ClimaSemanal() 
    clima.ingresar_temperaturas()
    print(f"Promedio semanal del clima: {clima.calcular_promedio():.2f} °C")

main()

import threading
import time

# Función que simula una tarea para un hilo
def tarea_hilo(identificador, delay):
    for i in range(5):
        print(f'Hilo {identificador}: Realizando tarea {i}')
        time.sleep(delay)

# Crear instancias de hilos
hilo1 = threading.Thread(target=tarea_hilo, args=(1, 1))
hilo2 = threading.Thread(target=tarea_hilo, args=(2, 0.8))
hilo3 = threading.Thread(target=tarea_hilo, args=(3, 1.2))

# Iniciar los hilos
hilo1.start()
hilo2.start()
hilo3.start()

# Esperar a que todos los hilos terminen
hilo1.join()
hilo2.join()
hilo3.join()

print('Programa principal: Todas las tareas han sido completadas.')


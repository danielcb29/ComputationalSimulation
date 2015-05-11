from Queue import *
import pygal, random, math
from pygal.style import Style

color_1 = color_2 = 'Rojo'
reloj = 0
LEF = PriorityQueue()
faseverde_1 = 100
faseverde_2 = 70
ambosrojo = 50
faserojo_1 = faseverde_2 + (2 * ambosrojo)
faserojo_2 = faseverde_1 + (2 * ambosrojo)
cola_sem_iz = 0
cola_sem_der = 0
cola_puente = Queue()
time_list = []
left_list = []
right_list = []
epi_list = []
spi_list = []


def main():
    global LEF, reloj, left_list, right_list,epi_list,spi_list
    LEF.put((0, 'VR_D'))
    #llegada_izq = generar_dato_exponencial(0.03130)
    #llegada_der = generar_dato_exponencial(0.04585)
    LEF.put((0, 'LCI'))
    LEF.put((0, 'LCD'))
    #reloj = ambosrojo  # inicializacion de ambos semaforos en rojo
    #time_list.append((color_2, 2, reloj))  # Se entiende que los dos semaforos inician en la fase ambosrojos
    left_list.append(0)  # primer tiempo de llegada de carro por la izquierda
    right_list.append(0)  # primer tiempo de llegada de carro por la derecha

    while reloj <= 7200:
        evento = LEF.get()
        reloj = evento[0]
        ev = evento[1]
        ejecutar_evento(ev)
    graficar()
    imrpimir_datos()

def imrpimir_datos():
	#print 'Tiempos acumulado de vehiculos por derecha'
    #for d in right_list:
    #    print d
	print 'Tiempos acumulado de vehiculos por izquierda'
	for d in left_list:
		print d
	print 'Tiempo de entrada de puente izquierda'
	for iz in epi_list:
		print iz
	print 'Tiempo de salida de puente izquierda'
	for sal in spi_list:
		print sal

def ejecutar_evento(ev):
    # EV = string of queue
    global color_2, color_1, LEF, faseverde_1, faseverde_2, ambosrojo, reloj, cola_sem_iz, cola_sem_der, cola_puente, cont_VI, time_list, left_list, right_list, epi_list, spi_list
    if ev == 'RV_I':
        color_1 = 'Verde'
        if cola_sem_iz > 0:
            LEF.put((reloj, 'EPI'))  #se supone que no hay cola en el puente, en ese caso habria colision
            epi_list.append(reloj)
        cont_VI = faseverde_1
        #generar tiempo vr_i
        LEF.put((faseverde_1 + reloj, 'VR_I'))
        time_list.append((color_1, 1, faseverde_1 + reloj ))
    elif ev == 'VR_I':
        color_1 = 'Rojo'
        LEF.put((ambosrojo + reloj, 'RV_D'))
        time_list.append((color_1, 1, ambosrojo + reloj))
    elif ev == 'RV_D':
        color_2 = 'Verde'
        reloj = reloj
        LEF.put((faseverde_2 + reloj, 'VR_D'))
        time_list.append((color_2, 2, faseverde_2 + reloj))
    elif ev == 'VR_D':
        color_2 = 'Rojo'
        LEF.put((ambosrojo + reloj, 'RV_I'))
        time_list.append((color_2, 2, ambosrojo + reloj))
        time_list.append((color_1, 1, ambosrojo + reloj))
    elif ev == 'LCI':
        cola_sem_iz += 1
        if (color_1 == 'Verde') & (cola_puente.qsize() < 30) & (cola_sem_iz == 1):
            LEF.put((reloj, 'EPI'))
            epi_list.append(reloj)
        #generar tiempo de proxima llegada por izquierda
        proxima_llegada = generar_dato_exponencial(0.03130) + reloj
        LEF.put((proxima_llegada, 'LCI'))
        left_list.append(proxima_llegada)
    elif ev == 'LCD':
         #generar proxima llegada por derecha
        LEF.put((generar_dato_exponencial(0.04585) +reloj, 'LCD'))
        right_list.append(generar_dato_exponencial(0.04585) +reloj)
    elif ev == 'EPI':
        cola_sem_iz -= 1
        cola_puente.put(reloj)
        cont_VI -= 5
        if (cont_VI >= 5) & (cola_puente.qsize() < 30) & (cola_sem_iz > 0):
            #tiempo de proxima entrada al puente
            LEF.put((reloj+5, 'EPI'))  #hora en que llega
            epi_list.append(reloj+5)
        if cola_puente.qsize() == 1:  #genera su propia salida
            hora_salida = cola_puente.get() + int(random.uniform(65, 75)) 
            LEF.put((hora_salida, 'SPI'))
            spi_list.append(hora_salida)
    elif ev == 'SPI':
        #cola_puente.get() como hago para si es el primero, para extraerlo y que se vaya del puente
		if cola_puente.qsize() > 0:
			proxima_salida = cola_puente.get() + int(random.uniform(65, 75))
			if proxima_salida < reloj + 5:
				proxima_salida = reloj + 5
			LEF.put((proxima_salida, 'SPI'))
			spi_list.append(proxima_salida)
		if (cola_sem_iz > 0) & (color_1 == 'Verde'):
			LEF.put((reloj,'EPI'))
			epi_list.append(reloj)


def graficar():
    global time_list
    colors = []
    for tup in time_list:
        if tup[0] == 'Verde':
            colors.append('#00FF00')
        else:
            colors.append('#FF0000')
    custom_style = Style(colors=colors)
    semaforo_chart = pygal.XY(style=custom_style)
    semaforo_chart.title = 'Semaforos'
    current_semph = 1
    red_time = 0  # tiempo acumulado en rojo mientras el otro cambia
    last_time = 0  # tiempo acumulado durante los cambios internos
    for time in time_list:
        if time[1] != current_semph:
            current_semph = time[1]
            if time[1] == 1:
                semaforo_chart.add(str(time), [(red_time, 100), (time[2], 100)])
            else:
                semaforo_chart.add(str(time), [(red_time, -100), (time[2], -100)])
            red_time = time[2]
        else:
            if time[1] == 1 and time[0] == 'Rojo':
                semaforo_chart.add(str(time), [(last_time, 100), (time[2], 100)])
                last_time = time[2]
            elif time[1] == 1 and time[0] == 'Verde':
                semaforo_chart.add(str(time), [(last_time, 50), (time[2], 50)])
                last_time = time[2]
            elif time[1] == 2 and time[0] == 'Rojo':
                semaforo_chart.add(str(time), [(last_time, -100), (time[2], -100)])
                last_time = time[2]
            elif time[1] == 2 and time[0] == 'Verde':
                semaforo_chart.add(str(time), [(last_time, -50), (time[2], -50)])
                last_time = time[2]
    semaforo_chart.render_to_file('semaforos.svg')
    print time_list


def generar_dato_exponencial(lam):
    r = random.random()
    exp = int(-(1 / lam) * (math.log(r)))
    return exp
    
def unit_test_exponential_data_left():
	for i in range(0,1000): 
		print generar_dato_exponencial(0.03130)

def unit_test_exponential_data_right():
	for i in range(0,1000): 
		print generar_dato_exponencial(0.04585) 

main()
# unit_test_exponential_data_left()
#unit_test_exponential_data_right()

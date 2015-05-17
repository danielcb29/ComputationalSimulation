from Queue import *
import pygal, random, math
from pygal.style import Style

color_1 = color_2 = 'Rojo'
reloj = 0
tiempo_simulacion = 7200
LEF = PriorityQueue()
faseverde_1 = 100
faseverde_2 = 70
ambosrojo = 80
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
epd_list = []
spd_list = []
cola_puente_cont=0
cont_VD=0
cont_VI=0

#Variables de desempeno
cont_salida_puente = 0
cont_tam_cola_iz=0
list_cola_iz =[] 
cont_tam_cola_der=0
list_cola_der=[]
tiempo_llegada_iz = PriorityQueue()
tiempo_llegada_der = PriorityQueue()
tiempo_espera_iz=[]
tiempo_espera_der=[]
numero_colisiones=0

#cont_ll=0
#cont_ent=0

def main():
	global LEF, reloj, tiempo_simulacion
	LEF.put((0, 'VR_D'))
	LEF.put((0, 'LCI'))
	LEF.put((0, 'LCD'))
	left_list.append(0)  # primer tiempo de llegada de carro por la izquierda
	right_list.append(0)  # primer tiempo de llegada de carro por la derecha

	print 'Fase verde izquierda:',faseverde_1
	print 'Fase verde derecha:',faseverde_2
	print 'Fase ambosrojo:',ambosrojo
	while reloj <= tiempo_simulacion:
		evento = LEF.get()
		reloj = evento[0]
		ev = evento[1]
		#print evento
		ejecutar_evento(ev)
	graficar()
	#imrpimir_datos()
	estudio_variables_desempeno()

def imrpimir_datos():
	print 'Tiempos acumulado de vehiculos por izquierda'
	for d in left_list:
		print d
	print 'Tiempo de entrada de puente izquierda'
	for iz in epi_list:
		print iz
	print 'Tiempo de salida de puente izquierda'
	for sal in spi_list:
		print sal
	print '######################################'
	print 'Tiempo acum der'
	for td in right_list:
		print td
	print 'Tiempo entrada der'
	for ted in epd_list:
		print ted
	print 'Tiempo salida der'
	for tsd in spd_list:
		print tsd

def ejecutar_evento(ev):
	# EV = string of queue
	global color_2, color_1, LEF, faseverde_1, faseverde_2, ambosrojo, reloj, cola_sem_iz, cola_sem_der, cola_puente, cont_VI,cont_VD, time_list, left_list, right_list, epi_list, spi_list,cola_puente_cont,epd_list,spd_list,cont_salida_puente, cont_tam_cola_iz,cont_tam_cola_der,list_cola_iz,list_cola_der,tiempo_espera_iz,tiempo_espera_der,tiempo_llegada_iz,tiempo_llegada_der,numero_colisiones#,cont_ll,cont_ent
	if ev == 'RV_I':
		color_1 = 'Verde'
		list_cola_iz.append(cont_tam_cola_iz)# VD TAM COLA IZ
		if cola_puente_cont > 0:
			numero_colisiones+=1
			restaurar_variables()
		if cola_sem_iz > 0:
			LEF.put((reloj, 'EPI'))  #se supone que no hay cola en el puente, en ese caso habria colision
			epi_list.append(reloj)
			cola_sem_iz -= 1
		cont_VI = faseverde_1
		#generar tiempo vr_i
		LEF.put((faseverde_1 + reloj, 'VR_I'))
		time_list.append((color_1, 1, faseverde_1 + reloj ))
	elif ev == 'VR_I':
		cont_tam_cola_iz = cola_sem_iz #VD TAM COLA IZ
		color_1 = 'Rojo'
		LEF.put((ambosrojo + reloj, 'RV_D'))
		time_list.append((color_1, 1, ambosrojo + reloj))
	elif ev == 'RV_D':
		color_2 = 'Verde'
		list_cola_der.append(cont_tam_cola_der) #VD TAM COLA DER
		if cola_puente_cont > 0:
			numero_colisiones+=1
			restaurar_variables()
		if cola_sem_der > 0:
			LEF.put((reloj, 'EPD'))  #se supone que no hay cola en el puente, en ese caso habria colision
			epd_list.append(reloj)
			cola_sem_der-=1
		cont_VD = faseverde_2
		#generar tiempo vr_d
		LEF.put((faseverde_2 + reloj, 'VR_D'))
		time_list.append((color_2, 2, faseverde_2 + reloj))
	elif ev == 'VR_D':
		cont_tam_cola_der=cola_sem_der # VD TAM COLA DER
		color_2 = 'Rojo'
		LEF.put((ambosrojo + reloj, 'RV_I'))
		time_list.append((color_2, 2, ambosrojo + reloj))
		time_list.append((color_1, 1, ambosrojo + reloj))
	elif ev == 'LCI':
		tiempo_llegada_iz.put(reloj) #VD TIEMPO PROM ESPERA I
		cont_tam_cola_iz+=1 # VD TAM COLA IZ
		cola_sem_iz += 1
		if (color_1 == 'Verde') & (cola_puente_cont < 30) & (cola_sem_iz == 1):
			LEF.put((reloj, 'EPI'))
			epi_list.append(reloj)
			cola_sem_iz -= 1
		#generar tiempo de proxima llegada por izquierda
		proxima_llegada = generar_dato_exponencial(0.03130) + reloj
		LEF.put((proxima_llegada, 'LCI'))
		left_list.append(proxima_llegada)
	elif ev == 'LCD':
		tiempo_llegada_der.put(reloj) #VD TIEMPO PROM ESPERA D
		cont_tam_cola_der+=1 # VD TAM COLA DER
		cola_sem_der+=1
		if (color_2 == 'Verde') & (cola_puente_cont < 30) & (cola_sem_der == 1):
			LEF.put((reloj, 'EPD'))
			epd_list.append(reloj)
			cola_sem_der-=1
		#generar proxima llegada por derecha
		proxima_llegada = generar_dato_exponencial(0.04585) +reloj
		LEF.put((proxima_llegada, 'LCD'))
		right_list.append(proxima_llegada)
	elif ev == 'EPI':
		tiempo_espera_iz.append(reloj - tiempo_llegada_iz.get())#VD TIEMPO PROM ESPERA I
		cola_puente.put(reloj)
		cola_puente_cont += 1
		cont_VI -= 5
		if (cont_VI >= 5) & (cola_puente_cont < 30) & (cola_sem_iz > 0):
			#tiempo de proxima entrada al puente
			LEF.put((reloj+5, 'EPI'))  #hora en que llega
			epi_list.append(reloj+5)
			cola_sem_iz -= 1
		if cola_puente_cont == 1:  #genera su propia salida
			hora_salida = cola_puente.get() + int(random.uniform(65, 75)) 
			LEF.put((hora_salida, 'SPI'))
			spi_list.append(hora_salida)
	elif ev == 'EPD':
		tiempo_espera_der.append(reloj-tiempo_llegada_der.get())  #VD TIEMPO PROM ESPERA D
		cola_puente.put(reloj)
		cola_puente_cont+=1
		cont_VD-=5
		if (cont_VD >= 5) & (cola_puente_cont < 30) & (cola_sem_der > 0):
			#tiempo de proxima entrada al puente
			LEF.put((reloj+5, 'EPD'))  #hora en que llega
			epd_list.append(reloj+5)
			cola_sem_der-=1
		if cola_puente_cont == 1:  #genera su propia salida
			hora_salida = cola_puente.get() + int(random.uniform(65, 75)) 
			LEF.put((hora_salida, 'SPD'))
			spd_list.append(hora_salida)            
	elif ev == 'SPI':
		cola_puente_cont -=1
		cont_salida_puente+=1 #VD PROM CARROS
		if cola_puente_cont > 0:
			proxima_salida = cola_puente.get() + int(random.uniform(65, 75))
			if proxima_salida < reloj + 5:
				proxima_salida = reloj + 5
			LEF.put((proxima_salida, 'SPI'))
			spi_list.append(proxima_salida)
		if (cola_sem_iz > 0) & (color_1 == 'Verde'):
			LEF.put((reloj,'EPI'))
			epi_list.append(reloj)
			cola_sem_iz -= 1
	elif ev == 'SPD':
		cola_puente_cont-=1
		cont_salida_puente+=1 # VD PROM CARROS
		if cola_puente_cont > 0:
			proxima_salida = cola_puente.get() + int(random.uniform(65, 75))
			if proxima_salida < reloj + 5:
				proxima_salida = reloj + 5
			LEF.put((proxima_salida, 'SPD'))
			spd_list.append(proxima_salida)
		if (cola_sem_der > 0) & (color_2 == 'Verde'):
			LEF.put((reloj,'EPD'))
			epd_list.append(reloj)
			cola_sem_der-=1

def restaurar_variables():
	cola_puente_cont=0
def estudio_variables_desempeno():
	#Promedio de carros por hora
	global cont_salida_puente,list_cola_der,list_cola_iz,tiempo_espera_iz,tiempo_espera_der,numero_colisiones
	prom_carros_hora = float(cont_salida_puente) / (tiempo_simulacion/3600)
	print 'Pormedio de carros que pasan por hora',prom_carros_hora
	
	#Tamano promedio cola
	#izq
	prom_cola_iz = 0.0
	for d in list_cola_iz: 
		prom_cola_iz+=d
	if len(list_cola_iz)>0: 
		prom_cola_iz/=len(list_cola_iz) 
	print 'Tamano promedio cola izquierda',prom_cola_iz
	#der
	prom_cola_der = 0.0
	for d in list_cola_der: 
		prom_cola_der+=d
	if len(list_cola_der)>0: 
		prom_cola_der/=len(list_cola_der) 
	print 'Tamano promedio cola derecha',prom_cola_der
	
	#tiempo promedio de espera 
	#iz
	prom_espera_iz =0.0
	for tp in tiempo_espera_iz:
		prom_espera_iz+=tp
	if len(tiempo_espera_iz)>0: 
		prom_espera_iz/=len(tiempo_espera_iz)
	print 'Tiempo promedio espera izquierda',prom_espera_iz
	#der
	prom_espera_der =0.0
	for tp in tiempo_espera_der:
		prom_espera_der+=tp
	if len(tiempo_espera_der)>0: 
		prom_espera_der/=len(tiempo_espera_der)
	print 'Tiempo promedio espera derecha',prom_espera_der
	
	#Numero de colisiones 
	print 'Numero de colisiones en la simulacion',numero_colisiones

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
    #print time_list


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

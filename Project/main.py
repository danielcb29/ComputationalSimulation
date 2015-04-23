from Queue import PriorityQueue
import pygal,random, math
from pygal.style import Style
color_1=color_2='Rojo'
reloj=0
LEF = PriorityQueue()
faseverde_1=100
faseverde_2=70
ambosrojo=50
faserojo_1= faseverde_2+(2*ambosrojo)
faserojo_2= faseverde_1+(2*ambosrojo)
time_list = []
left_list=[]
right_list=[]
def main():
	global LEF,reloj,left_list,right_list
	LEF.put((0,'RV_1'))
	llegada_izq=generar_dato_exponencial(0.03130)
	llegada_der=generar_dato_exponencial(0.04585)
	LEF.put((llegada_izq,'LCI'))
	LEF.put((llegada_der,'LCD'))
	reloj = ambosrojo #inicializacion de ambos semaforos en rojo
	time_list.append((color_1,1,reloj)) #Se entiende que los dos semaforos inician en la fase ambosrojos
	left_list.append(llegada_izq) #primer tiempo de llegada de carro por la izquierda
	right_list.append(llegada_der) #primer tiempo de llegada de carro por la derecha
	while reloj<=7200:
		ev = LEF.get()[1]
		ejecutar_evento(ev)
	graficar()
	print 'Tiempos entre llegadas por derecha'
	for d in right_list:
		print d
	print 'Tiempos entre llegadas por izquierda'
	for d in left_list:
		print d

def ejecutar_evento(ev):
	#EV = string of queue
	global color_2,color_1,LEF,faseverde_1,faseverde_2,ambosrojo,reloj,time_list,left_list,right_list
	if ev=='RV_1':
		color_1='Verde'
		reloj=faseverde_1+reloj
		LEF.put((reloj,'VR_1'))
		time_list.append((color_1,1,reloj))
	elif ev=='VR_1':
		color_1='Rojo'
		reloj=ambosrojo+reloj
		LEF.put((reloj,'RV_2'))
		time_list.append((color_1,1,reloj))
		time_list.append((color_2,2,reloj))
	elif ev=='RV_2':
		color_2='Verde'
		reloj=faseverde_2+reloj
		LEF.put((reloj,'VR_2'))
		time_list.append((color_2,2,reloj))
	elif ev=='VR_2':
		color_2='Rojo'
		reloj=ambosrojo+reloj
		LEF.put((reloj,'RV_1'))
		time_list.append((color_2,2,reloj))
		time_list.append((color_1,1,reloj))
	elif ev=='LCI':
		reloj += generar_dato_exponencial(0.03130)
		LEF.put((reloj,'LCI'))
		left_list.append(reloj)
	elif ev=='LCD':
		reloj += generar_dato_exponencial(0.04585)
		LEF.put((reloj,'LCD'))
		right_list.append(reloj)

def graficar():
	global time_list
	colors = []
	for tup in time_list: 
		if tup[0]=='Verde':
			colors.append('#00FF00')
		else:
			colors.append('#FF0000')
	custom_style = Style(colors=colors)
	semaforo_chart = pygal.XY( style=custom_style)
	semaforo_chart.title = 'Semaforos'
	current_semph = 1
	red_time = 0 #tiempo acumulado en rojo mientras el otro cambia
	last_time = 0 #tiempo acumulado durante los cambios internos
	for time in time_list:
		if time[1] != current_semph:
			current_semph=time[1]
			if time[1] == 1:
				semaforo_chart.add(str(time), [(red_time,100),(time[2],100)])
			else:
				semaforo_chart.add(str(time), [(red_time,-100),(time[2],-100)])
			red_time=time[2]
		else:
			if time[1] == 1 and time[0]=='Rojo':
				semaforo_chart.add(str(time), [(last_time,100),(time[2],100)])
				last_time=time[2]
			elif time[1] == 1 and time[0]=='Verde':
				semaforo_chart.add(str(time), [(last_time,50),(time[2],50)])
				last_time=time[2]
			elif time[1] == 2 and time[0]=='Rojo':
				semaforo_chart.add(str(time), [(last_time,-100),(time[2],-100)])
				last_time=time[2]
			elif time[1] == 2 and time[0]=='Verde':
				semaforo_chart.add(str(time), [(last_time,-50),(time[2],-50)])
				last_time=time[2]
	semaforo_chart.render_to_file('semaforos.svg')
	print time_list

def generar_dato_exponencial(lam):
	r = random.random()
	exp = -(1/lam)*(math.log1p(r))
	return exp

def unit_test_exponential_data_left():
	for i in range(0,1000): 
		print generar_dato_exponencial(0.03130)

def unit_test_exponential_data_right():
	for i in range(0,1000): 
		print generar_dato_exponencial(0.04585) 

main()
#unit_test_exponential_data_left()
#unit_test_exponential_data_right()

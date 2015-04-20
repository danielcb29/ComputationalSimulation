import pygal                                                       # First import pygal
from pygal.style import Style
custom_style = Style(colors=['#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'])
xy_chart = pygal.XY( style=custom_style)
xy_chart.title = 'Semaforosos'
xy_chart.add('Rojo_1', [(0,100),(50,100)])
xy_chart.add('Rojo_1', [(150,100),(270,100)])
xy_chart.add('Rojo_2', [(0,-100),(200,-100)])
xy_chart.add('Verde_1',  [(50,50),(150,50)])
xy_chart.add('Verde_2', [(200, -50), (270, -50)])
#xy_chart.add('y = 1',  [(-5, 1), (5, 1)])
#xy_chart.add('y = -1', [(-5, -1), (5, -1)])
xy_chart.render_to_file('semaforos.svg')                          # Save the svg to a file
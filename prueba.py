from datetime import datetime, timedelta
from re_datetime import *

now = fecha_actual()
fecha, hora = fecha_actual_txt()

print(now)
print(fecha)
print(hora)

fecha_actual = fecha_actual()
fecha_fin = datetime.strptime(fecha_actual,"%Y-%m-%d %H.%M.%S") - timedelta(minutes=5)
#fecha_inicio = datetime.strptime(fecha_fin,"%Y-%m-%d %H.%M.%S") - timedelta(minutes=5)
fecha_inicio = fecha_fin - timedelta(minutes=5)
fecha_fin = fecha_fin.strftime("%Y-%m-%d %H.%M.%S")
fecha_inicio = fecha_inicio.strftime("%Y-%m-%d %H.%M.%S")

print(fecha_inicio)
print(fecha_fin)
    
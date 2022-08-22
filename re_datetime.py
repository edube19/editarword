from datetime import datetime
from time import time

def fecha_actual():
    now = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    return now
    #2022-08-18 09.30.49

def fecha_solo():
    fecha_con_hora=fecha_actual()
    separar=fecha_con_hora.split(' ')
    fecha_solo=separar[0]
    return fecha_solo

def fecha_actual_txt():
    now = datetime.now()
    fecha = str(now.date())
    hora = str(now.hour)+"."+str(now.minute)+"."+str(now.second)
    return fecha, hora
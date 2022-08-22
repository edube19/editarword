from datetime import datetime
from re_datetime import *
from colorama import Fore, Back
from colorama import Style
import os

def crear_historial() :
    #Crear protocolo para el nombre del texto
    #pathRegistro = crear_historial()
    fecha, hora = fecha_actual_txt()
    tituloTxt = f"BotTrazer__{fecha}.txt"
    pathTxt = f"./historial/{tituloTxt}"
    if not os.path.exists(pathTxt):
        f = open (pathTxt,'w')
        f.write(tituloTxt[:-4] + '\n')
        f.close()
    return (pathTxt)

def anexar_historial(pathtexto,mensaje):
    # archivo-apendice.py
    f = open(pathtexto,'a')
    fecha, hora = fecha_actual_txt()
    f.write(f"{mensaje}"+f" HORA: {hora}"+'\n') 
    f.close()

def anexar_historial_error(pathtexto,mensaje):
    # archivo-apendice.py
    f = open(pathtexto,'a')
    fecha, hora = fecha_actual_txt()
    f.write(f"{mensaje}"+f" HORA: {hora}"+'\n')
    print (Back.RED+Fore.WHITE+mensaje+Style.RESET_ALL)
    f.close()

def anexar_bitacora(consulta):
    f = open('./bitacora.txt','a')
    for i in consulta:
        f.write(str(i)+'\n')
    f.close()

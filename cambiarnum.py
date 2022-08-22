from email.utils import decode_rfc2231
from pydoc import doc
import sys
from xmlrpc import client
from docx import Document
from docx.shared import Cm
import docx
from recursos import*
from recurso_prueba import*
from re_expediente import *
import os
from re_datetime import*

def editar_doc(page,fecha_ejecucion):
    expediente=extraer_expediente(page)#extrae el numero de expediente
    cliente=extraer_cliente(page)#extare el nombre del cliente
    ruta_guardar = f'C:/Users/DELL/Desktop/pruebaword/prueba/{fecha_ejecucion}/{expediente}.docx'
    ruta1=f"C:/Users/DELL/Desktop/pruebaword/TrazerBCP-main/TrazerBCP-main/Descargas/{fecha_ejecucion}/{expediente}.docx"
    principalv3(ruta1,cliente,ruta_guardar)
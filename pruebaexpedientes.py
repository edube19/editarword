from recursos import *
import docx
from docx import Document
from docx.shared import Cm
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

expediente='SOLCREDITOHIPOTECARIO_3990692_12.docx'
cliente='GINO PATRON ORDONEZ'
ruta=f'C:/Users/DELL/Downloads/{expediente}'
ruta_guardar=f'C:/Users/DELL/Desktop/pruebaword/TrazerBCP-main/TrazerBCP-main/pruebaexpediente/{expediente}'
principalv3_prueba(ruta,cliente,ruta_guardar)

"""nombre='GINO PATRON ORDONEZ'
ruta='C:/Users/DELL/Downloads/SOLCREDITOHIPOTECARIO_3990692_12.docx'
doc=docx.Document(ruta)
valor=buscar_nombre_separado(nombre,doc)
print(valor)"""
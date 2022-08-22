import pymysql
from re_datetime import *
from re_historial import *
from datetime import timedelta

class DataBase:
	def __init__(self):
		self.connection = pymysql.connect(
			host='192.168.48.2',
			user='botadmin',
			password='BOTadm1n$',
			db='kardpainodata',
		)
		self.cursor = self.connection.cursor()
		print("Conexión a base de datos exitosa.")

	def obtenerInfoDeHoy(self,pathRegistro):
		fecha_real = fecha_actual()
		fecha_fin = datetime.strptime(fecha_real,"%Y-%m-%d %H.%M.%S") - timedelta(minutes=5)
		fecha_inicio = fecha_fin - timedelta(minutes=5)
		fecha_fin = fecha_fin.strftime("%Y-%m-%d %H.%M.%S")
		fecha_inicio = fecha_inicio.strftime("%Y-%m-%d %H.%M.%S")
		#sql = f"""call consulta_trazer('{fecha_inicio.replace('.','-')[:-3]}-00', '{fecha_fin.replace('.','-')[:-3]}-00');"""
		sql = f"""call consulta_trazer('2022-08-18 00-00-00', '2022-08-18 23-59-59'); """ #con esto se cambia la fecha
		anexar_historial(pathRegistro,'\n'+"Consulta base de datos: " + fecha_inicio[:-3] + '.00' + ' / ' + fecha_fin[:-3] + '.00')
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			return info
		except Exception as inst:
			anexar_historial_error(pathRegistro,"No se logro realizar la consulta en la base de datos." + '\n' + str(inst))

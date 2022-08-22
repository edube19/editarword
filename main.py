#Librerias externas
from playwright.sync_api import sync_playwright
from colorama import Fore, Back
from colorama import Style
from datetime import datetime,timedelta
#Recursos propios
from re_catpcha import ResolverCatpcha
from co_principal import AbrirNavegador,LlenarCredenciales,AgregarObservaciones
from re_historial import anexar_historial_error, crear_historial
from re_datetime import fecha_actual,fecha_solo
from re_sql import *
from re_email import *
from re_expediente import*


if __name__=='__main__':
    with sync_playwright() as playwright:
        print(Fore.YELLOW + "======================================================================"+ Style.RESET_ALL)
        print(Back.BLACK+Fore.RED + """
        _______                  __   ____       __      _______        
        |   __   \      /\       |  | |     \    |  |    /       \\       
        |  |   \  \    /  \      |  | |  |\  \   |  |   /   ___   \\      
        |  |__ /  /   / /\ \     |  | |  | \  \  |  |  |   |   |   |     
        |    ____/   / /__\ \    |  | |  |  \  \ |  |  |   |   |   |     
        |   |       /  ____  \   |  | |  |   \  \|  |  |   |___|   |     
        |   |      /  /    \  \  |  | |  |    \     |   \         /      
        |___|     /__/      \__\ |__| |__|     \____|    \_______/       
                                                                        
        """ + Style.RESET_ALL+'\033[0;m') 
        print(Fore.YELLOW + "======================================================================="+ Style.RESET_ALL)
        print('\n' + Fore.YELLOW + ">>>======================Iniciando programa...======================<<<" + Fore.RESET +'\n')
        pathRegistro = crear_historial()
        to_s = 'practicantes.sistemas@notariapaino.pe'
        sql = DataBase()
        info = sql.obtenerInfoDeHoy(pathRegistro)
        #info = (('515131', '3991338', 'Firmo: MARTINEZ VILCA ISEL TATIANA', 1, 1, '8'), ('8061', '396X', 'HORA PRUEBA', 1, 1, '8'), ('517700', '3970158', 'PENDIENTES:1. BLOQUEO INSCRITO.2. HR/ PU C/INMUEBLE 2022 LEGIBLE DE C/U DE LOS INMUEBLES.3. RENTA.4. ALCABALA.5. PREDIAL.6.. CHEQUE PRODUCTO DEL DESEMBOLSO- SE HIZO CONSULTA POR EMISION A CG.', 1, 1, '8'), ('515131', '3991338', 'Firmo: MARTINEZ VILCA ISEL TATIANA', 1, 1, '8'))
        print("Casos encontrados: "+str(len(info)))
        anexar_historial(pathRegistro, '\n' + "Casos encontrados: "+str(len(info)) + '\n' + str(info))
        #anexar_bitacora(info)
        if len(info) == 0:
            logeando,agregar = False, False
        else:
            logeando,agregar = True, True
        hora_primer_logeo = datetime.strptime(fecha_actual(), "%Y-%m-%d %H.%M.%S")
        hora_ultimo_logeo = hora_primer_logeo
        while logeando == True and (hora_ultimo_logeo-hora_primer_logeo) < timedelta(minutes=10):
            path_to_extension = "./my-extension"
            user_data_dir = "/tmp/test-user-data-dir"
            context = playwright.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                args=[
                    f"--disable-extensions-except={path_to_extension}",
                    f"--load-extension={path_to_extension}",
                ],
            )
            page = AbrirNavegador(context,pathRegistro)
            if page:
                LlenarCredenciales(page)
                try:
                    msjeCatpcha = ResolverCatpcha(page,pathRegistro)
                    if msjeCatpcha == 'You are verified':
                        logeando = False
                except Exception as inst:
                    print('Error: Fallo la resolucion del catpcha')
                    print(inst)
                    anexar_historial_error(pathRegistro,'\n'+'Error: Fallo la resolucion del catpcha'+'\n'+str(inst))
            if logeando:
                hora_ultimo_logeo = datetime.strptime(fecha_actual(), "%Y-%m-%d %H.%M.%S")
                context.close()
            else:
                print("Catpcha resuelto, iniciando sesion ...")
                page.locator('#login-validate > div.submit_sect > button').click()

        if (hora_ultimo_logeo-hora_primer_logeo) >= timedelta(minutes=10):
            msje = '\n' + 'Tardo mucho el logeo de usuario en la pagina https://trazerweb.com/Login/index'
            anexar_historial_error(pathRegistro,msje)
            enviar_email(to_s,'Error Bot Trazer','Tardo mucho el logeo de usuario en la pagina https://trazerweb.com/Login/index, no se revisaron los siguientes casos. ' + str(info))
            agregar = False

        if agregar:
            AgregarObservaciones(page, info, pathRegistro, to_s)
            context.close()
        
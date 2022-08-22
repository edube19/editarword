from pydoc import pager
#from .re_datetime import fecha_solo
from re_datetime import*
from re_expediente import *
from re_historial import anexar_historial, anexar_historial_error
from re_email import enviar_email
# from playwright.sync_api import expect
#
#
#import time

from cambiarnum import*

def AbrirNavegador(context,pathRegistro):
    try:
        page = context.new_page()
        page.goto("http://www.trazerweb.com",wait_until='networkidle')
        return page
    except Exception as inst:
        msje = '\n'+'Error: Carga del navegador o de la pagina de login'+'\n'+str(inst)
        anexar_historial_error(pathRegistro,msje)
        return False

def LlenarCredenciales(page):
    usuario = '10082420822'
    psw = 'Cierre123'
    page.fill('#usuario',usuario)
    page.fill('#contrasena',psw)

def AgregarObservaciones(page, info, pathRegistro, to_s):
    import time
    fecha_ejecucion=fecha_actual()
    os.makedirs(f'C:/Users/DELL/Desktop/pruebaword/prueba/{fecha_ejecucion}', exist_ok=True)
    os.makedirs(f'C:/Users/DELL/Desktop/pruebaword/TrazerBCP-main/TrazerBCP-main/Descargas/{fecha_ejecucion}', exist_ok=True)
    for i in range(len(info)):
        if info[i][0] != '8060':
            print('\n'+'Expendiente Nro. ' + str(info[i][1]))
            anexar_historial(pathRegistro,'\n'+'Expendiente Nro. ' + str(info[i][1]))
            try:
                page.goto('https://www.trazerweb.com/BandejaEntrada',wait_until='networkidle')
            except Exception as inst:
                msje = '\n' + 'Error (bromita) : Carga de la pagina https://www.trazerweb.com/BandejaEntrada' + '\n' + str(inst)
                anexar_historial_error(pathRegistro,msje)
                enviar_email(to_s,'Error Bot Trazer','No cargo la pagina https://www.trazerweb.com/BandejaEntrada durante la evaluacion del expediente '+str(info[i][1]))
                continue
            #AGREGAR KARDEX Y PAGOS A TRAZER
            page.wait_for_selector('body > div.main-wrapper > header > div > div > div.span5 > nav > ul > li:nth-child(3) > a')
            try:
                page.goto('https://www.trazerweb.com/BandejaConsultas',wait_until='networkidle')
            except Exception as inst:
                msje = '\n' + 'Error (bromita) : Carga de la pagina https://www.trazerweb.com/BandejaConsultas' + '\n' + str(inst)
                anexar_historial_error(pathRegistro,msje)
                enviar_email(to_s,'Error Bot Trazer','No cargo la pagina https://www.trazerweb.com/BandejaConsultas durante la evaluacion del expediente '+str(info[i][1]))
                continue
            page.select_option("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > select", "01")
            page.wait_for_selector('#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input')
            page.fill("#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input", str(info[i][1]))
            #Busqueda del expendiente
            page.click("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > span > img")
            #Espera que aparezca el cuadro del msje
            page.wait_for_selector('body > div.sticky-queue.top-right')
            msjeInterno = page.locator('body > div.sticky-queue.top-right').inner_text()
            if msjeInterno.find('Por favor, no escribas menos de 4 caracteres.')!=-1 or msjeInterno.find('Sucedió un error al realizar la búsqueda')!=-1:
                print('Error en el formato del nro expediente')
                anexar_historial(pathRegistro,'Error en el formato del nro expediente: '+msjeInterno)
                enviar_email(to_s,'Error Bot Trazer','Consulta '+str(info[i])+'. Error en el formato del nro expediente: '+msjeInterno[2:])
            elif msjeInterno.find('Búsqueda satisfactoria')!=-1:
                page.wait_for_selector('#dtActividadesHipotecario > tbody > tr > td')
                contenidoTabla = page.locator('#dtActividadesHipotecario > tbody > tr > td:nth-child(1)').inner_text()
                if contenidoTabla == 'Sin información':
                    print('Nro de expediente no existe')
                    msje = 'Nro de expediente no existe o no contiene informacion alguna'
                    anexar_historial(pathRegistro,msje)
                    enviar_email(to_s,'Error Bot Trazer','Consulta '+str(info[i])+'. '+msje)
                elif contenidoTabla == info[i][1]:
                #Visualizar operacion
                    page.click("#dtActividadesHipotecario > tbody > tr > td:nth-child(9) > i")
                    try:
                        with page.expect_navigation():
                            page.evaluate(f"document.querySelector('#menuNotaria > li > a').click()")
                        page.click("#accordion1 > div > div.accordion-heading > a")#click en 'Funcionalidades transversales'
                    except Exception as inst:
                        msje = '\n' + 'Error (bromita) : Carga de la pagina https://trazerweb.com/FirmaContratoLegalft o similares' + '\n' + str(inst)
                        anexar_historial_error(pathRegistro,msje)
                        enviar_email(to_s,'Error Bot Trazer','No cargo la pagina https://trazerweb.com/FirmaContratoLegalft, o similares, durante la evaluacion del expediente '+str(info[i][1]))
                    
                    time.sleep(1)
                    #
                    
                    busqueda=buscar_sin_firma(page,fecha_ejecucion)#descarga los prestamos sin firmar en una carpeta
                    time.sleep(1)
                    if (busqueda):
                        editar_doc(page,fecha_ejecucion)
                    #
                    #descomnetar esto de abajo para que este como el original
                    """page.click("#collapseOne1 > div > ul > li:nth-child(2) > a")#click en bitacora
                    page.wait_for_selector("#observaciones")
                    page.wait_for_selector("#dtBitacora_wrapper > div.dt-wrapper")
                    page.fill("#observaciones", info[i][2])"""
              
                    ##dt_Expediente_Digital_Archivoss_filter > label > input[type=text] para poner 'prestamo'

                    #click en enviar
                    #page.click('#contenedorBitacora > div:nth-child(1) > div.span2 > button')
                    # try:
                    #     page.wait_for_selector('body > div.sticky-queue.top-right')
                    #     msjeInterno = page.locator('body > div.sticky-queue.top-right').inner_text()
                    #     if msjeInterno.find('Se registro la información correctamente.')!=-1:
                    #         #Se imprime en consola y se anexa al historial las observaciones agregadas a la bitácora
                    #         print('\n'+'Observaciones agregadas: ' + '\n' + info[i][2])
                    #         anexar_historial(pathRegistro,'\n'+'Observaciones agregadas: ' + '\n' + info[i][2])
                    # except Exception as inst:
                    #     anexar_historial(pathRegistro,'\n'+'Error: No se subieron las observaciones a la bitacora. '+str(inst))
                    time.sleep(1)
        else:
            continue



def ProcesoTrazer(page):

    idSeguimientoTrazer="3956235"
    observacionBitacora="KARDEX \n"+"KARDEX \nDERECHO \nDERECHOS"
    listaKeys=['Estudio de título final','minuta','cláusula adicional']

    #AGREGAR KARDEX Y PAGOS A TRAZER
    page.wait_for_selector('body > div.main-wrapper > header > div > div > div.span5 > nav > ul > li:nth-child(3) > a')
    page.goto('https://www.trazerweb.com/BandejaConsultas',wait_until='networkidle')
    page.select_option("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > select", "01")
    page.wait_for_selector('#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input')
    page.fill("#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input", idSeguimientoTrazer)
    page.click("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > span > img")
    page.click("#dtActividadesHipotecario > tbody > tr > td:nth-child(9) > i")

    with page.expect_navigation():
        page.evaluate("document.querySelector('#menuNotaria > li > a').click()")
    #page.evaluate("document.querySelector('#menuNotaria > li > a').click()")

    page.click("text=Funcionalidades Transversales")
    page.click("text=Bitácora")
    page.fill("text=Observaciones Agregar >> textarea", observacionBitacora)
    #Falta hacer clcik en enviar
    time.sleep(10)

    #DESCARGAR DOCUMENTOS
    page.goto('https://www.trazerweb.com/BandejaConsultas')
    page.select_option("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > select", "01")
    page.wait_for_selector('#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input')
    page.fill("#frmHipotecario > div:nth-child(2) > div:nth-child(3) > input", idSeguimientoTrazer)
    page.click("#frmHipotecario > div:nth-child(1) > div:nth-child(3) > div > div > span > img")
    page.click("#dtActividadesHipotecario > tbody > tr > td:nth-child(9) > i")
    
    with page.expect_navigation():
        page.evaluate("document.querySelector('#menuNotaria > li > a').click()")
    #page.evaluate("document.querySelector('#menuNotaria > li > a').click()")
    
    page.click("text=Funcionalidades Transversales")

    page.type("#dt_Expediente_Digital_Archivoss_filter > label > input[type=text]", listaKeys[0])
    with page.expect_download() as download_info:
        page.click("#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(7) > i")
    download = download_info.value
    path = f"./Descargas/abcx.docx"
    # Guardamos la información en el dispositivo
    download.save_as(path)
    download.delete()  

    #dt_Expediente_Digital_Archivoss > tbody > tr:nth-child(1) > td:nth-child(7) > i
    #dt_Expediente_Digital_Archivoss > tbody > tr:nth-child(1) > td:nth-child(7) > i
    #dt_Expediente_Digital_Archivoss > tbody > tr:nth-child(2) > td:nth-child(7) > i
    #Falta hacer clcik en enviar
    time.sleep(30)

    # ---------------------

"""     with page.expect_download() as download_info:
        page.click("text=SOLCREDITOHIPOTECARIO_3956235_13.docx 3956235-RENZO ZEBALLOS DEZA- contrato con  >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=SOLCREDITOHIPOTECARIO_3956235_12.docx 3956235-RENZO ZEBALLOS DEZA- contrato con  >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=SOLCREDITOHIPOTECARIO_3956235_11.docx 3956235-RENZO ZEBALLOS DEZA- contrato sin  >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=SOLCREDITOHIPOTECARIO_3956235_9.docx 3956235-RENZO ZEBALLOS DEZA- contrato con f >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=SOLCREDITOHIPOTECARIO_3956235_8.docx 3956235-RENZO ZEBALLOS DEZA- contrato sin f >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("tr:nth-child(7) td:nth-child(7) .icon-download")
    download = download_info.value
    page.click("text=102550100 DocumentoArchivoClasificaciónStatusFecha DigitalizaciónComentariosDesc >> input[type=\"text\"]")
    page.fill("text=102550100 DocumentoArchivoClasificaciónStatusFecha DigitalizaciónComentariosDesc >> input[type=\"text\"]", "minuta")
    with page.expect_download() as download_info:
        page.click("text=Minuta de Compra Venta_3956235_2.pdf VEN - 201 - Compraventa Zeballos - Rospigli >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=Minuta de Compra Venta_3956235_1.pdf CLAUSULA ADICIONAL.pdf OTROS VÁLIDO 10/06/2 >> i")
    download = download_info.value
    with page.expect_download() as download_info:
        page.click("text=Minuta de Compra Venta_3991131_1_TASACIONANTICIPADA_10062022.pdf MINUTA COMPRA - >> i")
    download = download_info.value """
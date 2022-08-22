from xml.dom.minidom import Document
from playwright.sync_api import Playwright, sync_playwright
import time
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    #LOGIN
    idSeguimientoTrazer="3956235"
    observacionBitacora="KARDEX \n"+"KARDEX \nDERECHO \nDERECHOS"
    listaKeys=['Estudio de título final','minuta','cláusula adicional']
    page.goto("https://www.trazerweb.com/")
    page.click("input[name=\"usuario\"]")
    page.fill("input[name=\"usuario\"]", "10082420822")
    page.click("input[name=\"contrasena\"]")
    page.fill("input[name=\"contrasena\"]", "Cierre123")

    #AQUI SE RESUELVE EL CAPTCHA
    #page.frame(name="a-3g4yr25lbchi").click("text=No soy un robot")
    time.sleep(20)

    #AGREGAR KARDEX Y PAGOS A TRAZER
    page.evaluate("document.querySelector('#login-validate > div.submit_sect > button').click()")
    time.sleep(7)

    #AGREGAR KARDEX Y PAGOS A TRAZER
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
    context.close()
    browser.close()

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

with sync_playwright() as playwright:
    run(playwright)
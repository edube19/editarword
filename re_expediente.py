import re
import time

def contar_registros(estado):
    #'Mostrando 1 a 10 de 51 registros'
    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', estado)]#extrae los numeros de un string, si quiere con decimales cambiar el int por float
    #print(s)
    registros=s[1]#en esta posicion se guarda la cantidad total de resultados de la busqueda (10)
    return registros #este es un int

def buscar_palabra(columna,ncol):
    cond=False
    if ncol==2 or ncol==6:
        r=columna.find('sin firma')
        t=columna.find('SIN FIRMA')
        if (r!=-1 or t!=-1):
            cond=True
    if ncol==4:
        if (columna=='VÁLIDO' or columna=='VALIDO'):
            cond=True
    return cond
            
def buscar_sin_firma(page,fecha_solo):
    try:
        page.wait_for_selector('#dt_Expediente_Digital_Archivoss_filter > label > input[type=text]')
        time.sleep(1)
        page.click('#dt_Expediente_Digital_Archivoss_filter > label > input[type=text]')
        page.keyboard.type("sin firma", delay=100)
        #page.fill('#dt_Expediente_Digital_Archivoss_filter > label > input[type=text]','sin firma')
        
        page.wait_for_selector('#dt_Expediente_Digital_Archivoss_info')
        estado=page.evaluate("document.querySelector('#dt_Expediente_Digital_Archivoss_info').innerText")
        #print(estado)#si esta leyendo el estado 
    except Exception as e:
        print(e)
    #print('contar_registros',contar_registros(estado)) si esta leyendo la cantidad de resultados
    if contar_registros(estado)!=0:#existe la tabla
        if contar_registros(estado)==1:#caso que solo haya un elemento en la busqueda
            page.wait_for_selector('#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(4)')
            #status
            status = page.evaluate ("document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(4)').innerText")
            cond1=buscar_palabra(status,4)
            #Archivo
            archivo = page.evaluate ("document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(2)').innerText")
            cond2=buscar_palabra(archivo,2)
            #Comentario, en caso falle en el nombre
            comentario = page.evaluate ("document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(6)').innerText")
            cond3=buscar_palabra(comentario,6)
            if ((cond1==True) and (cond2==True)) or ((cond1==True) and (cond3==True)):
                #page.click('#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(7) > i')
                exp=extraer_expediente(page)
                try:
                    with page.expect_download() as download_info:
                        page.click("#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(7) > i")
                    download = download_info.value
                    path = f"./Descargas/{fecha_solo}/{exp}.docx"
                    # Guardamos la información en el dispositivo
                    download.save_as(path)
                    download.delete()  
                except Exception as e:
                    print(e)
        else:            
            for i in range(1,contar_registros(estado)+1):#en caso haya muchos resultados
                page.wait_for_selector(f'#dt_Expediente_Digital_Archivoss > tbody > tr:nth-child({i}) > td:nth-child(4)')
                #columna status
                status=page.evaluate(f"document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr:nth-child({i}) > td:nth-child(4)').innerText")
                cond1=buscar_palabra(status,4)
                #columna archivo
                archivo=page.evaluate(f"document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr:nth-child({i}) > td:nth-child(2)').innerText")
                cond2=buscar_palabra(archivo,2)
                #columna comentario
                comentario = page.evaluate (f"document.querySelector('#dt_Expediente_Digital_Archivoss > tbody > tr:nth-child({i}) > td:nth-child(6)').innerText")
                cond3=buscar_palabra(comentario,6)
                if ((cond1==True) and (cond2==True)) or ((cond1==True) and (cond3==True)):
                    #page.click(f"#dt_Expediente_Digital_Archivoss > tbody > tr:nth-child({i}) > td:nth-child(7) > i")
                    exp=extraer_expediente(page)
                    try:
                        with page.expect_download() as download_info:
                            page.click("#dt_Expediente_Digital_Archivoss > tbody > tr > td:nth-child(7) > i")
                        download = download_info.value
                        path = f"./Descargas/{fecha_solo}/{exp}.docx"
                        # Guardamos la información en el dispositivo
                        download.save_as(path)
                        download.delete()
                        break
                    except Exception as e:
                        print(e)
        return True
    else:
        print('Aun no hay registros de prestamos sin firma')
        return False

def extraer_cliente(page):
    time.sleep(2)
    page.wait_for_selector('#divEncabezado > div > table:nth-child(1) > tbody > tr:nth-child(6) > td:nth-child(2)')
    cliente= page.evaluate("document.querySelector('#divEncabezado > div > table:nth-child(1) > tbody > tr:nth-child(6) > td:nth-child(2)').innerText")
    print(cliente)
    return cliente

def extraer_expediente(page):
    time.sleep(2)
    page.wait_for_selector('#divEncabezado > div > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(2)')
    expediente= page.evaluate("document.querySelector('#divEncabezado > div > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(2)').innerText")
    #print('descargando el expediente',expediente)
    return expediente

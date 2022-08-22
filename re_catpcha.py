#Librerias externas
import time
#Recursos propios
from re_historial import anexar_historial_error

def ResolverDesafio(frameDesafio,pathRegistro):
    try:
        botonBuster = frameDesafio.locator('body > div > div > div.rc-footer > div.rc-controls > div.primary-controls > div.rc-buttons > div.button-holder.help-button-holder')
        botonBuster.hover()
        botonBuster.click()
        return True
    except Exception as inst:
        print('Error: Boton para resolver el desafio')
        print(inst)
        anexar_historial_error(pathRegistro,'\n'+'Error: Boton para resolver el desafio'+'\n'+str(inst))
        return False

def ResolverCatpcha(page,pathRegistro):
    framePrincipal = page.frame_locator('#loginreCaptcha > div > div > iframe')
    casillaVerificacion = framePrincipal.locator('#recaptcha-anchor')
    # Hacemos clic a la casilla de verificacion del catpcha
    casillaVerificacion.click()
    msjeCatpcha = ''

    while msjeCatpcha != 'You are verified':
        for i in range(3):
            frameDesafio = page.frame_locator(f'body > div:nth-child({i+2}) > div:nth-child(4) > iframe')
            bodyDesafio = frameDesafio.locator("body").get_attribute("style")
            imgDesafio = frameDesafio.locator("#rc-imageselect").count()
            audioDesafio = frameDesafio.locator("body > div > div > div.rc-audiochallenge-error-message").count()
            if bodyDesafio == 'height: 100%;' and (imgDesafio != 0 or audioDesafio != 0):
                if imgDesafio==1:
                    desafioAuditivo = frameDesafio.locator('#recaptcha-audio-button')
                    desafioAuditivo.click()
                time.sleep(1)
                valueFrame = frameDesafio.locator('#recaptcha-token').get_attribute("value") #548, 526
                newValueFrame = valueFrame
                veces = 0
                while newValueFrame == valueFrame:
                    if veces>=1:
                        cambiarDesafio = frameDesafio.locator('#recaptcha-reload-button')
                        cambiarDesafio.click()
                        time.sleep(1)
                        imgDesafio = frameDesafio.locator("#rc-imageselect").count()
                        if imgDesafio==1:
                            desafioAuditivo = frameDesafio.locator('#recaptcha-audio-button')
                            desafioAuditivo.click()
                            time.sleep(1)
                        errorDesafio = frameDesafio.locator('body > div > div > div.rc-audiochallenge-error-message')
                        while errorDesafio.inner_text() == 'Multiple correct solutions required - please solve more.':
                            print(errorDesafio.inner_text())
                            cambiarDesafio.click()
                            time.sleep(1)
                        valueFrame = frameDesafio.locator('#recaptcha-token').get_attribute("value") #548, 526
                        newValueFrame = valueFrame
                    if not ResolverDesafio(frameDesafio,pathRegistro):
                        break
                    time.sleep(5)
                    newValueFrame = frameDesafio.locator('#recaptcha-token').get_attribute("value")
                    veces=+1
                #Si en 5 segundos no cambia el value entonces hay que (cambiar de reto) volver a resolver el desafio
                var = True
                msjeCatpcha = framePrincipal.locator('#recaptcha-accessible-status').inner_text()
                break
            else:
                var = False
        if var:
            break
        msjeCatpcha = framePrincipal.locator('#recaptcha-accessible-status').inner_text()
        
    return msjeCatpcha
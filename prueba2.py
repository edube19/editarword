from playwright.sync_api import sync_playwright
from re_email import *

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://www.trazerweb.com/")
#     print(page.title())
#     page.wait_for_selector('#usuario')
#     page.fill('#usuario','111222')
#     import time
#     time.sleep(2)
#     page.fill('#usuario','333')
#     time.sleep(2)
#     browser.close()
to_s = 'practicantes.sistemas@notariapaino.pe'

enviar_email(to_s,'Mensaje de prueba','mensaje de prueba')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time, csv

URL = "https://mtpe-candidatos.empleosperu.gob.pe/ofertas"

service = Service("chromedriver.exe")  # Ruta a tu chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

jobs = []

for a in soup.select("div.list-group.overflow-hidden a"):
    title_el = a.select_one("h5 ngb-highlight")
    empresa_el = a.select("ngb-highlight")
    empresa = empresa_el[1].get_text(strip=True) if len(empresa_el) > 1 else None
    ubicacion = a.select_one("span").get_text(strip=True) if a.select_one("span") else None

    small_spans = a.select("small span")
    detalles = [s.get_text(strip=True) for s in small_spans]
    detalles_text = " | ".join(detalles)

    jobs.append({
        "titulo": title_el.get_text(strip=True) if title_el else None,
        "empresa": empresa,
        "ubicacion": ubicacion,
        "detalles": detalles_text,
    })



driver.quit()
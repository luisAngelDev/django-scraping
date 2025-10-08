from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time, csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


URL = "https://mtpe-candidatos.empleosperu.gob.pe/ofertas"

options = Options()
options.add_argument("--headless")  # opcional, si no quieres abrir ventana
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Crear driver
driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(5)


# Espera hasta que haya al menos un elemento de la lista de empleos
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-group.overflow-hidden a"))
    )
except:
    print("No se cargaron los resultados a tiempo.")



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

if jobs:
    with open("trabajos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    print(f"Guardado {len(jobs)} trabajos en trabajos.csv")
else:
    print("No se encontraron trabajos.")
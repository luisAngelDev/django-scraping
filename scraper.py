import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

URL = "https://mtpe-candidatos.empleosperu.gob.pe/search-jobs/description?jobId=0f305c24b93e48e3a34311c8249c7d1a"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

def safe_text(el):
    return el.get_text(strip=True) if el else None

def scrape_page(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    # Seleccionamos todas las ofertas dentro del contenedor principal
    for a in soup.select("div.list-group.overflow-hidden a"):
        # Extraer título (primer h5 > ngb-highlight)
        title_el = a.select_one("h5 ngb-highlight")
        title = safe_text(title_el)

        # Empresa (segundo ngb-highlight fuera del h5)
        empresa_el = a.select("ngb-highlight")
        empresa = safe_text(empresa_el[1]) if len(empresa_el) > 1 else None

        # Ubicación (span debajo del subtítulo)
        ubicacion_el = a.select_one("span")
        ubicacion = safe_text(ubicacion_el)

        # Detalles (último div con small > span)
        detalles = []
        small_spans = a.select("small span")
        for s in small_spans:
            detalles.append(safe_text(s))
        detalles_text = " | ".join(detalles)

        # Link al detalle (href del <a>)
        link = a.get("href")
        if link:
            link = urljoin(url, link)

        jobs.append({
            "titulo": title,
            "empresa": empresa,
            "ubicacion": ubicacion,
            "detalles": detalles_text,
            "link": link
        })

    return jobs


def save_csv(items, filename="trabajos.csv"):
    if not items:
        print("No se encontraron trabajos.")
        return
    keys = items[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)
    print(f" Guardado {len(items)} trabajos en {filename}")

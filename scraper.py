import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

URL = "https://mtpe-candidatos.empleosperu.gob.pe/search-jobs/description?jobId=0f305c24b93e48e3a34311c8249c7d1a"  # <-- pon aquí la página principal de empleos

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

    # Cada tarjeta de empleo (ajusta la clase principal si es necesario)
    for card in soup.select("div.list-group-item"):
        # Títulos dentro de h6 (posición 0 = título, 1 = empresa)
        h6s = card.find_all("h6")
        title = safe_text(h6s[0]) if len(h6s) > 0 else None
        empresa = safe_text(h6s[1]) if len(h6s) > 1 else None

        # Extraer todos los li de los divs de detalle
        detalles = []
        for ul in card.find_all("ul"):
            for li in ul.find_all("li"):
                detalles.append(safe_text(li))

        jobs.append({
            "titulo": title,
            "empresa": empresa,
            "detalles": " | ".join(detalles)  # concatenamos todo en un campo
        })

    return jobs

def save_csv(items, filename="trabajos.csv"):
    keys = ["titulo", "empresa", "detalles"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)

def main():
    trabajos = scrape_page(URL)
    print(f"Encontrados {len(trabajos)} trabajos")
    save_csv(trabajos)

if __name__ == "__main__":
    main()

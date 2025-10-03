# scraper_requests.py
import requests
from bs4 import BeautifulSoup
import time
import csv
import logging
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def make_session(retries=3, backoff_factor=0.5, status_forcelist=(500,502,503,504)):
    s = requests.Session()
    retries = Retry(total=retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=status_forcelist,
                    allowed_methods=["GET","POST"])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.headers.update(HEADERS)
    return s

def fetch(session, url, timeout=10):
    logger.info("Fetching %s", url)
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    time.sleep(1)  # pausa cortita para no spamear el servidor
    return resp.text

def parse_list_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # Ejemplo: buscar tarjetas de producto / noticias
    for card in soup.select(".card, .news-item, .product"):
        title = card.select_one(".title, h2, .product-title")
        price = card.select_one(".price")
        link = card.select_one("a")
        items.append({
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "link": link['href'] if link and link.has_attr('href') else None
        })
    return items

def save_csv(items, filename="results.csv"):
    keys = items[0].keys() if items else []
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)

def main():
    session = make_session()
    base_url = "https://ejemplo.com/listado"
    html = fetch(session, base_url)
    items = parse_list_page(html)
    save_csv(items)
    logger.info("Guardado %d items", len(items))

if __name__ == "__main__":
    main()

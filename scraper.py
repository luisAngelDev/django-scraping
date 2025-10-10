import requests
import csv
import time

#BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api/v1/ofertas"
BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api/jobs?limit=30&offset=0"

LIMIT = 30

def obtener_todas_las_ofertas():
    trabajos = []
    offset = 0

    while True:
        params = {"limit": LIMIT, "offset": offset}
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Error al obtener página con offset {offset}: {response.status_code}")
            break

        data = response.json()
        ofertas = data.get("data", [])
        total = data.get("totalCount", 0)

        if not ofertas:
            break

        for job in ofertas:
            trabajos.append({
                "titulo": job.get("titulo"),
                "empresa": job.get("empresa", {}).get("razonSocial"),
                "ubicacion": job.get("departamento"),
                "descripcion": job.get("descripcion"),
            })

        print(f"Descargadas {len(trabajos)} de {total} ofertas...")
        offset += LIMIT
        time.sleep(0.5)  # Evita saturar el servidor

        if offset >= total:
            break

    return trabajos


if __name__ == "__main__":
    trabajos = obtener_todas_las_ofertas()

    if trabajos:
        with open("trabajos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=trabajos[0].keys())
            writer.writeheader()
            writer.writerows(trabajos)
        print(f"Guardado {len(trabajos)} trabajos en trabajos.csv")
    else:
        print("No se encontraron trabajos.")

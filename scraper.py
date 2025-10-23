
import requests
import csv
import time
import json

BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api/jobs"
LIMIT = 30

def obtener_todas_las_ofertas():
    trabajos = []
    offset = 0

    while True:
        params = {"limit": LIMIT, "offset": offset}
        resp = requests.get(BASE_URL, params=params, timeout=15)
        if resp.status_code != 200:
            print(f"Error al obtener página con offset {offset}: {resp.status_code}")
            break

        data = resp.json()
        ofertas = data.get("data", [])
        total = data.get("totalCount", 0)

        if not ofertas:
            break

        for job in ofertas:
            # Manejar campos opcionales
            location = job.get("location") or {}
            geo = job.get("geoLocation") or {}
            contract = job.get("contractType") or {}
            hours = job.get("hoursPerWeek") or {}
            education = job.get("educationDegree") or {}

            salary_min = salary_max = None
            packages = job.get("offeredRemunerationPackages") or []
            if packages:
                first = packages[0]
                salary_min = first.get("minimumAmount")
                salary_max = first.get("maximumAmount")

            trabajos.append({
                "id": job.get("id"),
                "titulo": job.get("positionTitle"),
                "empresa": job.get("companyName"),
                "descripcion_empresa": job.get("companyDescription"),
                "companyId": job.get("companyId"),
                "department_code": location.get("DEPARTMENT"),
                "province_code": location.get("PROVINCE"),
                "district_code": location.get("DISTRICT"),
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "contract_type": contract.get("name"),
                "hours_per_week": hours.get("name"),
                "education_degree": education.get("name"),
                "salary_min": salary_min,
                "salary_max": salary_max,
                "date_posted": job.get("datePosted"),
                "active": job.get("active"),
                "approvalStatus": job.get("approvalStatus"),
            })

        print(f"Descargadas {len(trabajos)} de {total} ofertas...")
        offset += LIMIT
        time.sleep(0.2)

        if offset >= total:
            break

    return trabajos


if __name__ == "__main__":
    trabajos = obtener_todas_las_ofertas()

    if not trabajos:
        print("No se encontraron trabajos.")
    else:
        # Guardar CSV (utf-8-sig para abrir bien en Excel)
        fieldnames = list(trabajos[0].keys())
        with open("trabajos.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trabajos)

        # Guardar JSON completo
        with open("trabajos.json", "w", encoding="utf-8") as f:
            json.dump(trabajos, f, ensure_ascii=False, indent=2)

        print(f"Guardado {len(trabajos)} trabajos en trabajos.csv y trabajos.json")

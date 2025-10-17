import requests
import json

BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api/jobs"
LIMIT = 5 

def obtener_ofertas_de_prueba():
    params = {"limit": LIMIT, "offset": 0}
    resp = requests.get(BASE_URL, params=params, timeout=15)

    if resp.status_code != 200:
        print(f"Error al obtener ofertas: {resp.status_code}")
        return []

    data = resp.json()
    ofertas = data.get("data", [])

    trabajos = []

    for job in ofertas:
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

    return trabajos




if __name__ == "__main__":
    trabajos = obtener_ofertas_de_prueba()

    if not trabajos:
        print(" No se encontraron trabajos.")
    else:
        with open("trabajos_prueba.json", "w", encoding="utf-8") as f:
            json.dump(trabajos, f, ensure_ascii=False, indent=2)

        print(f" Guardadas {len(trabajos)} ofertas en 'trabajos_prueba.json'")


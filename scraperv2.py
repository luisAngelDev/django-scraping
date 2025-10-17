import requests
import json

BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api"

def obtener_catalogos():
    """Obtiene los nombres de departamentos, provincias y distritos"""
    url = f"{BASE_URL}/additionalDisplayData?language=es-pe"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    loc = data.get("location", {})
    departamentos = {d["code"]: d["name"] for d in loc.get("DEPARTMENT", [])}
    provincias = {p["code"]: p["name"] for p in loc.get("PROVINCE", [])}
    distritos = {d["code"]: d["name"] for d in loc.get("DISTRICT", [])}

    return departamentos, provincias, distritos


def obtener_ofertas(location="lima", limit=10):
    """Obtiene ofertas de empleo por ubicación"""
    url = f"{BASE_URL}/jobs?limit={limit}&location={location}&offset=0"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def combinar_ofertas_con_nombres(ofertas, departamentos, provincias, distritos):
    """Reemplaza códigos por nombres"""
    resultados = []

    for job in ofertas:
        resultados.append({
            "id": job.get("id"),
            "titulo": job.get("title"),
            "empresa": job.get("company", {}).get("name"),
            "department": departamentos.get(job.get("department_code"), job.get("department_code")),
            "province": provincias.get(job.get("province_code"), job.get("province_code")),
            "district": distritos.get(job.get("district_code"), job.get("district_code")),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "date_posted": job.get("publication_date"),
        })

    return resultados


if __name__ == "__main__":
    print("Descargando catálogos...")
    departamentos, provincias, distritos = obtener_catalogos()

    print(" Descargando ofertas...")
    ofertas = obtener_ofertas(location="lima", limit=5)

    print(" Combinando resultados...")
    resultado_final = combinar_ofertas_con_nombres(ofertas, departamentos, provincias, distritos)

    print(json.dumps(resultado_final, indent=4, ensure_ascii=False))

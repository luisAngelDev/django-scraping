import requests
import json

BASE_URL = "https://mtpe-candidatos.empleosperu.gob.pe/api"

def obtener_catalogos():
    """Obtiene los nombres de departamentos, provincias y distritos"""
    url = f"{BASE_URL}/additionalDisplayData?language=es-pe"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    location_data = data.get("location", [])
    departamentos = {}
    provincias = {}
    distritos = {}

    for loc in location_data:
        level = loc.get("level")
        code = loc.get("code")
        name = loc.get("name")

        if level == "DEPARTMENT":
            departamentos[code] = name
        elif level == "PROVINCE":
            provincias[code] = name
        elif level == "DISTRICT":
            distritos[code] = name

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
        loc = job.get("location", {})
        resultados.append({
            "id": job.get("id"),
            "titulo": job.get("positionTitle"),
            "empresa": job.get("companyName"),
            "department": departamentos.get(loc.get("DEPARTMENT"), loc.get("DEPARTMENT")),
            "province": provincias.get(loc.get("PROVINCE"), loc.get("PROVINCE")),
            "district": distritos.get(loc.get("DISTRICT"), loc.get("DISTRICT")),
            "salary_min": job.get("offeredRemunerationPackages", [{}])[0].get("minimumAmount"),
            "salary_max": job.get("offeredRemunerationPackages", [{}])[0].get("maximumAmount"),
            "date_posted": job.get("datePosted"),
        })

    return resultados





if __name__ == "__main__":
    print("Descargando catálogos...")
    departamentos, provincias, distritos = obtener_catalogos()

    print("Descargando ofertas...")
    ofertas = obtener_ofertas(location="lima", limit=5)

    print("Combinando resultados...")
    resultado_final = combinar_ofertas_con_nombres(ofertas, departamentos, provincias, distritos)

    # Guardar en archivo
    with open("ofertas_lima.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print(f"Guardadas {len(resultado_final)} ofertas en 'ofertas_lima.json'")

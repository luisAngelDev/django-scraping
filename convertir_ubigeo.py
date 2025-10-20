import pandas as pd
import json

# Cambia este nombre por el archivo real
archivo = "Lista_Ubigeos_INEI.csv"  # o .csv

# Leer el archivo (Excel o CSV)
if archivo.endswith(".xlsx"):
    df = pd.read_excel(archivo, dtype=str)
else:
    df = pd.read_csv(archivo, dtype=str)

# Crear diccionario ubigeo
ubigeos = {}
for _, row in df.iterrows():
    codigo = row["UBIGEO_INEI"].strip()
    ubigeos[codigo] = {
        "departamento": row["DEPARTAMENTO"].strip(),
        "provincia": row["PROVINCIA"].strip(),
        "distrito": row["DISTRITO"].strip(),
    }

# Guardar en JSON
with open("ubigeos.json", "w", encoding="utf-8") as f:
    json.dump(ubigeos, f, ensure_ascii=False, indent=2)

print(f" Convertidos {len(ubigeos)} registros y guardados en ubigeos.json")

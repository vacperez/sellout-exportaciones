"""
Exporta los datos del Excel limpio a data/sellout.json.
Ejecutar cada vez que se agreguen datos nuevos al Excel:
    python exportar_json.py
Luego hacer commit y push a GitHub — Vercel lo publica automáticamente.
"""
import pandas as pd, json, sys
from datetime import date
from pathlib import Path

EXCEL = Path(input("Ruta al archivo Excel limpio: ").strip())
if not EXCEL.exists():
    print(f"Archivo no encontrado: {EXCEL}")
    sys.exit(1)

df = pd.read_excel(EXCEL, sheet_name="BASE_LIMPIA")
df["SELL OUT"] = pd.to_numeric(df["SELL OUT"], errors="coerce").fillna(0)
df = df[df["INCLUIR_EN_TOTAL_VENTA"] == True]
df["NOMBRE"] = df["NOMBRE"].str.replace("\xa0", " ", regex=False).str.strip()

MESES = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO",
         "SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

anios = sorted(df["AÑO"].dropna().unique())

mensual = {}
for a in anios:
    mensual[int(a)] = [round(df[(df["AÑO"]==a)&(df["MES"]==m)]["SELL OUT"].sum(), 2) for m in MESES]

pais_d = {}
for pais in sorted(df["PAIS"].dropna().unique()):
    pais_d[pais] = {int(a): round(df[(df["PAIS"]==pais)&(df["AÑO"]==a)]["SELL OUT"].sum(), 2) for a in anios}

NOMBRES_MAP = {
    "FERRETERIA ESPINOZA S.A.": "F. Espinoza",
    "DISTRIBUIDORA EL PACIFICO S.A.": "El Pacífico",
    "MEGA LINEAS S.A.": "Mega Líneas",
    "HECTOR JOSE BALLADARES ABARCA": "Balladares",
    "ALMACENES BOU": "Bou",
    "DISTRIBUIDORA ARSA S.A.": "ARSA",
    "CORPORACION DIEK S.A. DE C.V.": "DIEK",
    "VIDUC S.A. DE C.V.": "VIDUC",
    "WAKO IMPORTACIONES": "Wako",
    "FERRETERIA JENNY, S.A.": "F. Jenny"
}

cli_d = {}
for nombre, alias in NOMBRES_MAP.items():
    cli_d[alias] = {int(a): round(df[(df["NOMBRE"]==nombre)&(df["AÑO"]==a)]["SELL OUT"].sum(), 2) for a in anios}

meses_con_dato_ultimo_anio = [m for m in MESES if df[(df["AÑO"]==max(anios))&(df["MES"]==m)]["SELL OUT"].sum() > 0]
ultimo_mes = meses_con_dato_ultimo_anio[-1] if meses_con_dato_ultimo_anio else "ENERO"

data = {
    "ultima_actualizacion": str(date.today()),
    "ultimo_mes": ultimo_mes,
    "ultimo_anio": int(max(anios)),
    "mensual": mensual,
    "paises": pais_d,
    "clientes": cli_d
}

out = Path("data/sellout.json")
out.parent.mkdir(exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ data/sellout.json actualizado — {len(anios)} años, {len(pais_d)} países, hasta {ultimo_mes} {max(anios)}")
print("Siguiente paso: git add . && git commit -m 'datos' && git push")

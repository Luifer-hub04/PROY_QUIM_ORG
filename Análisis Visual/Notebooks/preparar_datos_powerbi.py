# -*- coding: utf-8 -*-
"""
Preparación del modelo de datos para Power BI
=============================================

Entrada : Datos/datos_power_bi.xlsx        (tabla cruda de CAS-SciFinder, 200 reacciones)
Salida  : Datos/datos_modelo_powerbi.xlsx  (3 tablas de Excel listas para Power BI)

    Compuestos      -> una fila por reactivo principal (Sus1) con sus propiedades limpias
    Reacciones      -> una fila por reacción (tabla de hechos)
    TiposReaccion   -> catálogo de mecanismos (SN, AN, Redox, ...)

Relaciones que se crean luego en Power BI:
    Reacciones[Compuesto]     *--1  Compuestos[Compuesto]
    Reacciones[Tipo_reaccion] *--1  TiposReaccion[Codigo]

Uso:  python preparar_datos_powerbi.py   (desde cualquier carpeta)
Librerías: pandas, numpy, openpyxl
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "Datos" / "datos_power_bi.xlsx"
SALIDA = RAIZ / "Datos" / "datos_modelo_powerbi.xlsx"

# ---------------------------------------------------------------------------
# 1. Compuestos asignados al grupo y su clasificación química
#    (Familia, grupo funcional y capacidad de formar puentes de hidrógeno)
# ---------------------------------------------------------------------------
ASIGNADOS = {
    # nombre en el Excel                : (Familia, Grupo funcional, Puentes de H)
    "Metilamina":                        ("Amina", "Amina primaria",   "Donador y aceptor"),
    "Bencidina":                         ("Amina", "Amina aromática",  "Donador y aceptor"),
    "Dimetilamina":                      ("Amina", "Amina secundaria", "Donador y aceptor"),
    "N-metiletanamina":                  ("Amina", "Amina secundaria", "Donador y aceptor"),
    "Trimetilamina":                     ("Amina", "Amina terciaria",  "Solo aceptor"),
    "N-isopropil-N-metilpropan-2amina":  ("Amina", "Amina terciaria",  "Solo aceptor"),
    "Azometina":                         ("Imina", "Imina",            "Donador y aceptor"),
    "Acetamida":                         ("Amida", "Amida primaria",   "Donador y aceptor"),
    "N-metilacetamida":                  ("Amida", "Amida secundaria", "Donador y aceptor"),
    "N,N-dimetilacetamida":              ("Amida", "Amida terciaria",  "Solo aceptor"),
    "Urea":                              ("Amida", "Urea (diamida)",   "Donador y aceptor"),
}

TIPOS_REACCION = [
    ("SN", "Sustitución nucleofílica", "Un nucleófilo (p. ej. el par libre del N) reemplaza a un grupo saliente."),
    ("AN", "Adición nucleofílica", "El nucleófilo se adiciona a un carbono electrófilo (C=O, C=N)."),
    ("SE", "Sustitución electrofílica", "Un electrófilo sustituye un H, típico de anillos aromáticos."),
    ("AE", "Adición electrofílica", "Un electrófilo se adiciona a un enlace múltiple C=C."),
    ("SR", "Sustitución radicalaria", "Sustitución por un mecanismo de radicales libres."),
    ("AR", "Adición radicalaria", "Adición a un enlace múltiple vía radicales libres."),
    ("E", "Eliminación", "Pérdida de una molécula pequeña formando un enlace múltiple."),
    ("Redox", "Óxido-reducción", "Cambio en el estado de oxidación (aminación reductiva, oxidaciones)."),
    ("Condensación", "Condensación", "Unión de dos moléculas con pérdida de agua u otra molécula pequeña."),
]

# Límites físicos razonables: valores fuera de rango son errores de digitación
# (p. ej. densidad 11725 en lugar de 1,1725) y se descartan (quedan vacíos).
LIMITES = {
    "PM_g_mol": (1, 2000),
    "pf_C": (-273, 1500),
    "Peb_C": (-273, 1500),
    "Densidad_g_cm3": (0, 5),
    "pKa": (-15, 60),
    "Momento_dipolar_D": (0, 15),
    "Solubilidad_g_L": (0, 5000),
}

SUPERINDICES = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def limpiar_numero(valor):
    """Convierte textos de CAS-SciFinder a número.

    Ejemplos:  '0,66_(25)' -> 0.66   '6,26_x_10⁻⁴' -> 0.000626   '>500,00' -> 500
               '163,00-165,00' -> 164 (promedio del rango)   '378,52±52,00' -> 378.52
               '45_(aprox.)' -> 45    'N/D' / 'Miscible' -> NaN
    """
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return np.nan
    if isinstance(valor, (int, float, np.number)):
        return float(valor)
    t = str(valor).translate(SUPERINDICES).replace("_", " ").strip()
    t = re.sub(r"\(.*?\)", "", t)                 # quita condiciones entre paréntesis
    t = t.replace("~", "").replace(">", "").replace("<", "").replace("°C", "").replace(" D", "")
    t = t.split("±")[0]                           # valor ± incertidumbre -> valor
    t = re.sub(r"(\d),(\d)", r"\1.\2", t)         # coma decimal -> punto
    cient = re.match(r"\s*(-?\d+(?:\.\d+)?)\s*x\s*10\s*(-?\d+)", t)
    if cient:
        return float(cient.group(1)) * 10 ** int(cient.group(2))
    rango = re.match(r"\s*(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)", t)
    if rango:
        return (float(rango.group(1)) + float(rango.group(2))) / 2
    num = re.search(r"-?\d+(?:\.\d+)?", t)
    return float(num.group()) if num else np.nan


def limpiar_nombre(nombre):
    """Normaliza nombres traducidos automáticamente ('norte' -> 'N', guiones bajos -> espacios)."""
    if not isinstance(nombre, str):
        return nombre
    t = nombre.replace("_", " ")
    t = re.sub(r"\bnorte\b", "N", t)
    t = re.sub(r"\s+,", ",", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def aplicar_limites(df):
    for col, (lo, hi) in LIMITES.items():
        if col in df:
            df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan
    return df


def tiempo_horas(tr):
    """Extrae el tiempo de reacción en horas de textos como '21h - 60', '30min - 0', '1,50 h TA'."""
    t = re.sub(r"(\d),(\d)", r"\1.\2", str(tr).replace("_", " ").lower())
    m = re.search(r"(\d+(?:\.\d+)?)\s*(h|min|d)\b", t)
    if not m:
        return np.nan
    factor = {"h": 1, "min": 1 / 60, "d": 24}[m.group(2)]
    return round(float(m.group(1)) * factor, 3)


def temperatura_c(tr):
    """Extrae la temperatura en °C. 'TA' / 'rt' (temperatura ambiente) = 25 °C."""
    t = re.sub(r"(\d),(\d)", r"\1.\2", str(tr).replace("_", " ").lower())
    t = re.sub(r"(\d\s*)(h|min|d)\s*-\s*", r"\1\2 ", t)   # '25h -40': el guion separa, no es signo
    m = re.findall(r"(-?\d+(?:\.\d+)?)\s*°c", t)
    if m:
        return float(m[-1])
    if re.search(r"\b(ta|rt|t\.a\.)\b", t):
        return 25.0
    sin_tiempo = re.sub(r"\d+(?:\.\d+)?\s*(h|min|d)\b", " ", t)
    m = re.search(r"-?\d+(?:\.\d+)?", sin_tiempo)
    return float(m.group()) if m else np.nan


def estado_25c(pf, peb):
    if pd.notna(peb) and peb < 25:
        return "Gas"
    if pd.notna(pf) and pf > 25:
        return "Sólido"
    if pd.notna(pf) or pd.notna(peb):
        return "Líquido"
    return "Sin dato"


def rango_pm(pm):
    if pd.isna(pm):
        return ("Sin dato", 9)
    for i, (hi, txt) in enumerate([(50, "< 50"), (100, "50 – 100"), (150, "100 – 150")]):
        if pm < hi:
            return (txt, i)
    return ("≥ 150", 3)


def main():
    crudo = pd.read_excel(ENTRADA)
    crudo["Sus1"] = crudo["Sus1"].astype(str).str.strip()

    # ---------------- Tabla de COMPUESTOS (dimensión) ----------------
    props = {
        "PM(g/mol)": "PM_g_mol", "pf(°C)": "pf_C", "P.eb(°C)": "Peb_C",
        "Densidad(g/cm3)": "Densidad_g_cm3", "pKa": "pKa",
        "Momento_dipolar": "Momento_dipolar_D", "S(g/L)": "Solubilidad_g_L",
    }
    comp = crudo[["Sus1", "CAS", *props]].rename(columns=props).copy()
    comp["Solubilidad_texto"] = comp["Solubilidad_g_L"].where(
        comp["Solubilidad_g_L"].astype(str).str.contains("Miscible", case=False, na=False))
    for col in props.values():
        comp[col] = comp[col].map(limpiar_numero)
    comp = aplicar_limites(comp)
    # Un compuesto aparece en varias reacciones: se toma su PRIMER valor reportado.
    # (No se usa la mediana porque en el Excel crudo hay celdas arrastradas que
    #  incrementan el valor: p. ej. P.eb de metilamina -6.3, -5.3, -4.3, ...)
    agg = {c: "first" for c in props.values()}
    agg.update({"CAS": "first", "Solubilidad_texto": "first"})
    comp = comp.groupby("Sus1", as_index=False).agg(agg)

    clasif = comp["Sus1"].map(ASIGNADOS)
    comp["Familia"] = clasif.map(lambda x: x[0] if isinstance(x, tuple) else "Otros reactivos")
    comp["Grupo_funcional"] = clasif.map(lambda x: x[1] if isinstance(x, tuple) else "Otros reactivos")
    comp["Puentes_H"] = clasif.map(lambda x: x[2] if isinstance(x, tuple) else "No clasificado")
    comp["Asignado"] = np.where(comp["Sus1"].isin(ASIGNADOS), "Sí", "No")
    comp["Estado_25C"] = [estado_25c(a, b) for a, b in zip(comp["pf_C"], comp["Peb_C"])]
    rangos = comp["PM_g_mol"].map(rango_pm)
    comp["Rango_PM"] = rangos.map(lambda r: r[0])
    comp["Rango_PM_Orden"] = rangos.map(lambda r: r[1])
    comp["Solubilidad_texto"] = comp["Solubilidad_texto"].fillna("")
    comp.insert(0, "Compuesto", comp.pop("Sus1").map(limpiar_nombre))
    comp = comp[["Compuesto", "CAS", "Familia", "Grupo_funcional", "Puentes_H", "Asignado",
                 "Estado_25C", "Rango_PM", "Rango_PM_Orden", "PM_g_mol", "pf_C", "Peb_C",
                 "Densidad_g_cm3", "Solubilidad_g_L", "Solubilidad_texto", "pKa", "Momento_dipolar_D"]]

    # ---------------- Tabla de REACCIONES (hechos) ----------------
    r = pd.DataFrame({
        "ID_Reaccion": range(1, len(crudo) + 1),
        "CAS_reaccion": crudo["CAS_reacción"],
        "Nombre_reaccion": crudo["Nombre_reacción"].map(limpiar_nombre),
        "Tipo_reaccion": crudo["Tipo_reaccion"].str.strip(),
        "Compuesto": crudo["Sus1"].map(limpiar_nombre),
        "Reactivo_2": crudo["Reactivo_2"].map(limpiar_nombre),
        "Producto": crudo["Pro1"].map(limpiar_nombre),
        "PM_producto": crudo["PM4(g/mol)"].map(limpiar_numero),
        "Peb_producto_C": crudo["P.eb4(°C)"].map(limpiar_numero),
        "Catalizador": crudo["Catalizador_1"].map(limpiar_nombre),
        "Solvente": crudo["Solvente_1"].map(limpiar_nombre),
        "Medio": crudo["Medio"].fillna("No reportado"),
        "Condiciones": crudo["TR"].astype(str).map(limpiar_nombre),
        "Tiempo_h": crudo["TR"].map(tiempo_horas),
        "Temperatura_C": crudo["TR"].map(temperatura_c),
    })
    r["Usa_catalizador"] = np.where(r["Catalizador"].notna(), "Sí", "No")
    r["Catalizador"] = r["Catalizador"].fillna("Sin catalizador")
    r["Solvente"] = r["Solvente"].fillna("No reportado")
    r["Reactivo_2"] = r["Reactivo_2"].fillna("")
    r.loc[(r["PM_producto"] < 1) | (r["PM_producto"] > 3000), "PM_producto"] = np.nan
    r.loc[(r["Peb_producto_C"] < -273) | (r["Peb_producto_C"] > 1500), "Peb_producto_C"] = np.nan
    r.loc[(r["Temperatura_C"] < -100) | (r["Temperatura_C"] > 400), "Temperatura_C"] = np.nan

    tipos = pd.DataFrame(TIPOS_REACCION, columns=["Codigo", "Tipo_reaccion_nombre", "Descripcion"])

    # ---------------- Escritura en Excel con formato Tabla ----------------
    with pd.ExcelWriter(SALIDA, engine="openpyxl") as w:
        for nombre, df in [("Compuestos", comp), ("Reacciones", r), ("TiposReaccion", tipos)]:
            df.to_excel(w, sheet_name=nombre, index=False)
    wb = load_workbook(SALIDA)
    for ws in wb.worksheets:
        tabla = Table(displayName=ws.title, ref=ws.dimensions)
        tabla.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(tabla)
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(45, max(12, len(str(col[0].value)) + 4))
    wb.save(SALIDA)

    print(f"Compuestos: {len(comp)} ({(comp['Asignado'] == 'Sí').sum()} asignados)")
    print(f"Reacciones: {len(r)}  |  Tipos de reacción: {len(tipos)}")
    print(f"Archivo generado: {SALIDA}")
    return comp, r


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()

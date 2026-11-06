# -*- coding: utf-8 -*-
"""
Generación local de TODAS las gráficas del notebook de Colab (Graficas_Def.ipynb)
===============================================================================

Reproduce el mismo análisis del notebook, pero en vez de mostrarlas en pantalla
las guarda como archivos:

    Análisis Visual/Graficas/   -> PNG (300 dpi) + HTML interactivo de Altair
    Documentación/imagenes/     -> copia de los PNG para el informe LaTeX

Diferencias con el notebook de Colab (correcciones):
  1. Lee el Excel del repositorio (Datos/datos_power_bi.xlsx = DATOS_limpio.xlsx)
     en lugar de Google Drive.
  2. Se corrige la coma faltante en la lista de compuestos
     ("Azometina", "N-metiletanamina" estaban unidos en un solo texto).
  3. Las frecuencias de 'Medio' y 'Tipo_reaccion' se calculan ANTES de la gráfica
     de barras de Altair (en el .py exportado estaban después y daba NameError).

Uso:  python generar_graficas.py
Librerías: pandas, numpy, matplotlib, seaborn, altair, plotly, vl-convert-python, kaleido
"""
import shutil
import sys
from pathlib import Path

import altair as alt
import matplotlib
matplotlib.use("Agg")                     # sin ventana: sólo guardar archivos
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "Datos" / "datos_power_bi.xlsx"
SALIDA = RAIZ / "Análisis Visual" / "Graficas"
LATEX = RAIZ / "Documentación" / "imagenes"
SALIDA.mkdir(parents=True, exist_ok=True)
LATEX.mkdir(parents=True, exist_ok=True)

generadas = []


def guardar(nombre, fig=None):
    """Guarda la figura actual de Matplotlib/Seaborn en PNG y la copia al informe."""
    fig = fig or plt.gcf()
    ruta = SALIDA / f"{nombre}.png"
    fig.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close("all")
    shutil.copy(ruta, LATEX / ruta.name)
    generadas.append(ruta.name)


def guardar_altair(nombre, chart):
    """Guarda un gráfico de Altair como PNG (informe) y HTML (interactivo)."""
    chart.save(SALIDA / f"{nombre}.html")
    chart.save(SALIDA / f"{nombre}.png", scale_factor=3)
    shutil.copy(SALIDA / f"{nombre}.png", LATEX / f"{nombre}.png")
    generadas.extend([f"{nombre}.png", f"{nombre}.html"])


def limpiar_columna(serie):
    """Mismo método del notebook: coma -> punto y se extrae el primer número."""
    s = serie.astype(str).str.replace(",", ".", regex=False)
    s = s.str.extract(r"([-+]?\d*\.?\d+)")[0]
    return pd.to_numeric(s, errors="coerce")


# ---------------------------------------------------------------- DATOS
df = pd.read_excel(DATOS)
print("Tamaño del conjunto de datos:", df.shape)

compounds = ["Metilamina", "Bencidina", "N-isopropil-N-metilpropan-2amina", "Azometina",
             "N-metiletanamina", "Dimetilamina", "Trimetilamina", "Acetamida",
             "N-metilacetamida", "N,N-dimetilacetamida", "Urea"]

df = df[df["Sus1"].isin(compounds)].reset_index(drop=True)
print(f"Filas conservadas: {len(df)}")
print(df["Sus1"].value_counts().to_string())

params = df[["PM(g/mol)", "pf(°C)", "P.eb(°C)", "Densidad(g/cm3)", "pKa", "Momento_dipolar", "S(g/L)"]]
params_clean = params.apply(limpiar_columna)

# ---------------------------------------------------------------- 1-2. CORRELACIÓN
corr = params_clean.corr(method="spearman")

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlación de Spearman")
guardar("01_heatmap_spearman")

cg = sns.clustermap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1)
guardar("02_clustermap_spearman", cg.figure)

# ---------------------------------------------------------------- 3-6. REGRESIONES
sns.set_theme(style="whitegrid")
regresiones = [
    ("03_reg_pf_vs_densidad", "pf(°C)", "Densidad(g/cm3)",
     "Punto de Fusión vs Densidad", "Punto de Fusión - pf (°C)", "Densidad (g/cm3)"),
    ("04_reg_peb_vs_densidad", "P.eb(°C)", "Densidad(g/cm3)",
     "Punto de Ebullición vs Densidad", "Punto de Ebullición - P.eb (°C)", "Densidad (g/cm3)"),
    ("05_reg_pf_vs_peb", "pf(°C)", "P.eb(°C)",
     "Punto de Fusión vs Punto de Ebullición", "Punto de Fusión - pf (°C)", "Punto de Ebullición - P.eb (°C)"),
    ("06_reg_dipolo_vs_peb", "Momento_dipolar", "P.eb(°C)",
     "Momento Dipolar vs Punto de Ebullición", "Momento Dipolar (D)", "Punto de Ebullición - P.eb (°C)"),
]
for nombre, x, y, titulo, xl, yl in regresiones:
    plt.figure(figsize=(8, 6))
    sns.regplot(data=params_clean, x=x, y=y,
                scatter_kws={"alpha": 0.6, "color": "#d95f02", "s": 50},
                line_kws={"color": "#1b9e77", "linewidth": 2})
    plt.title(f"Gráfico de Dispersión: {titulo}", fontsize=14, pad=15)
    plt.xlabel(xl, fontsize=12)
    plt.ylabel(yl, fontsize=12)
    plt.tight_layout()
    guardar(nombre)

# ---------------------------------------------------------------- 7-8. TR por tipo y medio
df_filtrado = df[["Tipo_reaccion", "Medio"]].copy()
df_filtrado["TR"] = limpiar_columna(df["TR"])
df_tr = df_filtrado.dropna(subset=["Tipo_reaccion", "Medio", "TR"])

plt.figure(figsize=(12, 6))
sns.violinplot(data=df_tr, x="Tipo_reaccion", y="TR", hue="Medio", palette="viridis", inner="quartile")
plt.title("Distribución de TR por Tipo de Reacción y Medio", fontsize=14, pad=15)
plt.xlabel("Tipo de Reacción", fontsize=12)
plt.ylabel("TR", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Medio", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
guardar("07_violin_TR_tipo_medio")

ax = df_tr.boxplot(by=["Tipo_reaccion", "Medio"], column=["TR"], figsize=(14, 7), grid=True, rot=45)
ax.set_title("Diagrama de Cajas y Bigotes de TR por Tipo de Reacción y Medio", fontsize=14, pad=15)
plt.suptitle("")
ax.set_xlabel("Grupo (Tipo de Reacción, Medio)", fontsize=12)
ax.set_ylabel("TR", fontsize=12)
plt.tight_layout()
guardar("08_boxplot_TR_tipo_medio", ax.figure)

# ---------------------------------------------------------------- 9. FRECUENCIAS (Altair)
FrecuenciaMedio = df_filtrado["Medio"].value_counts()
FrecuenciaTipo_reaccion = df_filtrado["Tipo_reaccion"].value_counts()
print("Frecuencia de Medio:\n", FrecuenciaMedio.to_string())
print("Frecuencia de Tipo de reacción:\n", FrecuenciaTipo_reaccion.to_string())

df_freq_medio = FrecuenciaMedio.reset_index()
df_freq_medio.columns = ["Valor", "Frecuencia"]
df_freq_medio["Variable"] = "Medio"
df_freq_tipo = FrecuenciaTipo_reaccion.reset_index()
df_freq_tipo.columns = ["Valor", "Frecuencia"]
df_freq_tipo["Variable"] = "Tipo de reacción"
df_plot = pd.concat([df_freq_medio, df_freq_tipo])

chart = (
    alt.Chart(df_plot)
    .mark_bar()
    .encode(
        x=alt.X("Valor:N", title="Categoría", sort="-y"),
        y=alt.Y("Frecuencia:Q", title="Frecuencia"),
        color=alt.Color("Variable:N", title="Variable/Atributo", scale=alt.Scale(scheme="tableau10")),
        xOffset="Variable:N",
        tooltip=["Variable", "Valor", "Frecuencia"],
    )
    .properties(title="Comparativa de Frecuencias: Medio vs Tipo de reacción", width=500, height=350)
    .interactive()
)
guardar_altair("09_frecuencias_medio_tipo", chart)

# ---------------------------------------------------------------- 10. DONA (Altair)
df_donut = df_tr.copy()
df_donut["Categoria_Combinada"] = df_donut["Tipo_reaccion"] + " (" + df_donut["Medio"] + ")"
df_grouped = df_donut.groupby("Categoria_Combinada", as_index=False)["TR"].sum()

grafico_altair = (
    alt.Chart(df_grouped)
    .mark_arc(innerRadius=60, outerRadius=100)
    .encode(
        theta=alt.Theta(field="TR", type="quantitative", title="Suma de TR"),
        color=alt.Color(field="Categoria_Combinada", type="nominal", title="Grupo (Reacción, Medio)"),
        tooltip=["Categoria_Combinada", "TR"],
    )
    .properties(title="Distribución de TR por Grupo (Reacción, Medio)", width=350, height=350)
    .interactive()
)
guardar_altair("10_dona_TR_grupo", grafico_altair)

# ---------------------------------------------------------------- 11-13. PLOTLY (interactivas)
# Una fila por compuesto (primer valor reportado) + clasificación química,
# para inspeccionar cada molécula al pasar el cursor (hover).
CLASIFICACION = {
    "Metilamina": ("Amina primaria", "Donador y aceptor"),
    "Bencidina": ("Amina aromática", "Donador y aceptor"),
    "Dimetilamina": ("Amina secundaria", "Donador y aceptor"),
    "N-metiletanamina": ("Amina secundaria", "Donador y aceptor"),
    "Trimetilamina": ("Amina terciaria", "Solo aceptor"),
    "N-isopropil-N-metilpropan-2amina": ("Amina terciaria", "Solo aceptor"),
    "Azometina": ("Imina", "Donador y aceptor"),
    "Acetamida": ("Amida primaria", "Donador y aceptor"),
    "N-metilacetamida": ("Amida secundaria", "Donador y aceptor"),
    "N,N-dimetilacetamida": ("Amida terciaria", "Solo aceptor"),
    "Urea": ("Urea (diamida)", "Donador y aceptor"),
}
datos_px = params_clean.copy()
datos_px["Compuesto"] = df["Sus1"]
datos_px = datos_px.groupby("Compuesto", as_index=False).first()
datos_px["Grupo funcional"] = datos_px["Compuesto"].map(lambda c: CLASIFICACION[c][0])
datos_px["Puentes de H"] = datos_px["Compuesto"].map(lambda c: CLASIFICACION[c][1])
etiquetas = {"PM(g/mol)": "Peso molecular (g/mol)", "P.eb(°C)": "Punto de ebullición (°C)",
             "pf(°C)": "Punto de fusión (°C)", "Momento_dipolar": "Momento dipolar (D)",
             "Densidad(g/cm3)": "Densidad (g/cm³)", "S(g/L)": "Solubilidad (g/L)"}
hover = {"PM(g/mol)": True, "P.eb(°C)": True, "pf(°C)": True, "Densidad(g/cm3)": True,
         "pKa": True, "Momento_dipolar": True, "S(g/L)": True}


NOMBRE_CORTO = {  # saltos de línea para que los nombres largos no invadan otros puntos
    "N-isopropil-N-metilpropan-2amina": "N-isopropil-N-metil-<br>propan-2-amina",
    "N,N-dimetilacetamida": "N,N-dimetil-<br>acetamida",
}


def guardar_plotly(nombre, fig, ancho=640, alto=540):
    """Guarda un gráfico de Plotly como HTML interactivo y PNG.

    El PNG se exporta al tamaño aproximado de una columna del informe
    (640 px de ancho) con letra grande, para que al imprimirlo a ancho de
    columna el texto quede legible (≈ 7 pt) y no se solape.
    """
    fig.update_layout(
        template="plotly_white", font=dict(size=15, family="Arial"),
        title=dict(font=dict(size=16), x=0.02, xanchor="left"),
        margin=dict(l=70, r=25, t=60, b=40),
    )
    if fig.layout.legend.y is None:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5))
    fig.update_layout(legend_font_size=13)
    fig.write_html(SALIDA / f"{nombre}.html", include_plotlyjs="cdn")
    fig.write_image(SALIDA / f"{nombre}.png", width=ancho, height=alto, scale=4)
    shutil.copy(SALIDA / f"{nombre}.png", LATEX / f"{nombre}.png")
    generadas.extend([f"{nombre}.png", f"{nombre}.html"])


def etiquetar(fig, datos, x, y, desplazamientos, log_y=False):
    """Pone el nombre de cada compuesto con una flecha corta.

    desplazamientos: {compuesto: (dx, dy)} en píxeles respecto al punto; así se
    ubica cada etiqueta a mano donde no choca con otra.
    """
    for _, fila in datos.iterrows():
        dx, dy = desplazamientos.get(fila["Compuesto"], (0, -30))
        fig.add_annotation(
            x=fila[x], y=np.log10(fila[y]) if log_y else fila[y],
            text=NOMBRE_CORTO.get(fila["Compuesto"], fila["Compuesto"]),
            ax=dx, ay=dy, showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor="#7F8C8D",
            font=dict(size=13, color="#2C3E50"), bgcolor="rgba(255,255,255,0.85)", borderpad=1,
        )


# 11. Burbujas: PM vs P.eb, tamaño = densidad, color = capacidad de puente de H
burbujas = datos_px.dropna(subset=["PM(g/mol)", "P.eb(°C)"]).copy()
burbujas["Tamaño"] = burbujas["Densidad(g/cm3)"].fillna(burbujas["Densidad(g/cm3)"].median())
fig = px.scatter(burbujas, x="PM(g/mol)", y="P.eb(°C)", size="Tamaño", color="Puentes de H",
                 hover_name="Compuesto", hover_data=hover, labels=etiquetas,
                 size_max=26, color_discrete_sequence=["#1b9e77", "#d95f02"],
                 title="PM vs punto de ebullición (tamaño = densidad)")
etiquetar(fig, burbujas, "PM(g/mol)", "P.eb(°C)", {
    "Bencidina": (-70, 25), "Acetamida": (-55, -35), "N-metilacetamida": (45, -40),
    "Urea": (-60, 20), "N,N-dimetilacetamida": (80, -15), "N-isopropil-N-metilpropan-2amina": (55, 55),
    "N-metiletanamina": (70, -30), "Trimetilamina": (75, 15), "Dimetilamina": (-15, -50),
    "Metilamina": (5, 40),
})
fig.update_xaxes(range=[15, 200])
fig.update_yaxes(range=[-70, 450])
guardar_plotly("11_plotly_burbujas_pm_peb", fig)

# 12. 3D: PM, P.eb y momento dipolar por grupo funcional
tres_d = datos_px.dropna(subset=["PM(g/mol)", "P.eb(°C)", "Momento_dipolar"])
fig = px.scatter_3d(tres_d, x="PM(g/mol)", y="Momento_dipolar", z="P.eb(°C)", color="Grupo funcional",
                    hover_name="Compuesto", hover_data=hover,
                    labels={"PM(g/mol)": "PM (g/mol)", "Momento_dipolar": "μ (D)", "P.eb(°C)": "P.eb (°C)"},
                    title="PM, momento dipolar y punto de ebullición")
fig.update_traces(marker=dict(size=6, line=dict(width=1, color="DarkSlateGrey")))
fig.update_layout(scene=dict(camera=dict(eye=dict(x=1.6, y=-1.6, z=0.75), center=dict(x=0, y=0, z=-0.08)),
                             domain=dict(x=[0, 1], y=[0.2, 1]),
                             xaxis=dict(title_font_size=14, tickfont_size=11),
                             yaxis=dict(title_font_size=14, tickfont_size=11),
                             zaxis=dict(title_font_size=14, tickfont_size=11)))
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5))
guardar_plotly("12_plotly_3d_pm_dipolo_peb", fig, alto=560)

# 13. Densidad vs solubilidad (escala logarítmica: la solubilidad abarca varios órdenes)
dens_sol = datos_px.dropna(subset=["Densidad(g/cm3)", "S(g/L)"])
dens_sol = dens_sol[dens_sol["S(g/L)"] > 0]
fig = px.scatter(dens_sol, x="Densidad(g/cm3)", y="S(g/L)", color="Grupo funcional",
                 hover_name="Compuesto", hover_data=hover, labels=etiquetas, log_y=True,
                 title="Densidad vs solubilidad en agua (eje log)")
fig.update_traces(marker=dict(size=13, line=dict(width=1, color="white")))
etiquetar(fig, dens_sol, "Densidad(g/cm3)", "S(g/L)", {
    "Metilamina": (45, -30), "Trimetilamina": (10, 40), "Dimetilamina": (70, 15),
    "Acetamida": (-20, -35), "Bencidina": (-55, -25), "Urea": (-45, 30),
}, log_y=True)
fig.update_xaxes(range=[0.55, 1.42])
fig.update_yaxes(range=[-1, 3.7], dtick=1)
guardar_plotly("13_plotly_densidad_solubilidad", fig)

if __name__ == "__main__":
    print(f"\n{len(generadas)} archivos generados en {SALIDA}:")
    for g in generadas:
        print("  -", g)

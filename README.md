<div align="center">

# 🧪 Proyecto Final de Química Orgánica
### Relación estructura–propiedad en aminas y amidas

**Ingeniería Ambiental · FAMARENA – Universidad Distrital · QUIMORG 2026-III**

<!-- Navegación rápida por el repositorio -->
[![Datos](https://img.shields.io/badge/📁_Datos-Excel_CAS--SciFinder-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](Datos/)
[![Análisis Visual](https://img.shields.io/badge/📊_Análisis_Visual-Python_+_Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](An%C3%A1lisis%20Visual/)
[![Documentación](https://img.shields.io/badge/📄_Documentación-LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)](Documentaci%C3%B3n/)

<!-- Accesos directos a los entregables -->
[![Abrir en Colab](https://img.shields.io/badge/Abrir_en-Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/drive/1FPoSINbOlCPPnTC1RbqM-ZbU4wjF3MK5)
[![Dashboard Power BI](https://img.shields.io/badge/Dashboard-Power_BI_Service-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](#-dashboard-power-bi)
[![Informe PDF](https://img.shields.io/badge/Informe-PDF-B31B1B?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](Documentaci%C3%B3n/main.pdf)
[![Tablero de tareas](https://img.shields.io/badge/GitHub-Projects-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Luifer-hub04/PROY_QUIM_ORG/projects)

</div>

---

## 📌 Descripción

Estudio de las propiedades fisicoquímicas de **aminas** (metilamina, dimetilamina,
trimetilamina, N-metiletanamina, bencidina) y **amidas** (acetamida,
N-metilacetamida, N,N-dimetilacetamida, urea) obtenidas en **CAS-SciFinder**.
Se relacionan peso molecular, punto de fusión, punto de ebullición, densidad,
pKa, momento dipolar y solubilidad para explicar el efecto de los **puentes de
hidrógeno**, el **grado de sustitución del nitrógeno** y la **resonancia del
grupo amida**.

## 🗂️ Estructura del repositorio

```
PROY_QUIM_ORG/
├── Datos/                      → Base de datos de CAS-SciFinder (Excel en formato Tabla)
│   ├── datos_power_bi.xlsx         → datos crudos/limpios usados en Colab
│   └── datos_modelo_powerbi.xlsx   → modelo procesado (Compuestos, Reacciones, TiposReaccion)
├── Análisis Visual/
│   ├── Notebooks/              → Colab (.ipynb/.py) y script de preparación para Power BI
│   ├── Graficas/               → Figuras exportadas (Seaborn / Matplotlib)
│   └── Power BI/               → Dashboard interactivo (.pbip / .pbix)
└── Documentación/              → Informe científico en LaTeX
    ├── main.tex                → Archivo maestro (une las partes)
    ├── Sara/sara.tex           → Introducción, Marco Teórico, Tabla de datos
    ├── Valentina/valentina.tex → Metodología, Análisis gráfico, Conclusiones
    ├── references.bib          → Bibliografía (BibLaTeX + Biber)
    ├── imagenes/               → Figuras usadas en el informe
    └── main.pdf                → Informe compilado
```

## 🛠️ Herramientas

| Etapa | Herramienta |
|---|---|
| Recolección de datos | CAS-SciFinder · Microsoft Excel (formato Tabla) |
| Limpieza y análisis | Google Colab · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Altair |
| Informe | LaTeX (MiKTeX + TeXstudio / Overleaf) · BibLaTeX |
| Dashboard | Power BI Desktop · Power Query · DAX · Power BI Service |
| Control de versiones | Git · GitHub · GitHub Projects |

## 📊 Dashboard Power BI

> 🔗 **Enlace a Power BI Service:** _pendiente de publicar_
> <!-- Reemplazar por el enlace de "Publicar en la web" o del área de trabajo -->

**Abrir el dashboard en cualquier computador** (Power BI Desktop, con internet):

1. Descargar el repositorio (`git clone` / `git pull`).
2. Abrir `Análisis Visual/Power BI/Dashboard_Quimica_Organica.pbip`.
3. Inicio → **Actualizar**: los datos se descargan del Excel publicado en GitHub,
   sin importar en qué carpeta esté el proyecto.
4. Si pregunta cómo conectarse a `raw.githubusercontent.com`: **Anónimo → Conectar**.

Sin internet: Transformar datos → **Editar parámetros** → `RutaDatos` = ruta local de
`Datos\datos_modelo_powerbi.xlsx` → Actualizar. Más detalles en el
[README de Power BI](An%C3%A1lisis%20Visual/Power%20BI/README.md).

## 📄 Compilar el informe

Desde la carpeta `Documentación/`:

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## 👥 Integrantes

| Integrante | Responsabilidad |
|---|---|
| Sara [Apellido] | Introducción, Marco Teórico, Tabla de datos |
| Valentina [Apellido] | Metodología, Análisis gráfico, Conclusiones |
| [Tercer integrante] | CAS-SciFinder, Power BI, Repositorio |

---

<div align="center">
<sub>Entrega: 16 de noviembre de 2026, 18:00 · Sustentación: 19, 23 o 26 de noviembre</sub>
</div>

# Guía del equipo: qué se hizo y cómo funciona

Documento para Sara, Valentina y el resto del grupo. Explica cada paso realizado,
por qué se hizo así y cómo usarlo. Sirve también para responder preguntas del
profesor sobre el repositorio y el informe.

---

## 1. Instalación de herramientas (en el computador del repositorio)

| Herramienta | Versión | Cómo se instaló | Para qué sirve |
|---|---|---|---|
| **MiKTeX** | 25.12 | `winget install MiKTeX.MiKTeX` | Distribución de LaTeX: trae `pdflatex` (compila) y `biber` (bibliografía). |
| **Power BI Desktop** | 2.159 | Microsoft Store (`winget install 9NTXR16HNW1T`) | Diseñar el dashboard `.pbix`. |

- MiKTeX quedó configurado con **instalación automática de paquetes**: si el
  documento usa un paquete que no está, MiKTeX lo descarga solo al compilar.
- Recomendado: instalar **TeXstudio** (https://www.texstudio.org/) como editor
  visual. Cada integrante debe instalar MiKTeX + TeXstudio en su propio equipo,
  o usar **Overleaf**.

## 2. Configuración de Git

En la carpeta del proyecto se ejecutó:

```bash
git init -b main
git config --local user.name "Luifer-hub04"
git config --local user.email "Luifer-hub04@users.noreply.github.com"
git config --local credential.https://github.com.username "Luifer-hub04"
git remote add origin https://github.com/Luifer-hub04/PROY_QUIM_ORG.git
```

- `--local` significa que esa identidad **sólo aplica a esta carpeta**, no a todo el computador.
- **No se guardó ninguna contraseña.** GitHub ya no acepta contraseñas desde la
  consola; al hacer el primer `git push` se abre el navegador para iniciar
  sesión (Git Credential Manager) y el acceso queda guardado de forma segura.

> ⚠️ **Muy importante para la nota (20 %):** el profesor revisa los *commits* de
> cada integrante. Cada una debe **clonar el repositorio con su propia cuenta**
> y subir sus propios cambios. No suban todo desde una sola cuenta.

### Flujo de trabajo para cada integrante

```bash
# Una sola vez: descargar el repositorio
git clone https://github.com/Luifer-hub04/PROY_QUIM_ORG.git
cd PROY_QUIM_ORG
git config user.name "TuUsuarioDeGitHub"
git config user.email "tu_correo_institucional"

# Cada vez que vayas a trabajar
git pull                                  # traer lo último del grupo
# ... editar tu archivo (sara.tex o valentina.tex) ...
git add "Documentación/Sara/sara.tex"
git commit -m "Sara: redacta introducción"
git push
```

Luifer-hub04 (dueño del repo) debe invitar a cada integrante en
**Settings → Collaborators** para que puedan hacer `push`.

## 3. Estructura de carpetas (exigida por la rúbrica)

```
Datos/              → Excel de CAS-SciFinder en formato Tabla
Análisis Visual/    → Notebook de Colab, gráficas exportadas y .pbix de Power BI
Documentación/      → Informe LaTeX modular + PDF compilado
README.md           → Portada del repositorio con botones (badges) de navegación
```

Qué se movió y por qué:

| Archivo original | Nuevo lugar | Motivo |
|---|---|---|
| `datos_power_bi.xlsx` | `Datos/` | Base de datos limpia del proyecto (es el mismo archivo que el notebook de Colab lee como `DATOS_limpio.xlsx` desde Google Drive). |
| `gráficas_def` (sin extensión) | `Análisis Visual/Notebooks/Graficas_Def.ipynb` | Era un notebook de Colab sin extensión; con `.ipynb` GitHub lo muestra correctamente. Se quitaron tildes del nombre para evitar problemas en LaTeX y en la consola. |
| `gráficas_def.py` | `Análisis Visual/Notebooks/Graficas_Def.py` | Versión en texto plano del notebook. |
| `main.tex`, `references.bib` | `Documentación/` | Fuentes del informe. |
| `Figure_1…`, `Figure_2…` | `Documentación/imagenes/ejemplos_plantilla/` | Eran imágenes de ejemplo de la plantilla (IA vs. energía renovable), no del proyecto. Ya no se usan en el informe. |
| `main-blx.bib` | eliminado | Archivo auxiliar que BibLaTeX regenera solo al compilar. |

### Gráficas del notebook de Colab

Todas las gráficas del notebook se regeneran en el computador con el script
`Análisis Visual/Notebooks/generar_graficas.py` (mismo código de Colab, pero
guarda archivos en vez de mostrarlos):

```bash
python "Análisis Visual/Notebooks/generar_graficas.py"
```

Guarda PNG a 300 dpi en `Análisis Visual/Graficas/` y los copia a
`Documentación/imagenes/`. Las de Altair se guardan además en **HTML
interactivo** (se abren con doble clic en el navegador y tienen tooltip).

Correcciones respecto al `.py` exportado de Colab:
- lee `Datos/datos_power_bi.xlsx` en vez de Google Drive;
- se agregó la coma faltante entre `"Azometina"` y `"N-metiletanamina"`;
- las frecuencias de `Medio` y `Tipo_reaccion` se calculan antes de la gráfica
  de barras (en el `.py` estaban después y Python daría `NameError`).

**Plotly (exigido por la rúbrica):** se agregaron 3 gráficas con
`plotly.express`, tanto al script como al final del notebook
`Graficas_Def.ipynb` (5 celdas nuevas: título, preparación de datos y 3
gráficas). En Colab, ejecutar el notebook completo y las gráficas aparecen al
final; se pueden rotar, ampliar y al pasar el cursor muestran todas las
propiedades del compuesto. Usan **una fila por compuesto** (primer valor
reportado), a diferencia de las regresiones de Seaborn que usan todas las filas.

| Gráfica Plotly | Qué demuestra |
|---|---|
| Burbujas PM vs P.eb (tamaño = densidad, color = puentes de H) | A igual PM, los compuestos con N–H hierven más alto (trimetilamina 2,8 °C vs N-metiletanamina 36,5 °C) |
| 3D PM × momento dipolar × P.eb | Amidas/urea forman un grupo aparte: alto dipolo **y** alto P.eb |
| Densidad vs solubilidad (eje log) | Aminas pequeñas muy solubles; bencidina (aromática) casi insoluble |

> **Versión para el PDF:** en `generar_graficas.py` los PNG de Plotly se exportan
> al tamaño de una columna (640 px, letra 13–16) y cada nombre de compuesto va
> con una flecha corta ubicada a mano (función `etiquetar`) para que no se
> solapen ni queden cortados al imprimir. El HTML interactivo no cambia.
>
> Para subir el notebook actualizado a Colab: Archivo → Subir notebook →
> `Análisis Visual/Notebooks/Graficas_Def.ipynb`.

| Archivo | Contenido |
|---|---|
| `01_heatmap_spearman.png` | Matriz de correlación de Spearman |
| `02_clustermap_spearman.png` | Agrupamiento jerárquico de la correlación |
| `03_reg_pf_vs_densidad.png` | Regresión: punto de fusión vs densidad |
| `04_reg_peb_vs_densidad.png` | Regresión: punto de ebullición vs densidad |
| `05_reg_pf_vs_peb.png` | Regresión: punto de fusión vs ebullición |
| `06_reg_dipolo_vs_peb.png` | Regresión: momento dipolar vs ebullición |
| `07_violin_TR_tipo_medio.png` | Violín de TR por tipo de reacción y medio |
| `08_boxplot_TR_tipo_medio.png` | Cajas y bigotes de TR por tipo de reacción y medio |
| `09_frecuencias_medio_tipo.png` / `.html` | Frecuencias de tipo de reacción y medio (Altair) |
| `10_dona_TR_grupo.png` / `.html` | Dona de TR por grupo (reacción, medio) (Altair) |
| `11_plotly_burbujas_pm_peb.png` / `.html` | Burbujas PM vs P.eb por puentes de H (Plotly) |
| `12_plotly_3d_pm_dipolo_peb.png` / `.html` | Dispersión 3D PM, momento dipolar, P.eb (Plotly) |
| `13_plotly_densidad_solubilidad.png` / `.html` | Densidad vs solubilidad, eje log (Plotly) |

## 4. Informe LaTeX modular

### Cómo funciona

`main.tex` es el **archivo maestro**: contiene la configuración (paquetes,
márgenes, encabezados, título, resumen) y **une** las partes con `\input`:

```latex
\input{Sara/sara}             % Introducción, Marco Teórico, Tabla de datos
\input{Valentina/valentina}   % Metodología, Análisis gráfico, Conclusiones
```

- Se usó `\input` y no `\include` porque `\include` fuerza un salto de página,
  lo que rompería el diseño a dos columnas.
- Cada integrante edita **sólo su archivo**, así no hay conflictos en GitHub.
- `sara.tex` y `valentina.tex` **no** llevan `\documentclass` ni
  `\begin{document}`: son fragmentos que se pegan dentro de `main.tex`.

### Cambios hechos a la plantilla del docente

Se respetó la plantilla oficial (JCSA) y sólo se ajustó:

1. Se quitó `lipsum` (texto de relleno) y se eliminó una carga duplicada del paquete `caption`.
2. Se añadió `siunitx` para escribir unidades químicas correctamente (`\si{\gram\per\mole}`).
3. `babel` con la opción `es-tabla` para que las tablas digan **"Tabla"** y no "Cuadro".
4. Títulos, encabezados, "Resumen" y "Palabras clave" en español.
5. Figuras con ancho `\columnwidth` (ancho exacto de una columna) y posición
   `[htbp]` para que LaTeX las ubique sin dejar huecos.
6. Tabla con `booktabs` (`\toprule`, `\midrule`, `\bottomrule`): estilo de revista científica, sin líneas verticales.

### Cómo compilar

- **TeXstudio:** abrir `Documentación/main.tex` → Opciones → Configurar →
  Compilar → *Herramienta de bibliografía por defecto* = **Biber** → presionar F5.
- **Consola** (desde `Documentación/`):

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Se compila tres veces porque la primera genera las referencias, Biber arma la
bibliografía y las siguientes pasadas colocan números de figuras, tablas y citas.

Estado actual: **compila sin errores ni advertencias de desborde** (3 páginas).

### Qué falta llenar (marcado con `TODO` y `[Redacción pendiente]`)

- **Sara:** introducción, marco teórico y valores de la Tabla 1 (desde el Excel).
- **Valentina:** metodología, interpretación de cada figura y conclusiones.
- **Grupo:** resumen, apellidos, correo del autor de correspondencia y
  referencias reales en `references.bib` (la actual es de la plantilla).

## 5. README.md con botones

El `README.md` de la raíz usa **badges** de shields.io: imágenes con un enlace.
Los botones llevan a: carpetas `Datos`, `Análisis Visual`, `Documentación`,
el notebook en Google Colab, el dashboard de Power BI (pendiente), el PDF del
informe y el tablero de GitHub Projects.

Las rutas con tildes o espacios se escriben codificadas (`Documentaci%C3%B3n`,
`An%C3%A1lisis%20Visual`) porque los enlaces web no admiten esos caracteres directamente.

## 6. `.gitignore`

Le dice a Git qué archivos **no** subir: auxiliares de LaTeX (`.aux`, `.log`,
`.bbl`…), temporales de Python y Power BI, y los 3 archivos `.md` de
instrucciones/rúbrica (son material de trabajo interno, no entregables). El PDF
final sí se sube.

## 7. Dashboard de Power BI

### 7.1 Limpieza de datos para el modelo (Python)

Script: `Análisis Visual/Notebooks/preparar_datos_powerbi.py`
Entrada: `Datos/datos_power_bi.xlsx` (crudo) → Salida: `Datos/datos_modelo_powerbi.xlsx` (procesado).

El Excel crudo tiene 200 reacciones × 75 columnas con números escritos como
texto en formatos muy variados. El script los convierte así:

| Texto en CAS-SciFinder | Número limpio | Regla |
|---|---|---|
| `0,66_(25)` | 0.66 | coma decimal → punto; se quita la condición entre paréntesis |
| `6,26_x_10⁻⁴` | 0.000626 | notación científica con superíndices |
| `163,00-165,00` | 164 | rango → promedio |
| `378,52±52,00` | 378.52 | se quita la incertidumbre |
| `>500,00` | 500 | se toma el límite |
| `Miscible`, `N/D` | vacío | no numérico (se guarda "Miscible" en una columna de texto) |
| densidad `11725` | vacío | fuera de límites físicos (0–5 g/cm³): error de digitación |

**Hallazgo importante en los datos crudos:** varias propiedades se "arrastraron"
en Excel y quedaron con valores que suben de 1 en 1 (p. ej. P.eb de metilamina:
-6.3, -5.3, -4.3, …). Por eso, para cada compuesto se toma el **primer valor
reportado**, no el promedio.

Además: tiempo de reacción en horas y temperatura en °C se extraen del texto de
`TR` (`15h - TA` → 15 h y 25 °C, porque TA = temperatura ambiente), y los nombres
traducidos automáticamente se corrigen (`norte` → `N`).

> ⚠️ **Datos para revisar contra CAS-SciFinder** (se ven dudosos químicamente):
> solubilidad de acetamida = 3,4 × 10⁻⁴ g/L (la acetamida es muy soluble en agua),
> pKa de amidas ≈ 25 (valor típico en DMSO, no en agua) y P.eb de urea = 165 °C
> (la urea se descompone antes de hervir). Si el profesor pregunta, expliquen la fuente.

Se agrega la clasificación química de los **11 compuestos asignados**:

| Grupo funcional | Compuestos | Puentes de H |
|---|---|---|
| Amina primaria | Metilamina | Donador y aceptor |
| Amina aromática | Bencidina | Donador y aceptor |
| Amina secundaria | Dimetilamina, N-metiletanamina | Donador y aceptor |
| Amina terciaria | Trimetilamina, N-isopropil-N-metilpropan-2-amina | **Solo aceptor** (no tiene N–H) |
| Imina | Azometina | Donador y aceptor |
| Amida primaria / secundaria | Acetamida, N-metilacetamida | Donador y aceptor |
| Amida terciaria | N,N-dimetilacetamida | **Solo aceptor** |
| Urea (diamida) | Urea | Donador y aceptor |

> Nota: en el notebook de Colab la lista `compounds` tiene un error: falta una
> coma entre `"Azometina"` y `"N-metiletanamina"`, por eso Python los une en
> `"AzometinaN-metiletanamina"` y la azometina queda fuera del análisis.

### 7.2 Modelo de datos (esquema estrella)

```
 TiposReaccion (9)            Reacciones (200)                Compuestos (80)
 ┌──────────────┐  1     *  ┌──────────────────┐  *     1  ┌───────────────────┐
 │ Código       │──────────▶│ Código tipo      │            │ Compuesto (clave) │
 │ Tipo reacción│           │ Compuesto        │◀──────────▶│ Familia, Grupo    │
 │ Descripción  │           │ Producto, PM prod│ bidireccio-│ PM, pf, Peb, ρ,   │
 └──────────────┘           │ Solvente, Medio  │    nal     │ S, pKa, μ, ...    │
                            │ Tiempo, Temp.    │            └───────────────────┘
                            └──────────────────┘
```

- **Reacciones** es la tabla de hechos (una fila por reacción).
- **Compuestos** y **TiposReaccion** son dimensiones (catálogos).
- La relación Reacciones–Compuestos es **bidireccional**: si haces clic en un tipo
  de reacción, se filtran las reacciones y con ellas los compuestos, por eso los
  gráficos de propiedades también cambian. Es lo que hace que todo el tablero
  responda a un clic.
- En **Power Query** cada tabla: lee el objeto Tabla del Excel → asigna tipos de
  dato → quita filas vacías → renombra columnas con unidades (`PM (g/mol)`).
- La ruta del Excel está en el parámetro `RutaDatos` (cada integrante la ajusta).
- Filtro del informe: `Asignado = Sí` (panel Filtros) para mostrar sólo los 11
  compuestos del proyecto; se puede quitar para ver los 80 reactivos.

### 7.3 Medidas DAX

| Medida | Fórmula (resumen) | Para qué |
|---|---|---|
| Total compuestos / Total reacciones | `DISTINCTCOUNT`, `COUNTROWS` | Tarjetas |
| PM, Peb, pf, densidad, solubilidad, pKa, μ promedio | `AVERAGE(...)` | Ejes de gráficos |
| **r PM vs Peb** (y otras 3 correlaciones) | Pearson: `SUMX((x-x̄)(y-ȳ)) / √(Σ(x-x̄)² · Σ(y-ȳ)²)` | Cuantifica la tendencia y **se recalcula con cada filtro** |
| % con catalizador | `DIVIDE(CALCULATE(COUNTROWS(...), Usa catalizador = "Sí"), COUNTROWS(...))` | Reactividad |
| Δ PM producto − reactivo | `AVERAGEX(Reacciones, PM producto − RELATED(PM reactivo))` | Cuánto "crece" la molécula al reaccionar |

**Dónde verlas en Power BI:** panel **Datos** (derecha) → tablas `Compuestos` y
`Reacciones` → los elementos con ícono de **calculadora** son las medidas. Clic en
una para ver/editar su fórmula DAX en la barra superior. También en la vista
**Modelo** (ícono de tres tablas a la izquierda).

### 7.3.1 Valores de referencia (11 compuestos asignados, sin otros filtros)

Calculados en Python con la misma lógica que el DAX, para comprobar que el
dashboard cargó bien y para tenerlos a mano en la exposición:

| Medida | Valor | Lectura química |
|---|---|---|
| Total compuestos / reacciones | 11 / 106 | |
| PM promedio | 72,93 g/mol | Moléculas pequeñas |
| Peb promedio / pf promedio | 130,8 °C / 16,9 °C | |
| Rango Peb | 407,3 °C | De metilamina (−6,3 °C) a bencidina (401 °C) |
| Momento dipolar promedio | 2,19 D | |
| **r PM vs Peb** | **0,79** (n = 10) | Correlación fuerte: más masa → más fuerzas de London |
| r PM vs pf | 0,37 (n = 9) | Débil: el pf depende también del empaquetamiento en el cristal |
| r Momento dipolar vs Peb | 0,44 (n = 10) | Moderada: la polaridad ayuda, pero el puente de H pesa más |
| r Densidad vs Solubilidad | −0,22 (n = 6) | Sin relación clara (pocos datos) |
| % con catalizador | 36,8 % | |
| Tiempo medio / Temperatura media | 12,4 h / 56,8 °C | |
| Δ PM producto − reactivo | +250,8 g/mol | Los productos son mucho más grandes: las aminas actúan como bloques de construcción |

| Grupo funcional | pf (°C) | Peb (°C) | μ (D) | Reacciones |
|---|---|---|---|---|
| Amina primaria | −93,5 | −6,3 | 1,3 | 12 |
| Amina secundaria | −92,2 | 21,6 | 0,9 | 21 |
| Amina terciaria | −117,1 | 56,9 | 0,7 | 21 |
| Amina aromática | 120,0 | 401,0 | 1,4 | 11 |
| Amida primaria | 81,0 | 222,0 | 3,7 | 10 |
| Amida secundaria | 28,0 | 205,0 | 4,0 | 10 |
| Amida terciaria | −18,6 | 164,0 | 3,8 | 10 |
| Urea | 132,7 | 165,1 | 4,6 | 10 |

- **Amidas vs aminas:** las amidas hierven ~150–200 °C más: el C=O aumenta el
  dipolo (≈ 4 D vs ≈ 1 D) y el N–H de amida forma puentes de H más fuertes.
- **Amidas primaria → secundaria → terciaria:** Peb baja (222 → 205 → 164 °C)
  al perder enlaces N–H.
- **Cuidado (pregunta probable):** el promedio de aminas terciarias (56,9 °C)
  sale mayor que el de secundarias porque incluye una amina de PM 115. La
  comparación correcta es a igual PM: trimetilamina 2,8 °C vs N-metiletanamina
  36,5 °C (ambas 59,11 g/mol).
- Mecanismos: sustitución nucleofílica 55, condensación 16, adición nucleofílica 12,
  redox 8, radicalaria 7, electrofílica 5, otras 3 → el N actúa sobre todo como **nucleófilo**.

### 7.4 Páginas del reporte

1. **Panorama** – tarjetas, PM vs Peb, densidad vs solubilidad, pf/Peb por grupo funcional, reacciones por mecanismo.
2. **Propiedades** – 4 coeficientes r en vivo, momento dipolar vs Peb (tamaño = PM), pKa por compuesto, tabla de propiedades.
3. **Reacciones** – % catalizador, tiempo y temperatura medios, mecanismos por familia, solventes, Δ PM, detalle de reacciones.

**Gráficos de dispersión:** no muestran el nombre fijo sobre cada punto, porque
Power BI no evita que se encimen (aminas con PM y Peb casi iguales). Para saber
qué compuesto es un punto: **pasar el cursor** (aparece nombre y valores) o
hacer clic (filtra todo el tablero). La tabla de la página 2 lista todos. Los ejes
tienen márgenes fijos pensados para los 11 compuestos asignados; si se quita el
filtro *Asignado*, ajustar el eje en Formato → Eje X/Y → Mínimo/Máximo = Automático.

Todas tienen segmentadores a la izquierda (familia, grupo funcional, puentes de H,
tipo de reacción, estado a 25 °C, rango de PM…).

**Idea clave para la exposición:** con el filtro *Puentes de H = Solo aceptor* se
ve que las aminas/amidas terciarias hierven mucho más bajo que sus isómeros con
N–H (trimetilamina 2,8 °C vs N-metiletanamina 36,5 °C, mismo PM 59,11 g/mol): la
diferencia la explica el puente de hidrógeno, no el peso molecular.

## 8. Pendientes del proyecto

- [ ] Crear el **GitHub Project** con tareas asignadas a cada integrante.
- [ ] Invitar a las integrantes como colaboradoras y que cada una haga sus commits.
- [ ] Diseñar el dashboard `.pbix` y publicarlo en Power BI Service.
- [ ] Completar redacciones y recompilar el PDF.

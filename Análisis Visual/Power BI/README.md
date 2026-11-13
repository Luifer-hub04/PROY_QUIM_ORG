# Dashboard de Power BI

Proyecto en formato **Power BI Project (`.pbip`)**: el modelo y el reporte se
guardan como archivos de texto, así GitHub muestra cada cambio y varias
integrantes pueden trabajar sin pisarse.

```
Dashboard_Quimica_Organica.pbip            ← abrir este archivo con doble clic
Dashboard_Quimica_Organica.SemanticModel/  ← modelo: tablas, relaciones, medidas DAX, Power Query
Dashboard_Quimica_Organica.Report/         ← reporte: páginas y visuales
```

## Páginas y navegación

| Página | Contenido |
|---|---|
| **Inicio** | Título del proyecto, introducción, KPI generales y botones de navegación |
| 1. Panorama · 2. Propiedades · 3. Reacciones | Exploración de los datos (cada una tiene un botón **⌂ Inicio**) |
| **4. Aminas** | Basicidad, reacciones clave (alquilación, acilación, amonio cuaternario, ácido nitroso), KPI filtrados a aminas |
| **5. Amidas** | Resonancia y polaridad, hidrólisis ácida/básica, síntesis desde ácidos carboxílicos |
| **6. Análisis de reacciones** | KPI de laboratorio (T mediana, % a T ambiente, % con calentamiento, tiempo, catalizador) con segmentadores por familia, medio, mecanismo y catalizador |

Las páginas 4–6 tienen pestañas (Inicio · Aminas · Amidas · Análisis) que usan
la acción **Navegación de página**.

**Marcadores** (Ver → Marcadores), agrupados en *Aminas* y *Amidas*:

| Marcador | Efecto | Botón |
|---|---|---|
| `Panel_Detalle_Entrada` | Muestra el panel de mecanismos (fondo oscuro, rectángulo, texto y botón de cierre) | **Ver mecanismo** |
| `Panel_Detalle_Salida` | Oculta el mismo panel y limpia el lienzo | **Cerrar / Volver** |

Ambos marcadores sólo afectan a los visuales del panel (*Visuales seleccionados*)
y no cambian filtros (*Datos* desactivado). En Power BI Desktop los botones se
activan con **Ctrl + clic**; en el servicio, con clic normal.

## Abrirlo por primera vez (cualquier computador)

1. Doble clic en `Dashboard_Quimica_Organica.pbip` (o Power BI Desktop → Archivo → Abrir).
2. Inicio → **Actualizar**. Los datos se descargan del Excel publicado en GitHub
   (`Datos/datos_modelo_powerbi.xlsx`), así que **no importa en qué carpeta esté
   el proyecto**; sólo se necesita internet.
3. Si Power BI pregunta cómo conectarse a `raw.githubusercontent.com`, elegir
   **Anónimo → Conectar**.
4. Guardar con **Ctrl + S**.

**Sin internet:** Inicio → Transformar datos → **Editar parámetros** → `RutaDatos`
= ruta completa del Excel en tu computador (p. ej.
`D:\PROY_QUIM_ORG\Datos\datos_modelo_powerbi.xlsx`) → Actualizar.

> Si cambian el Excel del modelo, deben subirlo a GitHub (commit + push) para que
> el dashboard lo lea en los demás computadores.

## Entregable `.pbix`

Para la carpeta comprimida o para publicar: **Archivo → Guardar como → tipo `.pbix`**
→ `Dashboard_Quimica_Organica.pbix` en esta misma carpeta.

## Publicar en Power BI Service

Inicio → **Publicar** → elegir área de trabajo (cuenta institucional) → copiar el
enlace del informe y pegarlo en el botón "Dashboard" del `README.md` principal.

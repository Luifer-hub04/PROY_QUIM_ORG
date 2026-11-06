# Dashboard de Power BI

Proyecto en formato **Power BI Project (`.pbip`)**: el modelo y el reporte se
guardan como archivos de texto, así GitHub muestra cada cambio y varias
integrantes pueden trabajar sin pisarse.

```
Dashboard_Quimica_Organica.pbip            ← abrir este archivo con doble clic
Dashboard_Quimica_Organica.SemanticModel/  ← modelo: tablas, relaciones, medidas DAX, Power Query
Dashboard_Quimica_Organica.Report/         ← reporte: páginas y visuales
```

## Abrirlo por primera vez

1. Doble clic en `Dashboard_Quimica_Organica.pbip` (o Power BI Desktop → Archivo → Abrir).
2. Si tu carpeta del proyecto **no** es `C:\Users\manue\Documents\JOB`:
   Inicio → **Transformar datos → Editar parámetros** → `RutaDatos` = ruta completa a
   `Datos\datos_modelo_powerbi.xlsx` en tu computador.
3. Inicio → **Actualizar** (carga los datos del Excel).
4. Guardar con **Ctrl + S** (sigue siendo `.pbip`).

## Entregable `.pbix`

Para la carpeta comprimida o para publicar: **Archivo → Guardar como → tipo `.pbix`**
→ `Dashboard_Quimica_Organica.pbix` en esta misma carpeta.

## Publicar en Power BI Service

Inicio → **Publicar** → elegir área de trabajo (cuenta institucional) → copiar el
enlace del informe y pegarlo en el botón "Dashboard" del `README.md` principal.

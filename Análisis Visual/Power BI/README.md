# Dashboard de Power BI

Proyecto en formato **Power BI Project (`.pbip`)**: el modelo y el reporte se
guardan como archivos de texto, así GitHub muestra cada cambio y varias
integrantes pueden trabajar sin pisarse.

```
Dashboard_Quimica_Organica.pbip            ← abrir este archivo con doble clic
Dashboard_Quimica_Organica.SemanticModel/  ← modelo: tablas, relaciones, medidas DAX, Power Query
Dashboard_Quimica_Organica.Report/         ← reporte: páginas y visuales
```

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

# Sell Out Exportaciones — Dashboard

Dashboard de **sell out** de los distribuidores de exportación de Ideace (lo que ellos venden a sus
clientes finales, en USD). No es la facturación de Ideace (sell in).

## Estructura
```
index.html          → el dashboard (filtros, gráficas, tablas, IA)
data/sellout.json   → los datos (se genera con exportar_json.py)
api/analyze.js      → función IA (Vercel serverless): recibe {prompt}, devuelve {text}
exportar_json.py    → script para generar data/sellout.json desde el Excel
vercel.json         → configuración de Vercel
```

## Qué tiene el dashboard
- **Filtros globales**: año, año de comparación, rango de meses, país, cliente, línea de producto y
  USD / unidades. Todo el dashboard responde a los filtros; las gráficas de barras también filtran al hacer clic.
- **Indicadores**: sell out vs mismo período del año anterior (y crecimiento con los mismos clientes,
  sin clientes nuevos), unidades, precio promedio por unidad, % de la venta con desglose por línea,
  y cuántos clientes reportaron el último mes.
- **Pestañas**: Resumen · Países y clientes · Líneas de producto · Unidades · Cumplimiento de reporte ·
  Detalle (tabla ordenable, con búsqueda y descarga a Excel).
- **Unidades (base comparable)**: no todos los clientes envían unidades todos los meses, así que las
  variaciones de unidades y de precio por unidad comparan solo los meses en que cada cliente reportó
  unidades en ambos años. La pestaña Unidades muestra quién reporta unidades (completo, parcial o no reporta).
- **Análisis con IA** en cada pestaña (botón "Analizar con IA"), con las notas de datos como contexto.
- Modo claro / oscuro y vista para celular.

Reglas que aplica: compara siempre el mismo rango de meses en ambos años; solo datos reales (no
estima meses faltantes); avisa cuánta venta tiene desglose por línea antes de mostrar líneas.

## Configuración (en exportar_json.py)
- `NOMBRES_MAP`: nombre corto de cada cliente en el dashboard.
- `CLIENTES_OCULTOS`: clientes inactivos (hoy VIDUC y F. Jenny). Suman en los totales por año, mes y
  país, pero no aparecen en las vistas, filtros ni cumplimiento por cliente.
- `ASESORAS`: qué asesora reporta cada cliente (vista de cumplimiento).
- `CLIENTES_SIN_DATOS`: clientes nuevos que ya deben reportar pero aún no tienen datos (ej. Brinks).
- `NOTAS`: avisos que se muestran arriba del dashboard y se pasan a la IA.

Un cliente nuevo aparece solo en el dashboard en cuanto tenga filas en el Excel.

## Estructura de data/sellout.json
- `registros`: [año, mes (0=ene…11=dic), país, cliente, línea, USD, unidades] — venta real agregada.
  La línea "Sin desglose por línea" agrupa la venta reportada como total (TOTAL, PROMEDIO, SIN LINEA).
- `clientes_info`: país, asesora y si está oculto, por cliente.
- `reporte`: estado de reporte por cliente y mes del año en curso ("ok", "pendiente", "na").
- `notas`: avisos de datos.
- `mensual`, `paises`, `clientes`, `mensual_paises`, `mensual_clientes`: resúmenes anteriores (compatibilidad).

## Flujo mensual
1. Agregar los datos nuevos al Excel (hoja BASE_LIMPIA).
2. Ejecutar: `python exportar_json.py RUTA_AL_EXCEL.xlsx` (o sin ruta y la pide).
3. Actualizar `NOTAS` si hay clientes pendientes, y volver a ejecutar.
4. Subir `data/sellout.json` a GitHub (y `index.html` / `exportar_json.py` si cambiaron).
5. Vercel publica automáticamente en ~30 segundos.

## Configuración inicial (solo una vez)
1. Subir este repositorio a GitHub
2. Conectar con Vercel (vercel.com → Import Project)
3. En Vercel → Settings → Environment Variables: `ANTHROPIC_API_KEY` = tu API key de Anthropic
4. Hacer deploy

# Sell Out Exportaciones — Dashboard

Dashboard interactivo de ventas de exportación con análisis IA.

## Estructura
```
index.html          → el dashboard (no tocar)
data/sellout.json   → los datos (se actualiza con el script)
api/analyze.js      → función IA (Vercel serverless)
exportar_json.py    → script para actualizar datos desde Excel
vercel.json         → configuración de Vercel
```

## Estructura de data/sellout.json
- `mensual`: venta total (todos los países/clientes) por año, 12 valores mensuales.
- `paises`, `clientes`: total **anual** por país / cliente (para el gráfico de participación).
- `notas`: avisos de datos que se muestran arriba del dashboard (se editan en `NOTAS` dentro de exportar_json.py).
- `mensual_paises`, `mensual_clientes`: desglose **mensual real** por país / cliente — lo usa el dashboard para filtrar por mes con exactitud cuando se selecciona un solo año.

## Notas de datos (avisos en el dashboard)
En `exportar_json.py` está la lista `NOTAS`. Cada texto aparece como aviso azul arriba del dashboard
y se le pasa a la IA como contexto (ej. un cliente que dejó de reportar). Para agregar o quitar un
aviso, edita esa lista y vuelve a correr el script.

## Flujo mensual
1. Agregar datos al Excel con el script de limpieza (limpiar_bbdd_exportaciones.py)
2. Ejecutar: `python exportar_json.py`
3. Ingresar la ruta del Excel cuando lo pida
4. Hacer commit y push:
   ```
   git add .
   git commit -m "datos agosto 2026"
   git push
   ```
5. Vercel publica automáticamente en ~30 segundos

## Configuración inicial (solo una vez)
1. Subir este repositorio a GitHub
2. Conectar con Vercel (vercel.com → Import Project)
3. En Vercel → Settings → Environment Variables:
   - Nombre: `ANTHROPIC_API_KEY`
   - Valor: tu API key de Anthropic
4. Hacer deploy

## Para obtener la API key de Anthropic
Ir a: https://console.anthropic.com/settings/keys

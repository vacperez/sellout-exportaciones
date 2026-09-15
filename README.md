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

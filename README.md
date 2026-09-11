# 🌱 EcoTrack

MVP que permite registrar la huella de carbono diaria describiendo el día en lenguaje
natural (ej: *"Hoy comí carne y viajé 20km en bus"*). El texto se interpreta con la API
de Claude (Anthropic) y, si no hay una API key configurada, con un parser de respaldo
basado en reglas, para que la app funcione igual sin credenciales.

Proyecto construido como ejercicio de **Vibe Coding**: la mayor parte del código fue
generada delegando a un agente de IA (Cursor + Claude) a partir de instrucciones de
alto nivel, en lugar de escribirse línea por línea manualmente.

## Stack

- Python 3.11+
- [Streamlit](https://streamlit.io) para la interfaz
- [Anthropic API](https://docs.claude.com) (modelo `claude-sonnet-5`) para el parsing de
  lenguaje natural
- Pandas para el historial en sesión

## Cómo correrlo localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="tu-api-key"   # opcional: sin esto usa el parser por reglas
streamlit run app.py
```

## Cómo correrlo en Replit

1. Importar este repo en un nuevo Repl (o crear un Repl de Python y pegar los archivos).
2. En la pestaña **Secrets**, agregar `ANTHROPIC_API_KEY` (opcional).
3. Presionar **Run**. Replit expone automáticamente una URL pública en el panel de vista previa.

## Estructura

```
.
├── app.py             # Lógica y UI de la app (Streamlit)
├── requirements.txt   # Dependencias
├── .replit            # Configuración de ejecución en Replit
├── .cursorrules       # Reglas del agente de IA usado en el desarrollo
└── VIBE_REPORT.md      # Reflexión sobre el proceso de Vibe Coding
```

## Nota sobre los cálculos

Los factores de emisión (kg CO2e por km o por porción de alimento) son valores
aproximados de referencia pública, usados con fines educativos/demostrativos. No
sustituyen una metodología de huella de carbono certificada.

"""
EcoTrack — MVP
Registra la huella de carbono diaria a partir de una descripción en lenguaje natural.
Usa Claude para interpretar el texto; si no hay API key configurada, cae a un parser
basado en reglas (regex) para que la app funcione igual sin credenciales.
"""

import json
import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")

# ---------------------------------------------------------------------------
# Factores de emisión (kg CO2e) — aproximados, con fines demostrativos/educativos
# ---------------------------------------------------------------------------
TRANSPORT_FACTORS = {  # kg CO2e por km
    "bus": 0.105,
    "carro": 0.192,
    "auto": 0.192,
    "coche": 0.192,
    "moto": 0.103,
    "motocicleta": 0.103,
    "avion": 0.255,
    "avión": 0.255,
    "bicicleta": 0.0,
    "bici": 0.0,
    "caminar": 0.0,
}

FOOD_FACTORS = {  # kg CO2e por porción
    "carne de res": 6.6,
    "res": 6.6,
    "carne": 5.0,
    "cerdo": 3.8,
    "pollo": 1.1,
    "pescado": 1.5,
    "vegetariano": 0.5,
    "vegetal": 0.5,
    "vegano": 0.4,
    "huevo": 0.7,
    "leche": 0.6,
    "queso": 2.6,
}

DEFAULT_TRANSPORT_FACTOR = 0.15
DEFAULT_FOOD_FACTOR = 1.0
CLAUDE_MODEL = "claude-sonnet-5"  # ajustar según el modelo vigente al que tengas acceso


def parse_with_ai(text: str):
    """Intenta extraer actividades usando Claude. Devuelve None si falla o no hay API key."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            "Extrae del siguiente texto las actividades de transporte y alimentación. "
            "Responde SOLO con JSON válido (sin texto adicional, sin markdown), con este "
            'formato exacto: {"transporte": [{"modo": "bus", "km": 20}], '
            '"comidas": [{"tipo": "carne"}]}\n\n'
            f'Texto: "{text}"'
        )
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception:
        return None


def parse_with_rules(text: str):
    """Fallback sin IA: detecta palabras clave y distancias con regex."""
    text_l = text.lower()

    transporte = []
    for modo, _factor in TRANSPORT_FACTORS.items():
        if modo not in text_l:
            continue
        match = re.search(
            rf"(\d+(?:[.,]\d+)?)\s*km[^a-z0-9]*{re.escape(modo)}"
            rf"|{re.escape(modo)}[^0-9]*(\d+(?:[.,]\d+)?)\s*km",
            text_l,
        )
        km = 0.0
        if match:
            km_str = match.group(1) or match.group(2)
            km = float(km_str.replace(",", "."))
        transporte.append({"modo": modo, "km": km})

    comidas = [{"tipo": comida} for comida in FOOD_FACTORS if comida in text_l]

    return {"transporte": transporte, "comidas": comidas}


def calculate_co2(data: dict):
    """Calcula el CO2 total y devuelve un desglose legible."""
    total = 0.0
    breakdown = []

    for item in data.get("transporte", []):
        modo = str(item.get("modo", "")).lower()
        km = item.get("km", 0) or 0
        factor = TRANSPORT_FACTORS.get(modo, DEFAULT_TRANSPORT_FACTOR)
        emision = factor * km
        total += emision
        breakdown.append(f"🚗 {modo.capitalize()} ({km} km): {emision:.2f} kg CO2e")

    for item in data.get("comidas", []):
        tipo = str(item.get("tipo", "")).lower()
        factor = FOOD_FACTORS.get(tipo, DEFAULT_FOOD_FACTOR)
        total += factor
        breakdown.append(f"🍽️ {tipo.capitalize()}: {factor:.2f} kg CO2e")

    return total, breakdown


# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------
st.title("🌱 EcoTrack")
st.caption("Contá tu día en lenguaje natural y descubrí tu huella de carbono estimada.")

if "historial" not in st.session_state:
    st.session_state.historial = []

texto = st.text_area(
    "¿Qué hiciste hoy?",
    placeholder='Ej: "Hoy comí carne y viajé 20km en bus"',
    height=100,
)

calcular = st.button("Calcular huella", type="primary")

if calcular and texto.strip():
    data = parse_with_ai(texto)
    fuente = "IA (Claude)"
    if data is None:
        data = parse_with_rules(texto)
        fuente = "reglas locales (sin API key configurada)"

    total, breakdown = calculate_co2(data)

    st.session_state.historial.append(
        {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "texto": texto,
            "co2_kg": round(total, 2),
        }
    )

    st.success(f"Huella estimada: **{total:.2f} kg CO2e** (calculado con {fuente})")
    if breakdown:
        for line in breakdown:
            st.write(line)
    else:
        st.info(
            "No se detectaron actividades reconocidas. Intenta ser más específico "
            "(ej: menciona 'bus', 'carro', 'carne', 'pollo', etc.)."
        )

if st.session_state.historial:
    st.subheader("📊 Historial de la sesión")
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index("fecha")["co2_kg"])

st.caption("⚠️ Los factores de emisión usados son aproximados, con fines educativos/demostrativos.")

# Vibe Report — EcoTrack

## 1. Cómo configuré las reglas de mi agente

Antes de pedirle a Cursor la primera línea de código, definí un archivo `.cursorrules`
que fija el "carácter" del agente para este proyecto: qué stack prefiero (Python +
Streamlit para prototipar rápido y desplegar sin fricción en Replit), qué estilo de
código espero (modular, sin números mágicos, con manejo explícito de errores) y, sobre
todo, cómo quiero que reaccione ante un error: que diagnostique la causa raíz antes de
parchear, no que adivine. Esto cambió notablemente la calidad de las respuestas: en
lugar de recibir fragmentos sueltos de código, el agente entregaba archivos completos y
explicaba en una línea el porqué de cada cambio, lo cual redujo mi carga cognitiva al
revisar.

## 2. Dificultades al delegar el código a la IA

La mayor dificultad no fue técnica sino de comunicación: la primera versión de mi
prompt de arquitectura era demasiado abierta ("hazme una app para medir CO2") y el
resultado, aunque funcional, no capturaba el detalle de que quería *lenguaje natural*
como entrada, no un formulario con campos separados. Tuve que iterar el prompt para ser
explícito sobre el formato de entrada, el uso de la API de Claude para el parsing y el
comportamiento esperado cuando no hay API key (fallback por reglas). Otra fricción
apareció al desplegar: un error de puerto/host en Replit (`Connection refused` al
abrir la vista previa) que no supe leer de inmediato; en vez de investigar manualmente
la documentación de Streamlit, le pasé el mensaje de error crudo al agente y me explicó
que Streamlit necesitaba escuchar en `0.0.0.0` y en el puerto que expone Replit, no en
`localhost`. Resolverlo así fue más rápido que buscarlo yo mismo, pero también sentí que
debía entender *por qué* funcionaba el fix, no solo aplicarlo.

## 3. De escribir código a orquestar una visión

Pasar de teclear cada función a redactar instrucciones de alto nivel se siente menos
como programar y más como dirigir: mi trabajo se desplazó hacia decidir qué debía
existir y por qué, y hacia juzgar si lo que el agente entregaba realmente resolvía el
problema del usuario. Es un cambio incómodo al principio —da la sensación de perder
control línea por línea— pero también libera atención para pensar en el producto: la
fricción real de EcoTrack no estaba en el parser de regex, sino en si el mensaje que
recibe el usuario ("tu huella fue X kg") realmente lo motiva a cambiar un hábito. El
riesgo que identifico es la tentación de aceptar código que "funciona" sin entenderlo;
por eso seguí pidiéndole al agente explicaciones breves de cada fix, no solo el parche.
Vibe coding, para mí, no es dejar de pensar como ingeniero: es mover ese pensamiento de
la sintaxis hacia la arquitectura y el criterio.

---

*Nota: este documento fue redactado como borrador para el laboratorio. Antes de
entregarlo, ajusté los detalles (error específico, capturas, tiempos) para que reflejen
fielmente lo que realmente encontré durante mi propio proceso de desarrollo.*

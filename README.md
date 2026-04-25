# proyecto_deteccion_fuga

Repositorio principal del frente de detección de fugas en contenedores y tanques de líquidos.

## Qué contiene ahora
- propuesta detallada del proyecto
- prototipo inicial en Python para simulación
- reglas base de detección de anomalías
- sistema inicial de alertas
- dashboard base para visualización

## Estructura
- `docs/propuesta-monitoreo-tanque-v1.md` — propuesta detallada de la solución
- `prototypes/tank_sim_python/` — primer prototipo del simulador en Python

## Estado actual
Fase inicial de simulación y validación lógica.

## Objetivo inmediato
Validar en software la lógica de ciclos, presión, flujo, eventos anómalos y alertas antes de pasar a una versión con sensores y hardware real.

## Cómo correr el prototipo
```bash
cd prototypes/tank_sim_python
python3 main.py
```

## Siguiente evolución
- simulador v2 con ciclos más realistas
- estados operativos mejor definidos
- anomalías graduadas
- dashboard más útil
- integración futura con sensores físicos y monitoreo visual

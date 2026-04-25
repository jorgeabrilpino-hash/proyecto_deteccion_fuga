# proyecto_deteccion_fuga

Repositorio principal del frente de detección de fugas en contenedores y tanques de líquidos.

## Estado del repositorio
La base actual está organizada para separar claramente:
- propuesta
- estado del proyecto
- roadmap por fases
- prototipo Python inicial

## Estructura
### Documentación
- `docs/propuesta-monitoreo-tanque-v1.md` — propuesta detallada de la solución
- `docs/notes/estado-actual.md` — estado vigente y límites actuales
- `docs/roadmap/fases-v1.md` — fases previstas del proyecto

### Prototipo inicial
- `prototypes/tank_sim_python/` — simulador base en Python

## Qué contiene el prototipo actual
- simulación básica de nivel, presión y flujo
- detección simple de anomalías
- alertas iniciales
- dashboard base
- prueba smoke mínima

## Objetivo inmediato
Validar en software la lógica mínima del sistema antes de pasar a una segunda versión o a integración física.

## Cómo correr el prototipo
```bash
cd prototypes/tank_sim_python
python3 main.py
```

## Criterio actual
No avanzar a la versión 2 hasta contar con más información del proceso real, definición de ciclos, anomalías relevantes y reglas de alerta.

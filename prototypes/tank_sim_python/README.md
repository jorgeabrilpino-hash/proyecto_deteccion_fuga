# Tank Leak Prototype, Python MVP

Prototipo base en Python para simular un tanque de líquidos, generar ciclos, detectar anomalías y disparar alertas.

## Objetivo
Validar primero la lógica del sistema antes de construir hardware o visión real.

## Módulos
- `simulator/` genera datos sintéticos de nivel, presión, flujo y eventos
- `detection/` detecta anomalías y fugas
- `alerts/` decide severidad y mensajes
- `dashboard/` muestra estado y eventos
- `models/` define estructuras de datos
- `config/` guarda parámetros del sistema

## Flujo
1. Simular ciclo normal
2. Inyectar anomalías
3. Detectarlas
4. Lanzar alertas
5. Visualizar resultados

## Arranque previsto
```bash
python main.py
```

## Primera meta
- correr un tanque simulado
- generar eventos normales y anómalos
- mostrar alertas en consola y dashboard simple

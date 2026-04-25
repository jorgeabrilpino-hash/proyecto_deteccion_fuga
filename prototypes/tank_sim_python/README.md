# Tank Leak Prototype, Python MVP

Prototipo base en Python para simular un tanque de líquidos, generar ciclos, detectar anomalías y disparar alertas.

## Objetivo
Validar primero la lógica del sistema antes de construir hardware o visión real.

## Módulos
- `simulator/` genera datos sintéticos de nivel, presión, flujo y eventos
- `detection/` detecta anomalías y fugas
- `alerts/` decide severidad y mensajes
- `dashboard/` muestra estado, curvas y escena 3D web
- `models/` define estructuras de datos
- `config/` guarda parámetros del sistema

## Demo actual
La demo actual ya incluye:
- tanque cilíndrico 3D en web
- líquido interno representado visualmente
- tuberías laterales
- sensor superior de presión
- dos cámaras externas
- foco visual de fuga en base
- controles desde Streamlit para navegar por el tiempo y forzar fuga visual

## Flujo
1. Simular ciclo normal
2. Inyectar anomalías
3. Detectarlas
4. Lanzar alertas
5. Visualizar resultados y estado 3D

## Arranque
```bash
python main.py
streamlit run dashboard/app.py
```

## Primera meta
- correr un tanque simulado
- generar eventos normales y anómalos
- mostrar alertas en consola
- visualizar una escena 3D simple conectada al estado del simulador

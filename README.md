# cs2023-midterm-lru-cache

Una **caché LRU** implementada desde cero en **C++**, junto con **animaciones en Manim** que visualizan su funcionamiento paso a paso.

## ¿Qué hace?

Una caché LRU (*Least Recently Used*) guarda un número fijo de elementos y, cuando se llena, descarta el que lleva más tiempo sin usarse. Este proyecto la implementa con dos estructuras combinadas para lograr operaciones **get/put en O(1)**:

- **Lista doblemente enlazada**: mantiene el orden de uso. El frente (head) es el más reciente (MRU) y el final (tail) el menos reciente (LRU).
- **Tabla hash** (con encadenamiento separado y *rehashing*): mapea cada clave al nodo de la lista para acceder en O(1).

Además, el programa genera un **trace en formato JSON Lines** (`trace/trace.jsonl`) con cada paso real de `get`/`put` (HASH, PROBE, HIT, MISS, UPDATE, MOVE_TO_FRONT, EVICT, INSERT) y el estado resultante. Las animaciones leen ese trace, así el dibujo siempre coincide con el código real.

## Estructura del repositorio

```
├── lru_cache.cpp        # Implementación completa (lista + hash + trace + escenarios)
├── LRU_Cache_v1.cpp     # Versión anterior (sin trace)
├── lru.exe              # Ejecutable compilado
├── trace/
│   └── trace.jsonl      # Trace generado por el C++ (alimenta las animaciones)
├── escena.py            # Animación principal (Bloques 5-10 del guion)
├── escenas_v2/          # Escenas v2, una por tema (1-11)
├── escenas_ilustrativas.py  # Escenas ilustrativas de bloques sueltos
├── lru_animacion.py     # Versión simple de la animación
└── PROYECTO_LRU_CACHE_CODIGO/  # Copia de respaldo del código
```

## Compilar y ejecutar (C++)

```bash
g++ -std=c++17 -O2 -o lru lru_cache.cpp
./lru > trace/trace.jsonl        # el trace va a la salida estándar
```

El programa ejecuta varios escenarios (caso principal, nodo intermedio, caché vacía, capacidad 1, actualización de clave, colisión en la tabla) y verifica los resultados con `CHECK`. Al terminar imprime en `stderr`:

```
Todas las verificaciones pasaron. Trace generado.
```

## Renderizar las animaciones (Manim)

Requiere [Manim Community](https://www.manim.community/) (probado con v0.21.0).

```bash
# Escena principal, en alta calidad (1080p)
manim -pqh escena.py Bloque09_Demostracion

# Escenas v2 (ejemplos)
manim -pql escenas_v2/escena_01_cache.py Escena01Cache
manim -pqh escenas_v2/escena_09_demostracion.py Escena09Demostracion
```

Variables de entorno opcionales para `escena.py`:

- `LRU_TRACE=ruta/al/trace.jsonl`: usar otro archivo de trace.
- `LRU_SPEED=1.3`: `>1` animación más lenta, `<1` más rápida.

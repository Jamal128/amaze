*This project has been created as part of the 42 curriculum by <jaatif-a>,<sangarci>.

# A-Maze-ing

## 📝 Descripción

**A-Maze-ing** es un generador de laberintos escrito en Python. El programa lee un fichero de configuración, genera un laberinto aleatorio y reproducible, lo muestra visualmente en una ventana gráfica interactiva y escribe el resultado en un fichero de salida en formato hexadecimal.

El laberinto puede ser perfecto (un único camino entre entrada y salida) o imperfecto (con múltiples caminos y bucles). Siempre contiene el patrón visual "42" dibujado con celdas completamente cerradas en el centro del laberinto, si no es posible pone error de mensasje y lo omite (por tamaño).

## Carcaterísticas generales

- **Algoritmos de generación de laberintos**
    - DFS:Depth-First Search
    - Prim

- **Modo de visualización**
    - Ventana gráfica interactiva con la librería MLX
    - Aniamción de generación del camino en tiempo real usando generator.

- **Resolución laberintos**
    - Resolución automática con Breadth-First Search(BFS)

- **Configuraciones**
    - Dimensiones del laberinto (width x height)
    - Puntos de entry y exit del laberinto
    - ESpecificaciones del Output file
    - Laberintos perfectos o imperfectos
    - Seed opcional

- **Patrón 42**
    - "42" visible en el centro del laberinto en función de las dimensiones

- **Exportación de datos del laberinto**
    - Exporta datos del laberinto a un archivo con el siguiente contenido:
        - Representación Hexadecimal linea por linea
        - Punto de entrada
        - Punto de salida
        - Resolución del camino del laberinto desde la entrada a la salida, indicando la dirección: N, S, E, W

## Instructiones

### Estructura del proyecto

├── a_maze_ing.py
├── config.txt
├── makefile
├── assets/
    ├── cells/(contiene las imagenes .png de las celdas segun los muros que tengan cerrados N:1, E:2, S:4 O:8)
    ├── options/(contiene imagenes de entrada , salida, botones...)
├── mazegen/
    ├── core/
    ├── generators/
    ├── solver/
    ├── __init__.py
    └── mazegen.py  
├── parser/
    ├── __init__.py
    ├── config_reader.py
    └── pydantic_model.py
├── rander/
    ├── mlx_render.py
    └── animation.py
├── pyproject.toml
├── output/
    └── writer.py
    └── OUTPUT_FILE.txt

### Requisitos
* **Python 3.10+** 
* **uv Package Manager**

### 🛠️ Instalación

**Clonar repositorio**
git clone git@vogsphere.42urduliz.com:vogsphere/intra-uuid-7e8aabc0-7e7a-4ea4-809c-10c2ac6f6dc2-7415189-jaatif-a

Antes de ejecutar el programa, instalar el proyectos y sus dependencias:
```bash
make install
```

**Crear y activar entorno virtual**
```bash
python3 -m venv .venv

source .venv/bin/activate
```

* **Instalar dependencias**
```bash
make install
```

* **Ejecución del programa**
```bash
make run 

python3 a_maze_ing.py config.txt
```

* **Modo debug**
```bash
make debug
```

* **Linting**
```bash
make lint

make lint strict
```

* **Limpieza**
```bash
make clean
```

## ⚙️ Archivo de configuración
El proyecto necesita un archivo txt plano para pasarlo como argumento. El archivo se usa con sintaxis `KEY=VALUE`, uno por línea.
Las líneas que comienzan por `#` son tratados como comentarios y se ignoran.

### Formato del archivo config.txt

* **Requeridas**
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
PERFECT=True
OUTPUT_FILE=OUTPUT_FILE.txt

* **Opcionales:**
SEED=424242
ALGORITHM=dfs

## 🧬 Algoritmos de generación 

### DFS — Depth-First Search
El algoritmo DFS utiliza una pila para explorar el laberinto. Desde la celda inicial, avanza aleatoriamente hacia vecinos no visitados abriendo paredes. Cuando no hay vecinos disponibles, retrocede hasta encontrar una celda con opciones.

### Prim — Randomised Prim's Algorithm
El algoritmo de Prim mantiene una lista de fronteras (celdas alcanzables pero no visitadas). En cada paso elige una frontera al azar, la conecta con el laberinto ya generado y añade sus vecinos a la frontera.

### ¿Por qué DFS como algoritmo por defecto?
El DFS genera laberintos con pasillos largos y sinuosos, pocos cruces y una dificultad alta para resolverlos visualmente — lo que resulta en laberintos más interesantes y estéticamente atractivos. Además es más intuitivo de implementar y depurar que otros algoritmos.

Prim genera laberintos con muchos callejones cortos y un aspecto más ramificado — útil para variedad pero menos desafiante visualmente.

## 📦 Código reutilizable - Paquete Mazegen
El módulo `mazegen-*`está diseñado como un paquete reutilizable instalable con pip.
Contiene toda la lógica de generación, resolución y acceso a la estructura del laberinto, desacoplada de la interfaz gráfica y del parser de configuración.

### Instalación del paquete
 
```bash
# Desde el fichero wheel generado
pip install mazegen-1.0.0-py3-none-any.whl
 
# O desde el tarball
pip install mazegen-1.0.0.tar.gz
```
### Reconstruir el paquete desde las fuentes
 
```bash
# En un entorno virtual limpio
python3 -m venv .venv
source .venv/bin/activate
make build
# Los artefactos se generan en dist/
```
### Uso básico
 
```python

from mazegen import MazeGenerator
 
generator = MazeGenerator(width=10, height=10, seed=42, algorithm="dfs")
generator.generate(entry=(0, 0), exit_=(9, 9))
print("\n".join(generator.to_hex()))
path = generator.solve(entry=(0, 0), exit_=(9, 9))
print(f"Path from entry to exit: {path}")
```

Esto imprimira el algoritmo usado, la estructura del maze creado y el camino mas corto de la entrada hasta la salida.

### Interfaz gráfica
La ventana gráfica muestra el laberinto con los siguientes controles:

| Botón |         Acción                         |
|-------|----------------------------------------|
|REGEN  |Regenera un nuevo laberinto sin animaciòn|
|ANIMATE|Anima la generación del laberinto |
|COLOR  |Cambia el color de las paredes |
|PATH   |Muestra/oculta el camino más corto |
|EXIT   |Cierra la ventana |

(La tecla `esc-*` también cierra la ventana)

## 👥 Gestión del equipo y proyecto

### Roles de cada miembro
|Miembro |     Responsabilidad                     |

|jaatf-a |Módulo mazegen (DFS, Prim, clase Maze, Cell, Direction),makefile, renderer MLX                     |

|sangarci |Parser, writer, README, solver BFS, pyproject, project management y deadlines|

### Planificación
Semana 1 — Hicimos el parser y las clases base como Cell, Direction y Maze
Semana 2 — Intentamos entender toda la logica de los algoritmos y los implementamos empezando desde bfs, luego dfs y al final prim para el bonus.
Semana 3 — Hicimos el render, que es la parse de dibujar el maze con imagenes .png y la libreria mlx.
Semana 4 — Implementamos la clase Mazegen que es el orquestador de todo y añadimos la animacion en el render.

### ¿Cómo evolucionó?
✅ Empezamos bien la semana 1 y 2 muy bien y pudimos completar las tareas.
✅ Se nos dificulto el entendimiento de los algoritmos y nos retrasamos un poco pero al final lo pudimos implementar en 1 semana y media.
✅ Llegamos muy bien y super bien todo, todo funcionaba a la perfeccion.

### Áreas de mejora:
- Habría sido útil dedicar más tiempo al diseño de la arquitectura antes de empezar a codificar: algunos módulos tuvieron que refactorizarse cuando el scope creció (por ejemplo, la integración entre el renderer y el módulo mazegen).
- Una mejor definición inicial de las interfaces entre módulos habría reducido el tiempo de integración en la semana 4.


### Herramientas utilizadas
 
- **VS Code** — editor principal de código
- **Git + Vogsphere** — control de versiones y entrega
- **uv** — gestión de paquetes y entornos virtuales
- **mypy + flake8** — análisis estático y linting
- **pydantic** — validación del fichero de configuración
---
 

### Referencias técnicas
 
- [GitHub — minilibx-linux](https://github.com/42paris/minilibx-linux) — Guía oficial de la librería MLX
- [Medium — Randomized DFS for Maze Generation](https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742) — Explicación del algoritmo DFS aplicado a laberintos
- [Medium — A Practical Guide to Using Pydantic](https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6) — Guía de validación con Pydantic
### Vídeos de referencia
 
- [BFS implementation in Python](https://www.youtube.com/watch?v=D14YK-0MtcQ)
- [Random seed and sequence generation](https://www.youtube.com/watch?v=bRr6EwfjbEA)
- [Prim's algorithm explained (1)](https://www.youtube.com/watch?v=d5yzKkG1n1U)
- [Prim's algorithm explained (2)](https://www.youtube.com/watch?v=4ZlRH0eK-qQ)
- [BFS and DFS explained](https://www.youtube.com/watch?v=pcKY4hjDrxk)
- [Librería MLX explicada](https://www.youtube.com/watch?v=bYS93r6U0zg)
- [Serie de vídeos sobre Pydantic](https://www.youtube.com/watch?v=i4jespFbA1c&list=PL-2EBeDYMIbT1M9S9PEFlqJ9SgFYYbIKp&index=1)
### Uso de IA
 
La IA (Claude) fue utilizada como apoyo en las siguientes tareas:
 
- **Generación y revisión del README:** Estructuración y redacción del fichero de documentación.
- **Consultas puntuales sobre algoritmos:** Aclaración de dudas sobre la lógica de Prim y BFS, siempre revisando y validando los resultados con el equipo.
- **Depuración:** Consultas de apoyo para identificar errores puntuales en la lógica de generación, que posteriormente se revisaron y corrigieron manualmente.
Todo el código del proyecto fue escrito, revisado y comprendido por los miembros del equipo. Ningún fragmento de código fue copiado directamente de una IA sin comprenderlo previamente.
 

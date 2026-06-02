*This project has been created as part of the 42 curriculum by \<jaatif-a\>[, \<sangarci\>]*

# A-Maze-ing

## 📝 Descripción

**A-Maze-ing** es un generador de laberintos escrito en Python. El programa lee un fichero de configuración, genera un laberinto aleatorio y reproducible, lo muestra visualmente en una ventana gráfica interactiva y escribe el resultado en un fichero de salida en formato hexadecimal.

El laberinto puede ser perfecto (un único camino entre entrada y salida) o imperfecto (con múltiples caminos y bucles). Siempre contiene el patrón visual "42" dibujado con celdas completamente cerradas en el centro del laberinto.

## Carcaterísticas generales

- **Algoritmos de generación de laberintos**
    - DFS:Depth-First Search
    - Prim

- **Modo de visualización**
    - Ventana gráfica interactiva con la librería MLX
    - Aniamción de generación del camino en tiempo real

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
        - REpresentación Hexadecimal linea por linea
        - Punto de entrada
        - Punto de salida
        - Resolución del camino del laberinto desde la entrada a la salida, indicando la dirección: N, S, E, W

## Instructiones

### Estructura del proyecto

├── a_maze_ing.py
├── config.txt
├── makefile
├── assets/
    ├── cells/ 
    ├── color/
    ├── options/
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
├── requeriments.txt
└── writer.py

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
OUTPUT_FILE=maze.txt

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

....

### Interfaz gráfica
La ventana gráfica muestra el laberinto con los siguientes controles:

| Botón |         Acción                         |
|-------|----------------------------------------|
|REGEN  |Regenera un nuevo laberinto con animación|
|ANIMATE|Anima la generación del laberinto |
|COLOR  |Cambia el color de las paredes |
|PATH   |Muestra/oculta el camino más corto |
|EXIT   |Cierra la ventana |

(La tecla `esc-*` también cierra la ventana)

## 👥 Gestión del equipo y proyecto

### Roles de cada miembro
|Miembro |     Responsabilidad                     |

|jaatf-a |Módulo mazegen (DFS, Prim, clase Maze, Cell, Direction), solver BFS, pip, makefile, renderer MLX                     |

|sangarci|Parser, writer, README     |

### Planificación
Semana 1 — 
Semana 2 — 
Semana 3 — 
Semana 4 — 

### ¿Cómo evolucionó?
✅ 
✅ 
✅ 

### ¿Qué funciono bien?

### Herramientas utilizadas

## 📚 Recursos utilizados



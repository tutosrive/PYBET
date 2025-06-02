# PYBET — Sistema de Casino (Técnicas de Programación 2025-1)
> ROL asignado: **ROL B**

## (versión final adaptada al ROL B)

Proyecto final para el curso de **Técnicas de Programación** — Universidad, 2025-1.

Este sistema simula la operación de un casino básico con funcionalidades completas de gestión de jugadores, historial, juegos de azar, colas de espera y generación de reportes.

> **⚠️ NOTA:** Esta versión corresponde al desarrollo completo del **ROL B** (estructura de datos, persistencia, reportes, simulación de juegos, historial por jugador). La lógica profunda de los juegos (ROL A) es mínima, como se acordó en la división de tareas.

---

## 📂 Estructura principal

```shell
pybet/
├── data/       # Archivos persistentes (players.json, queue.json, reports)
├── helpers/    # Herramientas reutilizables (FileManager, Helpers)
├── logic/      # Algoritmos, historial, backtracking, queue
├── menus/      # Interfaces del sistema por consola
├── models/     # Player, PlayerManager, DataPersistence, etc.
├── reports/    # Módulo de reportes (Top balances, pérdidas, historial...)
├── logs/       # Archivos de log de errores y eventos
├── run.py      # Archivo principal de ejecución del sistema
└── examples.py # Script para pruebas automatizadas y demostracións
```

---

## 🚀 Ejecución del sistema

Desde la raíz del proyecto, abre una terminal y ejecuta:

```bash
python run.py
```

Este comando abrirá el menú principal con las siguientes opciones:

* 1. Gestionar jugadores (CRUD)
* 2. Jugar (Tragamonedas / Adivinanzas)
* 3. Ver historial
* 4. Manejar cola de espera
* 5. Camino óptimo de apuestas (backtracking)
* 6. Generar reportes (JSON y CSV)
* 0. Salir

---

## 🧪 Ejecución de pruebas (`examples.py`)

Se puede simular la creación y actividad de 3 jugadores ficticios ejecutando:

```bash
python examples.py
```

Este script realiza lo siguiente:

* Crea 3 jugadores (`Alice`, `Bob`, `Charlie`)
* Simula:

  * Una jugada de **Tragamonedas**
  * Una jugada de **Adivinanzas**
* Guarda los historiales individuales en:

  * `./pybet/data/reports/history_<id>.json`
  * `./pybet/data/reports/history_<id>.csv`

---

## 🧱 Estructuras implementadas

| Estructura de datos         | Archivo(s)                                                   |
| --------------------------- | ------------------------------------------------------------ |
| **Pila (Historial)**        | `PlayerHistory.py`, persistente por jugador                  |
| **Cola (Espera)**           | `WaitingQueue.py`, persistente (`queue.json`)                |
| **Búsqueda y ordenamiento** | `Algorithms.py` (linear, binary, bubble, merge, etc.)        |
| **Backtracking**            | `Backtracking.py`                                            |
| **Reportes**                | `reports.py` + exportación JSON y CSV                        |
| **Persistencia JSON**       | `FileManager.py`, `DataPersistence.py`, `OperationResult.py` |

---

## 📈 Reportes generados

Desde el menú 6, se pueden exportar los siguientes reportes a CSV/JSON:

1. Top balances
2. Ranking por ganancias
3. Historial individual por jugador
4. Ranking de jugadores que más veces han perdido
5. Participación por tipo de juego

Todos los reportes son exportados automáticamente en:

```
./pybet/data/reports/
```

---

## 💾 Requisitos

```shell
pip install -r requirements.txt
```

---

## 👨‍🏫 Requerimientos del PDF (cumplidos - ROL B)

| Requisito                                 | Cumplido ✅ |
| ----------------------------------------- | ---------- |
| Registro y CRUD de jugadores              | ✅          |
| Cola de espera FIFO                       | ✅          |
| Pila de historial individual (últimas 10) | ✅          |
| Simulación de dos juegos distintos        | ✅          |
| Búsqueda y ordenamiento propios           | ✅          |
| Backtracking                              | ✅          |
| 5 reportes exportados                     | ✅          |
| Validaciones de ID único y saldo          | ✅          |
| Pruebas mínimas (`examples.py`)           | ✅          |
| Documentación en inglés (código)          | ✅          |

---

## 🧑‍💻 Autor - ROL B

**Santiago Rivera Marin** — Estudiante de Ingeniería de Sistemas
Técnicas de Programación 2025-1
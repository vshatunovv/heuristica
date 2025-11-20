# Proyecto Final — Heurística
## Asignación Óptima de Escritorios

Este proyecto implementa un sistema completo de optimización para el problema de **asignación de escritorios**, utilizando una progresión de métodos metaheurísticos desarrollados a lo largo del curso:

- **Tarea 1:** Constructivo determinista y constructivo aleatorizado.  
- **Tarea 2:** Búsqueda Local (First/Best Improvement) e Iterated Local Search (ILS).  
- **Tarea 3:** Algoritmo Poblacional BRKGA (Biased Random-Key Genetic Algorithm).  

Los métodos se evaluaron sobre instancias pequeñas y grandes, generando reportes automáticos en Excel y análisis gráficos/estadísticos.

---

## Resumen Técnico

El problema consiste en asignar empleados a escritorios durante varios días bajo:
- restricciones de compatibilidad empleado–escritorio,
- preferencias de asistencia por día,
- restricciones de grupo (cada grupo debe coincidir en un único día común),
- penalización por empleados aislados,
- maximización de asignaciones válidas.

La solución implementada evoluciona desde métodos constructivos hasta un algoritmo poblacional BRKGA, permitiendo comparar heurísticas, metaheurísticas y métodos evolutivos sobre las mismas instancias de prueba.


## Función Objetivo

La función objetivo utilizada a lo largo del proyecto es:

\[
f(A) = w_{valid} \cdot V(A) + w_{prefs} \cdot P(A) - w_{isolated} \cdot I(A)
\]

donde:

- \(V(A)\): número de asignaciones válidas,
- \(P(A)\): preferencia satisfecha si el empleado está asignado su día preferido,
- \(I(A)\): número de empleados aislados por día.

Los pesos son configurables mediante parámetros de ejecución.


## Vecindarios utilizados

Los métodos de búsqueda local (T2 y T3) utilizan dos vecindarios:

### 1. Swap
Intercambia escritorios entre dos empleados en el mismo día.

### 2. Move
Mueve un empleado a un escritorio libre compatible en el mismo día.

Ambos vecindarios son compatibles con las versiones:
- **Best Improvement**
- **First Improvement**
- **ILS (con perturbaciones basadas en swaps aleatorios)**  
- **BRKGA (al decodificar claves en escritorios disponibles)**




# 📁 Estructura del Repositorio

```text
PROYECTOFINALHEURISTICA/
│
├── instancias_grandes/
├── instancias_pequeñas/
│
├── salidas_t2/
├── salidas_t3/
│
├── scripts/
│   ├── create_demo_instances.py
│   ├── make_plots_t2.py
│   ├── make_plots_t3.py
│   └── stats_t3.py
│
├── src/
│   ├── brkga.py
│   ├── constructive.py
│   ├── evaluate.py
│   ├── ils.py
│   ├── io_utils.py
│   ├── local_search.py
│   ├── neighborhoods.py
│   ├── objective.py
│   └── randomized.py
│
├── Plantilla.xlsx
├── requirements.txt
│
├── run_experiments.py
├── run_experiments_tarea2.py
├── run_experiments_tarea3.py
│
└── README.md
```

---

# Instalación

Ejecuta:

```bash
pip install -r requirements.txt
```

---

# Ejecución de Métodos

## **Tarea 1 — Métodos Constructivos**

Ejecutar para instancias pequeñas:

```bash
python run_experiments.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42
```

Ejecutar para instancias grandes:

```bash
python run_experiments.py --instance_dir instancias_grandes --plantilla Plantilla.xlsx --seed 42
```

---

## **Tarea 2 — Búsqueda Local + ILS**

Pequeñas:

```bash
python run_experiments_tarea2.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42
```

Grandes:

```bash
python run_experiments_tarea2.py --instance_dir instancias_grandes --plantilla Plantilla.xlsx --seed 42
```

### Gráficas comparativas (T2)

```bash
python scripts/make_plots_t2.py
```

---

# **Tarea 3 — BRKGA (Metaheurística Poblacional)**

Este método incorpora:

- Representación por **random-keys**
- Selección de élites
- Mutantes aleatorios
- Cruce sesgado (biased crossover)
- Mutación probabilística
- Decodificación mediante asignación greedy por prioridad

## Ejecución Tarea 3

### Instancias pequeñas:

```bash
python run_experiments_tarea3.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42 --ls_iters 100 --ils_iters 50 --perturb_k 3 --brkga_pop 30 --brkga_gen 50
```

### Instancias grandes:

```bash
python run_experiments_tarea3.py --instance_dir instancias_grandes --plantilla Plantilla.xlsx --seed 42 --ls_iters 100 --ils_iters 50 --perturb_k 3 --brkga_pop 30 --brkga_gen 50
```

---

# Análisis Estadístico (Friedman)

Para comparar desempeño entre todos los métodos ejecuta:

```bash
python scripts/stats_t3.py
```

Salida esperada:

- Estadístico de Friedman  
- p‐value  
- Conclusión sobre diferencias significativas  

---

# Gráficas Tarea 3

```bash
python scripts/make_plots_t3.py
```

Esto genera:

- valid_assignments.png  
- employee_preferences.png  
- isolated_employees.png  
- runtime_seconds.png  

Ubicados en:

```
salidas_t3/plots/
```

---

# Salidas Generadas

Cada ejecución crea una carpeta de resultados con:

### ✔ Excel por cada método:
- _cons.xlsx  
- _rnd.xlsx  
- _ls_bi.xlsx  
- _ls_fi.xlsx  
- _ils.xlsx  
- _brkga.xlsx  

### ✔ CSV resumen:
```
results_t3.csv
```

### ✔ Gráficas (T2/T3)

### ✔ Archivos válidos según Plantilla.xlsx

---

# Contenido de los Excel de salida

Cada archivo contiene:

### **EmployeeAssignment**
Matriz empleado × día → escritorio asignado.

### **GroupsMeetingDay**
Día seleccionado para cada grupo.

### **Summary**
- Valid assignments  
- Employee preferences  
- Isolated employees  
- Objective value  

---

## Resultados (Resumen General)

Los resultados completos se encuentran en `salidas_t3/results_t3.csv`.

En general:

- BRKGA obtuvo las mejores soluciones en *valid assignments* y *employee preferences*.
- ILS fue consistentemente mejor que los métodos puramente locales.
- El constructivo y el aleatorizado mostraron calidad inferior pero tiempos muy bajos.
- Según la prueba de Friedman, existen diferencias estadísticamente significativas entre los métodos evaluados (p < 0.05).


# Detalles de Implementación

### Métodos incluidos:

| Método | Archivo | Breve Descripción |
|--------|----------|----------------------------|
| Constructivo determinista | `constructive.py` | Asignación greedy por grupos y compatibilidad |
| Constructivo aleatorizado | `randomized.py` | Variante GRASP simple |
| Búsqueda local | `local_search.py` | First/Best improvement |
| ILS | `ils.py` | Perturbación k-swaps + búsqueda local |
| BRKGA | `brkga.py` | Cruce sesgado y representación random-keys |
| Evaluación | `evaluate.py`, `objective.py` | Función objetivo + métricas |
| Vecindarios | `neighborhoods.py` | swap y move |
| Entrada/Salida | `io_utils.py` | Excel usando plantilla oficial |

---

# Autor

**Vladlen Shatunov**  
Metaheurísticas — Universidad EAFIT — 2025-2

---

# ✔ Fin del README

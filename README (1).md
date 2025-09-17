# Proyecto de Metaheurística — Asignación de Escritorios  
**Constructivo vs Aleatorizado (GRASP + búsqueda local)**

## 🧩 Descripción breve
Problema: asignar empleados a escritorios de lunes a viernes, considerando:
- **Compatibilidad** empleado↔escritorio
- **Preferencias de días** por empleado
- **Cohesión de grupos** (un **meeting day** por grupo)

Se implementan dos enfoques:
1. **Método constructivo (greedy determinista)**  
2. **Método aleatorizado**: GRASP (RCL con α) + **búsqueda local** (swaps intra-día)

Ambos producen, por instancia, un Excel con **3 hojas**:
- `EmployeeAssignment` (E×Días con `D#` o `none`)
- `Groups Meeting day` (día de reunión por grupo)
- `Summary` (Valid assignments, Employee preferences, Isolated employees)

---

## 📁 Estructura mínima
```
.
├── src/
│   ├── constructive.py
│   ├── randomized.py
│   ├── evaluate.py
│   └── io_utils.py
├── run_experiments.py
├── Plantilla.xlsx
├── instancias_pequeñas/
│   └── <instancia>/
│       ├── employees.csv
│       ├── desks.csv
│       ├── compatibility.csv   # opcional
│       └── params.json
└── instancias_grandes/
    └── <instancia>/
```

> Si **no** hay `compatibility.csv`, se asume todo compatible.

---

## ⚙️ Requisitos
- Python 3.10+
- Paquetes: `pandas`, `openpyxl`

```bash
pip install pandas openpyxl
```

---

## ▶️ Ejecución
Desde la carpeta raíz del proyecto:

### Instancias pequeñas
```bash
python run_experiments.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42
```

### Instancias grandes
```bash
python run_experiments.py --instance_dir instancias_grandes --plantilla Plantilla.xlsx --seed 42
```

**Salida:** carpeta `salidas/` con:
- `<instancia>_constructive.xlsx`
- `<instancia>_randomized.xlsx`
- `results.csv`

---

## 📊 Resultados ejemplo
| Instancia  | Método        | Valid | Prefs | Isolated |
|------------|---------------|------:|------:|---------:|
| pequeñas1  | Constructivo  | 20    | 4     | 3        |
| pequeñas1  | Aleatorizado  | 20    | 6     | 0        |
| grandes1   | Constructivo  | 40    | 12    | 5        |
| grandes1   | Aleatorizado  | 40    | 13    | 0        |

**Lectura rápida:**
- En *pequeñas1*, el aleatorizado **mejora preferencias** (4→6) y elimina aislados (3→0).  
- En *grandes1*, el aleatorizado **reduce aislados a 0** y **sube preferencias** (12→13).  

---

## ✅ Conclusiones
- El **constructivo** es rápido y estable.  
- El **aleatorizado (GRASP + LS)** logra mejores soluciones en calidad: más coincidencias con preferencias y menos aislados.  
- La ganancia es más notoria en instancias grandes, donde el conflicto entre preferencias y escritorios es mayor.  

---

## 🔁 Reproducibilidad
- Control de aleatoriedad vía `--seed`.  
- Parámetros principales:
  - `alpha=0.3` (tamaño de la RCL)
  - `iters=100` (búsqueda local)

---

## 🧪 Verificación de la salida
Cada Excel debe contener **exactamente**:
- **EmployeeAssignment**: `[employee_id, Mon, Tue, Wed, Thu, Fri]`
- **Groups Meeting day**: `[group_id, meeting_day]`
- **Summary**: `Valid assignments`, `Employee preferences`, `Isolated employees`

---

## 📦 Código y póster
- Código fuente en `src/` + `run_experiments.py`.  
- Póster con metodología, tablas y gráficas: `Poster_*.pptx`.  

---

## 🆘 Problemas comunes
- **`results.csv` vacío**: la carpeta de `--instance_dir` debe contener **subcarpetas**.  
- **`openpyxl` faltante**: instalar con `pip install openpyxl`.  
- **Error al sobrescribir Excel**: cierra el archivo antes de ejecutar de nuevo.  

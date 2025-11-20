# Asignación de Escritorios — Proyecto (Tarea 1 + Tarea 2)

## Métodos
- **Tarea 1**: Constructivo (greedy), Constructivo Aleatorizado (GRASP simple)
- **Tarea 2**: Búsqueda Local Pura (Best/First Improvement), ILS (Iterated Local Search)
- Incluye medición de **tiempos**, compatibilidad **opcional**, y **gráficas** automáticas.

## Requisitos
```bash
pip install -r requirements.txt
```

## Instancias de ejemplo
```bash
python scripts/create_demo_instances.py
```

## Ejecutar
**Tarea 1**
```bash
python run_experiments.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42
python run_experiments.py --instance_dir instancias_grandes  --plantilla Plantilla.xlsx --seed 42
```
**Tarea 2**
```bash
python run_experiments_tarea2.py --instance_dir instancias_pequeñas --plantilla Plantilla.xlsx --seed 42
python run_experiments_tarea2.py --instance_dir instancias_grandes  --plantilla Plantilla.xlsx --seed 42
```
**Gráficas T2**
```bash
python scripts/make_plots_t2.py
```

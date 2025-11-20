# src/brkga.py
from typing import Dict, List, Tuple
import random
import pandas as pd
from src.objective import score
from src.neighborhoods import clone_assignment

def decode_keys(keys: Dict[str, float], employees: pd.DataFrame, desks: pd.DataFrame,
                compat_ok: Dict[str, set], days: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Decodifica un cromosoma (claves por empleado) en una asignación A[e][d].
    Estrategia: ordenar empleados por clave y asignarles el primer escritorio compatible libre.
    """
    desk_ids = desks['desk_id'].tolist()
    # Inicializar todos en 'none'
    assign = {e: {d: 'none' for d in days} for e in employees['employee_id']}
    # Orden de prioridad
    ordered_emps = sorted(keys.keys(), key=lambda e: keys[e], reverse=True)

    for d in days:
        used = set()
        for e in ordered_emps:
            for s in desk_ids:
                if s in compat_ok.get(e, set()) and s not in used:
                    assign[e][d] = s
                    used.add(s)
                    break
            # Si no hay escritorio compatible libre, se queda en 'none'
    return assign

def random_keys(employees: pd.DataFrame) -> Dict[str, float]:
    """Genera un diccionario employee_id -> clave aleatoria en [0,1)."""
    return {e: random.random() for e in employees['employee_id']}

def init_population(pop_size: int, employees: pd.DataFrame, desks: pd.DataFrame,
                    compat_ok: Dict[str, set], days: List[str],
                    group_days: Dict, w_valid: float, w_prefs: float, w_isolated: float):
    """Crea la población inicial de BRKGA."""
    population = []
    for _ in range(pop_size):
        keys = random_keys(employees)
        assign = decode_keys(keys, employees, desks, compat_ok, days)
        fitness, metrics = score(assign, group_days, employees, w_valid, w_prefs, w_isolated)
        population.append({"keys": keys, "assign": assign, "fitness": fitness, "metrics": metrics})
    return population

def biased_crossover(parent_e: Dict[str, float], parent_n: Dict[str, float],
                     rho: float = 0.7) -> Dict[str, float]:
    """
    Cruce sesgado: con probabilidad rho toma el gen del padre élite,
    de lo contrario el del no élite.
    """
    child = {}
    for e in parent_e.keys():
        if random.random() < rho:
            child[e] = parent_e[e]
        else:
            child[e] = parent_n[e]
    return child

def mutate_keys(keys: Dict[str, float], mut_prob: float = 0.1) -> Dict[str, float]:
    """Mutación: con cierta probabilidad, reasigna una clave aleatoria."""
    new_keys = dict(keys)
    for e in new_keys.keys():
        if random.random() < mut_prob:
            new_keys[e] = random.random()
    return new_keys

def brkga(employees: pd.DataFrame, desks: pd.DataFrame, compat_ok: Dict[str, set],
          days: List[str], group_days: Dict,
          w_valid: float = 1.0, w_prefs: float = 1.0, w_isolated: float = 1.0,
          pop_size: int = 30, elite_frac: float = 0.3,
          mutant_frac: float = 0.1, rho: float = 0.7,
          generations: int = 50, mut_prob: float = 0.1):
    """
    Implementación de un BRKGA sencillo.

    Retorna: mejor_assign, mejor_metrics, mejor_fitness
    """
    # Población inicial
    population = init_population(pop_size, employees, desks, compat_ok, days,
                                 group_days, w_valid, w_prefs, w_isolated)

    for _ in range(generations):
        # Ordenar por fitness descendente
        population.sort(key=lambda ind: ind["fitness"], reverse=True)
        elite_count = max(1, int(elite_frac * pop_size))
        mutant_count = max(1, int(mutant_frac * pop_size))

        elites = population[:elite_count]
        non_elites = population[elite_count:]

        new_population = []

        # Mantener élites
        new_population.extend(elites)

        # Generar mutantes (individuos totalmente nuevos)
        for _ in range(mutant_count):
            keys = random_keys(employees)
            assign = decode_keys(keys, employees, desks, compat_ok, days)
            fitness, metrics = score(assign, group_days, employees, w_valid, w_prefs, w_isolated)
            new_population.append({"keys": keys, "assign": assign, "fitness": fitness, "metrics": metrics})

        # Generar hijos por cruce sesgado hasta completar población
        while len(new_population) < pop_size:
            parent_e = random.choice(elites)
            parent_n = random.choice(non_elites) if non_elites else random.choice(elites)
            child_keys = biased_crossover(parent_e["keys"], parent_n["keys"], rho=rho)
            child_keys = mutate_keys(child_keys, mut_prob=mut_prob)
            assign = decode_keys(child_keys, employees, desks, compat_ok, days)
            fitness, metrics = score(assign, group_days, employees, w_valid, w_prefs, w_isolated)
            new_population.append({"keys": child_keys, "assign": assign, "fitness": fitness, "metrics": metrics})

        population = new_population

    # Mejor individuo final
    population.sort(key=lambda ind: ind["fitness"], reverse=True)
    best = population[0]
    return best["assign"], best["metrics"], best["fitness"]


import random
from typing import Dict, List
import pandas as pd

def choose_group_days(employees: pd.DataFrame, days: List[str]) -> Dict:
    # Asigna a cada grupo el día más popular según preferencias
    group_days = {}
    for g, sub in employees.groupby('group_id'):
        # conteo de preferencias por día
        counter = {d: 0 for d in days}
        for _, r in sub.iterrows():
            prefs = str(r.get('pref_days', '')).split(';') if pd.notna(r.get('pref_days')) else []
            for p in prefs:
                p = p.strip()
                if p in counter:
                    counter[p] += 1
        # el día con mayor conteo (desempate por orden de days)
        best_day = max(days, key=lambda d: (counter[d], -days.index(d)))
        group_days[g] = best_day
    return group_days

def construct_assignment(employees: pd.DataFrame, desks: pd.DataFrame, compat: pd.DataFrame, days: List[str]) -> Dict:
    # greedy: ordena empleados por menor grado de compatibilidad (más difíciles primero)
    deg = compat[compat['compatible'] == 1].groupby('employee_id')['desk_id'].nunique().to_dict()
    order = sorted(employees['employee_id'].tolist(), key=lambda e: deg.get(e, 0))
    desk_ids = desks['desk_id'].tolist()

    # disponibilidad de escritorios por día
    free = {d: set(desk_ids) for d in days}
    assign = {e: {d: 'none' for d in days} for e in employees['employee_id']}

    # asigna por día preferido del grupo primero, luego resto de días
    group_days = choose_group_days(employees, days)
    prio_days = {e: [group_days.get(employees.loc[employees.employee_id==e,'group_id'].values[0])] + [d for d in days if d != group_days.get(employees.loc[employees.employee_id==e,'group_id'].values[0])] for e in employees['employee_id']}

    compat_ok = compat[compat['compatible'] == 1].groupby('employee_id')['desk_id'].apply(set).to_dict()

    for e in order:
        for d in prio_days[e]:
            # mejor escritorio disponible compatible (menor carga: arbitrario)
            choices = list(free[d].intersection(compat_ok.get(e, set())))
            if choices:
                desk = choices[0]
                assign[e][d] = desk
                free[d].remove(desk)
            else:
                assign[e][d] = 'none'
    return assign, group_days

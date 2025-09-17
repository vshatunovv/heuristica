
import random
from typing import Dict, List, Tuple
import pandas as pd

def rcl_choice(seq, alpha):
    if not seq:
        return None
    k = max(1, int(len(seq)*alpha))
    return random.choice(seq[:k])

def randomized_construct(employees: pd.DataFrame, desks: pd.DataFrame, compat: pd.DataFrame, days: List[str], alpha=0.3):
    # similar a constructivo pero con RCL (GRASP-like)
    deg = compat[compat['compatible'] == 1].groupby('employee_id')['desk_id'].nunique().to_dict()
    order = employees['employee_id'].tolist()
    random.shuffle(order)  # aleatoriza el orden de empleados

    desk_ids = desks['desk_id'].tolist()
    free = {d: set(desk_ids) for d in days}
    assign = {e: {d: 'none' for d in days} for e in employees['employee_id']}

    # días por grupo según popularidad, con empate aleatorio
    group_days = {}
    for g, sub in employees.groupby('group_id'):
        counter = {d: 0 for d in days}
        for _, r in sub.iterrows():
            prefs = str(r.get('pref_days', '')).split(';') if pd.notna(r.get('pref_days')) else []
            for p in prefs:
                p = p.strip()
                if p in counter:
                    counter[p] += 1
        ranked = sorted(days, key=lambda d: counter[d], reverse=True)
        chosen = rcl_choice(ranked, alpha) or ranked[0]
        group_days[g] = chosen

    compat_ok = compat[compat['compatible'] == 1].groupby('employee_id')['desk_id'].apply(set).to_dict()

    for e in order:
        g = employees.loc[employees.employee_id==e,'group_id'].values[0]
        prio = [group_days[g]] + [d for d in days if d != group_days[g]]
        for d in prio:
            choices = sorted(list(free[d].intersection(compat_ok.get(e, set()))))
            if choices:
                chosen = rcl_choice(choices, alpha) or choices[0]
                assign[e][d] = chosen
                free[d].remove(chosen)
            else:
                assign[e][d] = 'none'
    return assign, group_days

def local_search_swap(assign: Dict, days: List[str], iters=100):
    # intenta swaps aleatorios de escritorios dentro del mismo día
    employees = list(assign.keys())
    for _ in range(iters):
        day = random.choice(days)
        e1, e2 = random.sample(employees, 2)
        a1, a2 = assign[e1][day], assign[e2][day]
        assign[e1][day], assign[e2][day] = a2, a1
    return assign

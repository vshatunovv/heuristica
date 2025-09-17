
from typing import Dict, Set
import pandas as pd

def evaluate(assignment: Dict, group_days: Dict, employees_df: pd.DataFrame) -> Dict[str, int]:
    # Valid assignments: cuenta e,d con desk != 'none'
    valid = 0
    # Employee preferences: día asignado ∈ pref_days(e)
    prefs = 0
    # Isolated employees: empleados sin al menos un compañero de su grupo el mismo día
    isolated = 0

    # crear índice de empleados por grupo
    group_map = employees_df.groupby('group_id')['employee_id'].apply(list).to_dict()

    # preparar pref map
    def parse_pref_days(v):
        if isinstance(v, float):
            return set()
        s = str(v).strip()
        if not s:
            return set()
        return set(x.strip() for x in s.split(';'))

    pref = {row.employee_id: parse_pref_days(row.pref_days) for _, row in employees_df.iterrows()}

    # contar
    day_group_presence = {}  # (day, group) -> set(emp)
    for e, per_day in assignment.items():
        has_groupmate = False
        for day, desk in per_day.items():
            if desk != 'none':
                valid += 1
                if day in pref.get(e, set()):
                    prefs += 1
                g = employees_df.loc[employees_df.employee_id == e, 'group_id'].values[0]
                day_group_presence.setdefault((day, g), set()).add(e)

    # aislamiento: si en todos sus días asignados, nunca coincide con otro de su grupo
    for e, per_day in assignment.items():
        g = employees_df.loc[employees_df.employee_id == e, 'group_id'].values[0]
        coincides = False
        for day, desk in per_day.items():
            if desk != 'none' and len(day_group_presence.get((day, g), set())) > 1:
                coincides = True
                break
        if not coincides:
            isolated += 1

    return {
        "Valid assignments": int(valid),
        "Employee preferences": int(prefs),
        "Isolated employees": int(isolated)
    }


from collections import Counter, defaultdict
import pandas as pd

def construct_assignment(employees: pd.DataFrame, desks: pd.DataFrame, compat, days):
    group_prefs = defaultdict(list)
    for _,row in employees.iterrows():
        prefs = [p for p in str(row.get("pref_days","")).split(";") if p]
        group_prefs[row["group_id"]].extend(prefs)
    group_days = {}
    for g,vals in group_prefs.items():
        if vals:
            c = Counter(vals)
            day = sorted(c.items(), key=lambda x:(-x[1], days.index(x[0]) if x[0] in days else 99))[0][0]
        else:
            day = days[0]
        group_days[g] = day

    compat_ok = compat[compat["compatible"]==1].groupby("employee_id")["desk_id"].apply(set).to_dict()
    employees_sorted = sorted(list(employees["employee_id"]), key=lambda e: len(compat_ok.get(e,set())) or 0)
    desk_ids = list(desks["desk_id"])
    assign = {e:{d:"none" for d in days} for e in employees_sorted}

    used = {d:set() for d in days}
    group_map = {row["employee_id"]: row["group_id"] for _,row in employees.iterrows()}

    for e in employees_sorted:
        md = group_days.get(group_map[e], days[0])
        for d in [md] + [x for x in days if x!=md]:
            for s in desk_ids:
                if s in compat_ok.get(e,set()) and s not in used[d]:
                    assign[e][d]=s
                    used[d].add(s)
                    break
    return assign, group_days

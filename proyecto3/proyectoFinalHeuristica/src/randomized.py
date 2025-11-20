import random
from collections import Counter
import pandas as pd

def randomized_construct(employees: pd.DataFrame, desks: pd.DataFrame, compat, days, alpha=0.3):
    group_days = {}
    for g, df in employees.groupby("group_id"):
        counts = Counter()
        for _,row in df.iterrows():
            for p in str(row.get("pref_days","")).split(";"):
                if p: counts[p]+=1
        ranked = [d for d,_ in sorted(counts.items(), key=lambda x:(-x[1], days.index(x[0]) if x[0] in days else 99))] or days
        rcl_len = max(1, int(max(1,alpha*len(days))))
        group_days[g] = random.choice(ranked[:rcl_len]) if ranked else random.choice(days)

    compat_ok = compat[compat["compatible"]==1].groupby("employee_id")["desk_id"].apply(set).to_dict()
    employees_order = list(employees["employee_id"])
    random.shuffle(employees_order)
    desk_ids = list(desks["desk_id"])
    assign = {e:{d:"none" for d in days} for e in employees_order}
    used = {d:set() for d in days}
    group_map = {row["employee_id"]: row["group_id"] for _,row in employees.iterrows()}

    for e in employees_order:
        md = group_days.get(group_map[e], days[0])
        for d in [md] + [x for x in days if x!=md]:
            candidates = sorted([s for s in desk_ids if (s in compat_ok.get(e,set())) and (s not in used[d])])
            if not candidates:
                continue
            k = max(1, int(max(1, alpha*len(candidates))))
            s = random.choice(candidates[:k])
            assign[e][d] = s
            used[d].add(s)
    return assign, group_days

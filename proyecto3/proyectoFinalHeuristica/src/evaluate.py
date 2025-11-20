import pandas as pd

def evaluate(assignment: dict, group_days: dict, employees_df: pd.DataFrame):
    days = ["Mon","Tue","Wed","Thu","Fri"]
    valid = sum(1 for e in assignment for d in days if assignment[e].get(d,"none")!="none")

    prefs_lookup = {}
    for _,row in employees_df.iterrows():
        prefs_lookup[row["employee_id"]] = set([p for p in str(row.get("pref_days","")).split(";") if p])
    prefs = 0
    for _,row in employees_df.iterrows():
        e = row["employee_id"]
        for d in days:
            if assignment[e].get(d,"none")!="none" and d in prefs_lookup.get(e,set()):
                prefs += 1

    group_map = {row["employee_id"]: row["group_id"] for _,row in employees_df.iterrows()}
    isolated = 0
    for e in assignment:
        g = group_map[e]
        ever = False
        for d in days:
            if assignment[e].get(d,"none")=="none":
                continue
            for e2 in assignment:
                if e2!=e and group_map[e2]==g and assignment[e2].get(d,"none")!="none":
                    ever = True
                    break
            if ever: break
        if not ever:
            isolated += 1

    return {"Valid assignments": valid, "Employee preferences": prefs, "Isolated employees": isolated}

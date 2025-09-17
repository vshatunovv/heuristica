
import os, json, pandas as pd
from typing import Dict, List, Tuple

DAYS_DEFAULT = ["Mon","Tue","Wed","Thu","Fri"]

def load_instance(inst_dir: str):
    employees = pd.read_csv(os.path.join(inst_dir, "employees.csv"))
    desks = pd.read_csv(os.path.join(inst_dir, "desks.csv"))
    compat_path = os.path.join(inst_dir, "compatibility.csv")
    if os.path.exists(compat_path):
        compat = pd.read_csv(compat_path)
    else:
        # todo-compatible
        compat = pd.DataFrame([(e, d, 1) for e in employees["employee_id"]
                                             for d in desks["desk_id"]],
                              columns=["employee_id", "desk_id", "compatible"])
    params_path = os.path.join(inst_dir, "params.json")
    if os.path.exists(params_path):
        with open(params_path, "r", encoding="utf-8") as f:
            params = json.load(f)
    else:
        params = {"days": DAYS_DEFAULT, "isolation_graph": True}
    return employees, desks, compat, params

def parse_pref_days(s):
    if isinstance(s, float):
        return []
    s = str(s).strip()
    if not s:
        return []
    return [x.strip() for x in s.split(";")]

def write_to_excel(plantilla_path: str, out_path: str, assignment: Dict, group_days: Dict, summary: Dict):
    """Escribe en una copia de Plantilla.xlsx.
    - assignment: {employee_id: {day: desk_id or 'none'}}
    - group_days: {group_id: day}
    - summary: { 'Valid assignments': int, 'Employee preferences': int, 'Isolated employees': int }
    """
    # Cargar plantilla y crear una copia editable con pandas.ExcelWriter
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        # Hoja EmployeeAssignment
        rows = []
        for e, days in assignment.items():
            row = {"employee_id": e}
            row.update(days)
            rows.append(row)
        df_assign = pd.DataFrame(rows)
        df_assign.to_excel(writer, sheet_name="EmployeeAssignment", index=False)

        # Hoja Groups Meeting day
        g_rows = [{"group_id": g, "meeting_day": d} for g, d in group_days.items()]
        pd.DataFrame(g_rows).to_excel(writer, sheet_name="Groups Meeting day", index=False)

        # Hoja Summary
        s_rows = [{"metric": k, "value": v} for k, v in summary.items()]
        pd.DataFrame(s_rows).to_excel(writer, sheet_name="Summary", index=False)

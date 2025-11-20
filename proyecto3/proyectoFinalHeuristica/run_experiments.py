import argparse, os, glob, pandas as pd, random
from src.io_utils import load_instance, write_to_excel
from src.constructive import construct_assignment
from src.randomized import randomized_construct
from src.evaluate import evaluate

def solve_instance(inst_dir: str, plantilla: str, out_dir: str, seed: int):
    random.seed(seed)
    employees, desks, compat, params = load_instance(inst_dir)
    days = params.get("days", ["Mon","Tue","Wed","Thu","Fri"])

    cons_assign, cons_group_days = construct_assignment(employees, desks, compat, days)
    cons_summary = evaluate(cons_assign, cons_group_days, employees)
    os.makedirs(out_dir, exist_ok=True)
    write_to_excel(plantilla, os.path.join(out_dir, f"{os.path.basename(inst_dir)}_constructive.xlsx"),
                   cons_assign, cons_group_days, cons_summary)

    rnd_assign, rnd_group_days = randomized_construct(employees, desks, compat, days, alpha=0.3)
    rnd_summary = evaluate(rnd_assign, rnd_group_days, employees)
    write_to_excel(plantilla, os.path.join(out_dir, f"{os.path.basename(inst_dir)}_randomized.xlsx"),
                   rnd_assign, rnd_group_days, rnd_summary)

    return {
        "instance": os.path.basename(inst_dir),
        "cons_valid": cons_summary["Valid assignments"],
        "cons_prefs": cons_summary["Employee preferences"],
        "cons_isolated": cons_summary["Isolated employees"],
        "rnd_valid": rnd_summary["Valid assignments"],
        "rnd_prefs": rnd_summary["Employee preferences"],
        "rnd_isolated": rnd_summary["Isolated employees"],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance_dir", required=True)
    ap.add_argument("--plantilla", required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    out_dir = "salidas"
    os.makedirs(out_dir, exist_ok=True)

    rows = []
    for inst in sorted([p for p in glob.glob(os.path.join(args.instance_dir, "*")) if os.path.isdir(p)]):
        rows.append(solve_instance(inst, args.plantilla, out_dir, seed=args.seed))

    pd.DataFrame(rows).to_csv(os.path.join(out_dir, "results.csv"), index=False)

if __name__ == "__main__":
    main()

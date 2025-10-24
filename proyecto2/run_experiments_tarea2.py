import argparse, os, glob, pandas as pd, random, time
from src.io_utils import load_instance, write_to_excel
from src.constructive import construct_assignment
from src.randomized import randomized_construct
from src.evaluate import evaluate
from src.objective import score
from src.local_search import local_search
from src.ils import ils

def compat_sets(compat_df):
    return compat_df[compat_df['compatible']==1].groupby('employee_id')['desk_id'].apply(set).to_dict()

def solve_instance(inst_dir: str, plantilla: str, out_dir: str, seed: int,
                   w_valid: float, w_prefs: float, w_isolated: float,
                   ls_iters: int, ils_iters: int, perturb_k: int, ls_variant_default='first'):
    random.seed(seed)
    employees, desks, compat, params = load_instance(inst_dir)
    days = params.get("days", ["Mon","Tue","Wed","Thu","Fri"])
    compat_ok = compat_sets(compat)

    t0 = time.perf_counter()
    cons_assign, cons_group_days = construct_assignment(employees, desks, compat, days)
    cons_time = time.perf_counter() - t0
    cons_summary = evaluate(cons_assign, cons_group_days, employees)

    t0 = time.perf_counter()
    rnd_assign, rnd_group_days = randomized_construct(employees, desks, compat, days, alpha=0.3)
    rnd_time = time.perf_counter() - t0
    rnd_summary = evaluate(rnd_assign, rnd_group_days, employees)

    t0 = time.perf_counter()
    bi_assign, bi_metrics, _ = local_search(cons_assign, cons_group_days, employees, desks, compat_ok, days,
                                            w_valid, w_prefs, w_isolated, variant='best', max_iters=ls_iters)
    bi_time = time.perf_counter() - t0
    os.makedirs(out_dir, exist_ok=True)
    write_to_excel(plantilla, os.path.join(out_dir, f"{os.path.basename(inst_dir)}_ls_bi.xlsx"),
                   bi_assign, cons_group_days, bi_metrics)

    t0 = time.perf_counter()
    fi_assign, fi_metrics, _ = local_search(cons_assign, cons_group_days, employees, desks, compat_ok, days,
                                            w_valid, w_prefs, w_isolated, variant='first', max_iters=ls_iters)
    fi_time = time.perf_counter() - t0
    write_to_excel(plantilla, os.path.join(out_dir, f"{os.path.basename(inst_dir)}_ls_fi.xlsx"),
                   fi_assign, cons_group_days, fi_metrics)

    t0 = time.perf_counter()
    ils_assign, ils_metrics, _ = ils(cons_assign, cons_group_days, employees, desks, compat_ok, days,
                                     w_valid, w_prefs, w_isolated,
                                     ls_variant=ls_variant_default, ls_iters=ls_iters,
                                     ils_iters=ils_iters, perturb_k=perturb_k, accept_non_improving=False)
    ils_time = time.perf_counter() - t0
    write_to_excel(plantilla, os.path.join(out_dir, f"{os.path.basename(inst_dir)}_ils.xlsx"),
                   ils_assign, cons_group_days, ils_metrics)

    return {
        "instance": os.path.basename(inst_dir),
        "cons_valid": cons_summary["Valid assignments"],
        "cons_prefs": cons_summary["Employee preferences"],
        "cons_isolated": cons_summary["Isolated employees"],
        "cons_time": round(cons_time, 6),
        "rnd_valid": rnd_summary["Valid assignments"],
        "rnd_prefs": rnd_summary["Employee preferences"],
        "rnd_isolated": rnd_summary["Isolated employees"],
        "rnd_time": round(rnd_time, 6),
        "ls_bi_valid": bi_metrics["Valid assignments"],
        "ls_bi_prefs": bi_metrics["Employee preferences"],
        "ls_bi_isolated": bi_metrics["Isolated employees"],
        "ls_bi_time": round(bi_time, 6),
        "ls_fi_valid": fi_metrics["Valid assignments"],
        "ls_fi_prefs": fi_metrics["Employee preferences"],
        "ls_fi_isolated": fi_metrics["Isolated employees"],
        "ls_fi_time": round(fi_time, 6),
        "ils_valid": ils_metrics["Valid assignments"],
        "ils_prefs": ils_metrics["Employee preferences"],
        "ils_isolated": ils_metrics["Isolated employees"],
        "ils_time": round(ils_time, 6),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance_dir", required=True)
    ap.add_argument("--plantilla", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--w_valid", type=float, default=1.0)
    ap.add_argument("--w_prefs", type=float, default=1.0)
    ap.add_argument("--w_isolated", type=float, default=1.0)
    ap.add_argument("--ls_iters", type=int, default=100)
    ap.add_argument("--ils_iters", type=int, default=50)
    ap.add_argument("--perturb_k", type=int, default=3)
    args = ap.parse_args()

    out_dir = "salidas_t2"
    os.makedirs(out_dir, exist_ok=True)

    rows = []
    for inst in sorted([p for p in glob.glob(os.path.join(args.instance_dir, "*")) if os.path.isdir(p)]):
        rows.append(solve_instance(inst, args.plantilla, out_dir, seed=args.seed,
                                   w_valid=args.w_valid, w_prefs=args.w_prefs, w_isolated=args.w_isolated,
                                   ls_iters=args.ls_iters, ils_iters=args.ils_iters, perturb_k=args.perturb_k))

    pd.DataFrame(rows).to_csv(os.path.join(out_dir, "results_t2.csv"), index=False)

if __name__ == "__main__":
    main()

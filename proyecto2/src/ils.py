
import random
from typing import Dict, List
import pandas as pd
from src.local_search import local_search
from src.neighborhoods import clone_assignment, apply_neighbor

def perturb_k_swaps(assign: Dict, days: List[str], k: int, compat_ok) -> Dict:
    A = clone_assignment(assign)
    emps = list(A.keys())
    for _ in range(k):
        d = random.choice(days)
        e1, e2 = random.sample(emps, 2)
        mv = ('swap', d, e1, e2)
        newA = apply_neighbor(A, mv, compat_ok)
        if newA is not None:
            A = newA
    return A

def ils(initial_assign: Dict, group_days: Dict, employees: pd.DataFrame, desks: pd.DataFrame, compat_ok,
        days: List[str], w_valid=1.0, w_prefs=1.0, w_isolated=1.0,
        ls_variant='first', ls_iters=100, ils_iters=50, perturb_k=3, accept_non_improving=False):
    currA, curr_metrics, curr_val = local_search(initial_assign, group_days, employees, desks, compat_ok, days,
                                                 w_valid, w_prefs, w_isolated, variant=ls_variant, max_iters=ls_iters)
    bestA, best_val, best_metrics = currA, curr_val, curr_metrics

    for _ in range(ils_iters):
        A_pert = perturb_k_swaps(currA, days, perturb_k, compat_ok)
        A_desc, desc_metrics, desc_val = local_search(A_pert, group_days, employees, desks, compat_ok, days,
                                                      w_valid, w_prefs, w_isolated, variant=ls_variant, max_iters=ls_iters)
        if desc_val > curr_val or accept_non_improving:
            currA, curr_val, curr_metrics = A_desc, desc_val, desc_metrics
        if desc_val > best_val:
            bestA, best_val, best_metrics = A_desc, desc_val, desc_metrics

    return bestA, best_metrics, best_val

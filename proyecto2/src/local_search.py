
from typing import Dict, List
import pandas as pd
from src.neighborhoods import gen_swap_neighbors, gen_move_neighbors, available_free, apply_neighbor, clone_assignment
from src.objective import score

def local_search(assign: Dict, group_days: Dict, employees: pd.DataFrame, desks: pd.DataFrame, compat_ok,
                 days: List[str], w_valid=1.0, w_prefs=1.0, w_isolated=1.0,
                 variant='best', max_iters=100):
    desk_ids = desks['desk_id'].tolist()
    current = clone_assignment(assign)
    best_val, _ = score(current, group_days, employees, w_valid, w_prefs, w_isolated)

    it = 0
    improved = True
    while improved and it < max_iters:
        it += 1
        improved = False
        best_neighbor_val = best_val
        best_neighbor = None
        for d in days:
            free = list(available_free(current, d, set(desk_ids)))
            moves = list(gen_swap_neighbors(current, d)) + list(gen_move_neighbors(current, d, free, compat_ok))
            for mv in moves:
                newA = apply_neighbor(current, mv, compat_ok)
                if newA is None:
                    continue
                val, _ = score(newA, group_days, employees, w_valid, w_prefs, w_isolated)
                if val > best_val + 1e-9:
                    if variant == 'first':
                        current = newA
                        best_val = val
                        improved = True
                        break
                    else:
                        if val > best_neighbor_val:
                            best_neighbor_val = val
                            best_neighbor = newA
            if variant == 'first' and improved:
                break
        if variant == 'best' and best_neighbor is not None and best_neighbor_val > best_val + 1e-9:
            current = best_neighbor
            best_val = best_neighbor_val
            improved = True
    _, metrics = score(current, group_days, employees, w_valid, w_prefs, w_isolated)
    return current, metrics, best_val

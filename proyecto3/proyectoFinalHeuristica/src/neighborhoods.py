from typing import Dict, List

def clone_assignment(assign: Dict) -> Dict:
    return {e: dict(days) for e, days in assign.items()}

def available_free(assign: Dict, day: str, desks_set):
    used = set(a for e in assign for a in [assign[e][day]] if a != 'none')
    return desks_set - used

def gen_swap_neighbors(assign: Dict, day: str):
    emps = list(assign.keys())
    for i in range(len(emps)):
        for j in range(i+1, len(emps)):
            e1, e2 = emps[i], emps[j]
            if assign[e1][day] == 'none' and assign[e2][day] == 'none':
                continue
            yield ('swap', day, e1, e2)

def gen_move_neighbors(assign: Dict, day: str, free_desks: List[str], compat_ok):
    for e in assign.keys():
        cur = assign[e][day]
        for s in free_desks:
            if s != cur and (cur == 'none' or s != cur):
                if s in compat_ok.get(e, set()):
                    yield ('move', day, e, s)

def apply_neighbor(assign: Dict, move, compat_ok):
    t = move[0]
    day = move[1]
    newA = clone_assignment(assign)
    if t == 'swap':
        _, _, e1, e2 = move
        s1, s2 = newA[e1][day], newA[e2][day]
        if (s2 == 'none' or s2 in compat_ok.get(e1,set())) and (s1 == 'none' or s1 in compat_ok.get(e2,set())):
            newA[e1][day], newA[e2][day] = s2, s1
            return newA
        return None
    elif t == 'move':
        _, _, e, s = move
        for other in newA.keys():
            if other != e and newA[other][day] == s:
                newA[other][day] = 'none'
        newA[e][day] = s
        return newA
    return None

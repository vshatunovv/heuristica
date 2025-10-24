
from typing import Dict
import pandas as pd
from src.evaluate import evaluate

def score(assignment: Dict, group_days: Dict, employees_df: pd.DataFrame,
          w_valid=1.0, w_prefs=1.0, w_isolated=1.0):
    m = evaluate(assignment, group_days, employees_df)
    return w_valid*m['Valid assignments'] + w_prefs*m['Employee preferences'] - w_isolated*m['Isolated employees'], m

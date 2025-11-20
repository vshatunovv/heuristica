# scripts/stats_t3.py
import pandas as pd
from scipy.stats import friedmanchisquare

def main(results_csv='salidas_t3/results_t3.csv'):
    df = pd.read_csv(results_csv)

    methods_valid = ['cons_valid','rnd_valid','ls_bi_valid','ls_fi_valid','ils_valid','brkga_valid']

    # Armar listas por método
    data = [df[col].values for col in methods_valid]

    stat, p = friedmanchisquare(*data)
    print("Friedman sobre 'Valid assignments':")
    print(f"Statistic = {stat:.4f}, p-value = {p:.4e}")
    if p < 0.05:
        print("Hay diferencias significativas entre los métodos.")
    else:
        print("No se detectan diferencias significativas al 5%.")

if __name__ == '__main__':
    main()

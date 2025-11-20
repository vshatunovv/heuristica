
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_metric(df, metric_cols, title, out_path):
    plt.figure(figsize=(7,5))
    for col in metric_cols:
        plt.plot(df['instance'], df[col], marker='o', label=col)
    plt.title(title)
    plt.xlabel('Instance')
    plt.ylabel('Value')
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()

def main(results_csv='salidas_t2/results_t2.csv', out_dir='salidas_t2/plots'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(results_csv)

    plot_metric(df, ['cons_valid','rnd_valid','ls_bi_valid','ls_fi_valid','ils_valid'],
                'Valid Assignments', os.path.join(out_dir, 'valid_assignments.png'))
    plot_metric(df, ['cons_prefs','rnd_prefs','ls_bi_prefs','ls_fi_prefs','ils_prefs'],
                'Employee Preferences', os.path.join(out_dir, 'employee_preferences.png'))
    plot_metric(df, ['cons_isolated','rnd_isolated','ls_bi_isolated','ls_fi_isolated','ils_isolated'],
                'Isolated Employees', os.path.join(out_dir, 'isolated_employees.png'))
    plot_metric(df, ['cons_time','rnd_time','ls_bi_time','ls_fi_time','ils_time'],
                'Runtime (seconds)', os.path.join(out_dir, 'runtime_seconds.png'))

if __name__ == '__main__':
    main()

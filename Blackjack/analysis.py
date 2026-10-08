import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("results/threshold_results.csv")
grouped_ev = df.groupby("Threshold")["Expected Return"]

mean_expected_returns = grouped_ev.mean()
# print(f"Mean Expected Returns:\n{mean_expected_returns}")
standard_deviation = grouped_ev.std()
# print(f"Standard Deviation:\n{standard_deviation}")
standard_error = standard_deviation / np.sqrt(grouped_ev.count())
# print(f"Standard Error:\n{standard_error}")
# print(f"Columns: {df.columns.tolist()}")

t_critical = 2.776
margin_of_error = t_critical * standard_error

lower_ci = mean_expected_returns - margin_of_error
upper_ci = mean_expected_returns + margin_of_error

# print("Lower CI:")
# print(lower_ci)

# print("Upper CI:")
# print(upper_ci)

summary = pd.DataFrame({
    "Mean EV": mean_expected_returns,
    "Standard Deviation": standard_deviation,
    "Standard Error": standard_error,
    "95% CI Lower": lower_ci,
    "95% CI Upper": upper_ci
})

print(summary)
summary.to_csv("results/threshold_summary.csv")

plt.errorbar(mean_expected_returns.index, mean_expected_returns.values, yerr=margin_of_error.values)
plt.xlabel("Threshold")
plt.ylabel("Expected Return")
plt.title("Expected Return by Blackjack Hit Threshold (95% CI)")
plt.grid(True)
plt.savefig("results/threshold_expected_return.png", dpi=300, bbox_inches="tight")
plt.show()

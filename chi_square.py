from scipy import stats
import pickle

categories = 2 ** 16

with open(f"frequency_table_{categories}", "rb") as f:
    (frequency_table, end_value) = pickle.load(f)


chi_square = 0

expected = sum(frequency_table) / len(frequency_table)
for observed in frequency_table:
    chi_square += ((observed - expected) ** 2) / expected


degrees_of_freedom = categories - 1
significance = 0.95
critical_chi_square = stats.chi2.ppf(1 - significance, degrees_of_freedom)


print(f"Chi-Square Value: {chi_square}")
print(f"Critical Chi-Square Value: {critical_chi_square}")

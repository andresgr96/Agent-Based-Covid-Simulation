import numpy as np
from scipy.stats import chi2_contingency
# using Pearson’s chi-squared statistic
# corrected for the Yates’ continuity
observed = np.array([[50, 9], [15, 3]])
chi_val, p_val, dof, expected =  chi2_contingency(observed, correction=False)
print(chi_val, p_val, dof, expected)
import numpy
from excel import Excel
# from sklearn import datasets, linear_model
import statsmodels.api as sm

xlsx_path = "D:/Users/frotz/Documents/Freiburg VWL/Skripte/Semester 4/Seminar/Research/Results_GPT_estimation.xlsx"

# y var litigation_FY
# x var GPT_prob

x = numpy.array(Excel.get_data(xlsx_path, col_name="GPT_prob")).reshape(-1, 1)
y = numpy.array(Excel.get_data(xlsx_path, col_name="litigation_FY")).reshape(-1, 1)

# print(f'x:\n\n {x}')
# print(f'y:\n\n {y}')

# logr = linear_model.LogisticRegression()
# logr.fit(x, y)
#
# log_odds = logr.coef_
# odds = numpy.exp(log_odds)
#
# print(odds)

est = sm.OLS(y, x)
est2 = est.fit()
print(est2.summary())

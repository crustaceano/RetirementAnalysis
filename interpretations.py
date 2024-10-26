import numpy as np
from train import model, X_columns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Получаем коэффициенты и переменные
coefficients = model.coef_[0]
features = X_columns

# Создаем DataFrame для визуализации
coef_df = pd.DataFrame({'Feature': features, 'Coefficient': coefficients})
coef_df['Exp_Coefficient'] = np.exp(coefficients)  # Экспоненциальные коэффициенты для интерпретации

# Сортировка по абсолютному значению коэффициентов
coef_df = coef_df.sort_values(by='Coefficient', ascending=False)



plt.figure(figsize=(10, 6))
sns.barplot(x='Coefficient', y='Feature', data=coef_df)
plt.title('Logistic Regression Coefficients')
plt.xlabel('Coefficient Value')
plt.ylabel('Features')
plt.axvline(0, color='red', linestyle='--')  # Линия для нуля
plt.show()



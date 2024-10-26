import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess import data_train

# Подготовка данных
X, y = data_train.drop(columns=['erly_pnsn_flg']), data_train['erly_pnsn_flg']
X = X.drop(columns=['accnt_status', 'phn', 'email', 'cprtn_prd_d', 'prsnt_age'])
X_columns = X.columns

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Сохранение данных в CSV (закомментировано для примера)
# X_train.to_csv('data/X_train.csv', index=False)
# X_test.to_csv('data/X_test.csv', index=False)
# y_train.to_csv('data/y_train.csv', index=False)
# y_test.to_csv('data/y_test.csv', index=False)

# Инициализация и обучение модели логистической регрессии
model = LogisticRegression(class_weight={0: 1, 1: 10}, random_state=42, max_iter=250)
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

# ROC-кривая и AUC
y_prob = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='red', linestyle='--')  # Линия для случайной классификации
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.grid()
plt.show()

# Визуализация коэффициентов модели
coefficients = model.coef_[0]
coef_df = pd.DataFrame({'Feature': X_columns, 'Coefficient': coefficients})
coef_df['Exp_Coefficient'] = np.exp(coefficients)  # Экспоненциальные коэффициенты для интерпретации
coef_df = coef_df.sort_values(by='Coefficient', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Coefficient', y='Feature', data=coef_df[:10])
plt.title('Top 10 Logistic Regression Coefficients')
plt.xlabel('Coefficient Value')
plt.ylabel('Features')
plt.axvline(0, color='red', linestyle='--')  # Линия для нуля
plt.show()

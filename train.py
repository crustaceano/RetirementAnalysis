import pandas as pd
from sklearn.model_selection import train_test_split
from preprocess import data_train
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

X, y = data_train.drop(columns=['erly_pnsn_flg']), data_train['erly_pnsn_flg']

X = X.drop(columns=['accnt_status', 'phn', 'email', 'cprtn_prd_d', 'prsnt_age'])
# debuging
# print(X.columns)
X_columns = X.columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Сохранение данных в CSV
# X_train.to_csv('data/X_train.csv', index=False)
# X_test.to_csv('data/X_test.csv', index=False)
# y_train.to_csv('data/y_train.csv', index=False)
# y_test.to_csv('data/y_test.csv', index=False)

# Инициализация модели логистической регрессии
model = LogisticRegression(class_weight={0: 1, 1: 10}, random_state=42, max_iter=250)

# Обучение модели
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)


print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
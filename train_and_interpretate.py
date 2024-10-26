import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess import *
from catboost import CatBoostClassifier
import shap

# Подготовка данных
data_train = preprocess(data_train)


X, y = data_train.drop(columns=['erly_pnsn_flg']), data_train['erly_pnsn_flg']
X_columns = X.columns

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Инициализация модели
model = CatBoostClassifier(
    iterations=1000,      # количество итераций
    learning_rate=0.05,    # скорость обучения
    depth=10,              # глубина деревьев
    random_seed=42,       # фиксированный seed для воспроизводимости
    auto_class_weights="Balanced",  # автоматическая балансировка классов
    verbose=100           # вывод информации каждые 100 итераций
)

# Обучение модели
model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=100)
model.save_model('model/catboost_model.cbm')
# Предсказание и оценка
y_pred = model.predict(X_test)

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

# SHAP анализ
# Инициализация объекта для расчета SHAP-значений
explainer = shap.TreeExplainer(model)

# Вычисление SHAP-значений для тестового набора
shap_values = explainer.shap_values(X_test)

# Отобразим важность признаков
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, plot_type="bar")
plt.title("SHAP Feature Importance")
plt.show()

# Визуализация SHAP значений для первых 10 примеров
shap.initjs()
shap.plots.force(explainer.expected_value, shap_values[:10], X_test[:10])

# Визуализация зависимостей SHAP значений для наиболее важных признаков
# for feature in X.columns[:5]:  # Выберите 5 наиболее важных признаков
#     plt.figure(figsize=(10, 6))
#     shap.dependence_plot(feature, shap_values, X_test)
#     plt.title(f'SHAP Dependence Plot for {feature}')
#     plt.show()

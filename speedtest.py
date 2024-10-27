import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier

from config import encoding

# Загрузка и предобработка данных
data_train = pd.read_csv('train_data/preprocessed_for_train.csv', encoding=encoding)
X, y = data_train.drop(columns=['erly_pnsn_flg']), data_train['erly_pnsn_flg']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Определяем модели для сравнения
models = {
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(),
    "Logistic Regression": LogisticRegression(),
    "CatBoost": CatBoostClassifier(verbose=0),  # Отключение вывода CatBoost
}

# Функция для замера времени fit и inference
def measure_time(model, X_train, y_train, X_test):
    # Измеряем время fit
    start_time_fit = time.time()
    model.fit(X_train, y_train)
    end_time_fit = time.time()
    fit_time = end_time_fit - start_time_fit

    # Измеряем время inference
    start_time_inference = time.time()
    predictions = model.predict(X_test)
    end_time_inference = time.time()
    inference_time = end_time_inference - start_time_inference

    return fit_time, inference_time

# Проведем тестирование и выведем результаты
results = {}
for model_name, model in models.items():
    fit_time, inference_time = measure_time(model, X_train, y_train, X_test)
    results[model_name] = {'fit_time': fit_time, 'inference_time': inference_time}
    print(f"{model_name} - Fit time: {fit_time:.4f} seconds, Inference time: {inference_time:.4f} seconds")

# Сортируем модели по времени fit и вывода (inference)
sorted_fit_results = dict(sorted(results.items(), key=lambda item: item[1]['fit_time']))
sorted_inference_results = dict(sorted(results.items(), key=lambda item: item[1]['inference_time']))

print("\nModels ranked by fit time:")
for model_name, times in sorted_fit_results.items():
    print(f"{model_name} - Fit time: {times['fit_time']:.4f} seconds")

print("\nModels ranked by inference time:")
for model_name, times in sorted_inference_results.items():
    print(f"{model_name} - Inference time: {times['inference_time']:.4f} seconds")

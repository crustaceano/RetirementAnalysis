from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import os
import pandas as pd
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier
from lime.lime_tabular import LimeTabularExplainer
from preprocess import *
from merge import *
from clear import *

# Загрузка модели
model = CatBoostClassifier()
model.load_model('model/catboost_model.cbm')
preprocessed_data = pd.read_csv('preprocessed.csv', encoding=encoding)
app = FastAPI()

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return HTMLResponse(open("templates/index.html").read())

@app.post("/predict/")
async def make_prediction(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Путь для временных файлов
    users_info_path = 'temp_users_info.csv'
    transactions_info_path = 'temp_transactions_info.csv'
    result_path = 'result.csv'

    try:
        with open(users_info_path, "wb") as f:
            f.write(await file1.read())
        with open(transactions_info_path, "wb") as f:
            f.write(await file2.read())

        # Выполняем инференс
        data = merge(users_info_path, transactions_info_path, 'data/merged_train.csv')
        cleared_data = clear(data)
        data_ids, preprocessed_data = preprocess(cleared_data)
        y_pred = model.predict(preprocessed_data)

        predictions_df = pd.DataFrame({'erly_pnsn_flg': y_pred})
        preprocessed_data.to_csv('preprocessed.csv', index=False, encoding=encoding)

        result_df = pd.concat([data_ids[['accnt_id']].reset_index(drop=True), predictions_df], axis=1)
        result_df.to_csv(result_path, index=False)

        # Логируем количество обработанных записей
        print(f"Processed {len(result_df)} records.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Удаляем временные файлы после использования
        for path in [users_info_path, transactions_info_path]:
            if os.path.exists(path):
                os.remove(path)

    # Возвращаем результат для скачивания
    return FileResponse(path=result_path, filename="result.csv", media_type='text/csv')


@app.post("/interpret/")
async def interpret(sample_index: int = Form(...)):
    print(f"Received sample_index: {sample_index}")

    # Загружаем предобработанные данные
     # Укажите нужную кодировку

    # Проверка на допустимость индекса
    if sample_index < 0 or sample_index >= len(preprocessed_data):
        raise HTTPException(status_code=400, detail="Индекс образца вне диапазона.")

    # Подготавливаем данные для LIME
    X = preprocessed_data.drop(columns=['erly_pnsn_flg'])
    lime_explainer = LimeTabularExplainer(
        X.values,
        mode='classification',
        feature_names=X.columns,
        class_names=['No Early Pension', 'Early Pension'],
        discretize_continuous=True
    )

    # Генерируем интерпретацию
    exp = lime_explainer.explain_instance(
        X.iloc[sample_index].values,
        model.predict_proba,
        num_features=10
    )

    # Сохраняем изображение интерпретации
    plt.figure()
    exp.as_pyplot_figure()
    plt.title(f'LIME Interpretation for Sample {sample_index}')
    image_path = f'static/lime_interpretation_sample_{sample_index}.png'
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()

    return JSONResponse(content={"image_url": f"/static/lime_interpretation_sample_{sample_index}.png"})
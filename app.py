from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()


@app.post("/predict/")
async def make_prediction(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Чтение CSV файла
    data = pd.read_csv(file.file)

    # Здесь вызываем модель для предсказания
    predict = model.predict(data)  # Предположим, model - это ваша обученная модель

    # Формируем ответ
    return {"predictions": predict.tolist()}  # Возвращаем предсказания в формате JSON

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from inference import inference  # Импортируем функцию inference

app = FastAPI()

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return HTMLResponse(open("templates/index.html").read())

@app.post("/predict/")
async def make_prediction(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Сохраняем загруженные файлы во временные директории
    users_info_path = 'temp_users_info.csv'
    transactions_info_path = 'temp_transactions_info.csv'
    result_path = 'result.csv'

    with open(users_info_path, "wb") as f:
        f.write(await file1.read())
    with open(transactions_info_path, "wb") as f:
        f.write(await file2.read())

    # Выполняем инференс
    inference(users_info_path, transactions_info_path, result_path)

    # Удаляем временные файлы после использования
    os.remove(users_info_path)
    os.remove(transactions_info_path)

    # Возвращаем результат для скачивания
    return FileResponse(path=result_path, filename="result.csv", media_type='text/csv')

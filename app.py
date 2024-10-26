from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import os
from inference import inference  # Импортируем функцию inference

app = FastAPI()

@app.get("/")
async def main():
    html_content = """
    <html>
        <head>
            <title>Upload Files for Prediction</title>
        </head>
        <body>
            <h1>Upload Files for Prediction</h1>
            <form action="/predict/" enctype="multipart/form-data" method="post">
                <input name="file1" type="file" required>
                <input name="file2" type="file" required>
                <button type="submit">Predict</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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

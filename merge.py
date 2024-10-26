import pandas as pd
# from tqdm import tqdm
from config import *

# config

# Чтение данных
users_data = pd.read_csv(USERS_INFO_PATH, sep=';', encoding=encoding)
transactions_data = pd.read_csv(TRANSACTIONS_INFO_PATH, sep=';', encoding=encoding)

# Преобразование даты
transactions_data['oprtn_date'] = pd.to_datetime(transactions_data['oprtn_date'])

# Группировка и сводная таблица
summary_data = transactions_data.pivot_table(
    index='accnt_id',
    columns='cmmnt',
    values='sum',
    aggfunc='sum',
    fill_value=0
).reset_index()

# Переименование столбцов
summary_data.columns = [f"{col} summary" if col != 'accnt_id' else col for col in summary_data.columns]

# Минимальная и максимальная дата транзакций
dates_summary = transactions_data.groupby('accnt_id')['oprtn_date'].agg(['min', 'max']).reset_index()
dates_summary.columns = ['accnt_id', 'min_oprtn_date', 'max_oprtn_date']
summary_data = pd.merge(summary_data, dates_summary, on='accnt_id', how='outer')

# Создание бинарных признаков для типов транзакций
transaction_exists = transactions_data.groupby(['accnt_id', 'cmmnt']).size().unstack(fill_value=0).astype(int)
transaction_exists.columns = [f"{col}_exists" for col in transaction_exists.columns]
summary_data = pd.merge(summary_data, transaction_exists, on='accnt_id', how='outer')

# Объединение данных с информацией о пользователях
merged_data = pd.merge(summary_data, users_data, on='accnt_id', how='outer')

# Сохранение в CSV
merged_data.to_csv(DATA_DIR + 'merged.csv', sep=';', index=False, encoding=encoding)

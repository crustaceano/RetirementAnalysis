import pandas as pd

# config
DATA_DIR = 'train_data/'
USERS_INFO_PATH = DATA_DIR + 'cntrbtrs_clnts_ops_trn.csv'
TRANSACTIONS_INFO_PATH = DATA_DIR + 'trnsctns_ops_trn.csv'
encoding = 'windows-1251'  # Кодировка файлов
users_data = pd.read_csv(USERS_INFO_PATH, sep=';', encoding=encoding)
transactions_data = pd.read_csv(TRANSACTIONS_INFO_PATH, sep=';', encoding=encoding)

transaction_types = transactions_data['cmmnt'].unique()


def merge_transactions_and_users_data():
    transactions_data['oprtn_date'] = pd.to_datetime(transactions_data['oprtn_date'])

    # Групируем таблицу по accnt_id и создаем сводную таблицу по суммам транзакций
    summary_data = transactions_data.pivot_table(
        index='accnt_id',
        columns='cmmnt',
        values='sum',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Переименовываем столбцы
    summary_data.columns = [f"{col} summary" if col != 'accnt_id' else col for col in summary_data.columns]

    # Добавляем временные фичи
    dates_summary = transactions_data.groupby('accnt_id')['oprtn_date'].agg(['min', 'max']).reset_index()
    dates_summary.columns = ['accnt_id', 'min_oprtn_date', 'max_oprtn_date']
    summary_data = pd.merge(summary_data, dates_summary, on='accnt_id', how='outer')

    # Создаем бинарные фичи для типов транзакций
    for transaction_type in transaction_types:
        summary_data[f"{transaction_type}_exists"] = (transactions_data.groupby('accnt_id')['cmmnt']
            .transform(lambda x: transaction_type in x.values)).astype(int)

    # Объединяем данные с информацией о пользователях
    merged_data = pd.merge(summary_data, users_data, on='accnt_id', how='outer')

    merged_data.to_csv(DATA_DIR + 'merged.csv', index=False, encoding=encoding)

merge_transactions_and_users_data()

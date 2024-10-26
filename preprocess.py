import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
from config import *


TRAIN_DATA_PATH = DATA_DIR + '/' + 'clear_train.csv'
data_train = pd.read_csv(TRAIN_DATA_PATH, sep=',', encoding='utf-8')

def scale_data(data, num_features):
    # Попробуем загрузить сохраненный скейлер
    try:
        scaler = joblib.load('model/standard_scaler.pkl')
        data[num_features] = scaler.transform(data[num_features])
        print("Скейлер загружен и данные успешно преобразованы.")
    except FileNotFoundError:
        # Если скейлер не найден, создаем новый и обучаем его
        scaler = StandardScaler()
        data[num_features] = scaler.fit_transform(data[num_features])
        joblib.dump(scaler, 'model/standard_scaler.pkl')
        print("Создан новый скейлер и данные успешно преобразованы.")

    return data


def encode_categorical_features(data_train, categorical_features):
    # Попробуем загрузить сохраненный OneHotEncoder
    try:
        category_encoder = joblib.load('model/category_encoder.pkl')
        print("OneHotEncoder загружен.")
    except FileNotFoundError:
        # Если скейлер не найден, создаем новый и обучаем его
        category_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        category_encoder.fit(data_train[categorical_features])
        joblib.dump(category_encoder, 'model/category_encoder.pkl')
        print("Создан новый OneHotEncoder и обучен.")

    # Кодируем категориальные признаки
    encoded_features = category_encoder.transform(data_train[categorical_features])
    encoded_columns = category_encoder.get_feature_names_out(categorical_features)
    encoded_df = pd.DataFrame(encoded_features, columns=encoded_columns)

    return encoded_df

def preprocess(data_train):
    # Поля
    id_fetures = ["clnt_id", "accnt_id"]
    num_features = ["pnsn_age"] #cprtn_prd_d / prsnt_age
    bool_features = ["phn", "email", "lk", "assgn_npo", "assgn_ops"]
    class_features = ["gndr", "addrss_type"] #accnt_status
    date_features = ["accnt_bgn_date", "min_oprtn_date", "max_oprtn_date"]
    label_features = ["erly_pnsn_flg"]
    text_features = ["rgn", "prvs_npf"]
    categorical_features = class_features + text_features
    num_merge_features = ['Возврат выплаченных сумм (ОПС) summary',
     'Восполнение (ОПС) summary',
     'Закрытие договора ОПС summary',
     'Компенсация(ОПС) summary',
     'Корректировка записей регистров (ОПС) summary',
     'Назначение пенсии (ОПС) summary',
     'Начисление (ОПС) summary',
     'Начисление пенсии (ОПС) summary',
     'Перевод между счетами ОПС summary',
     'Поступление взносов ОПС summary',
     'Приостановление/возобновление/прекращение выплат пенсии (ОПС) summary',
     'Распределение ИД ОПС summary',
     'Решение о единовременной выплате (ОПС) summary',
     'Возврат выплаченных сумм (ОПС)_exists',
     'Восполнение (ОПС)_exists',
     'Компенсация(ОПС)_exists',
     'Корректировка записей регистров (ОПС)_exists',
     'Назначение пенсии (ОПС)_exists',
     'Начисление (ОПС)_exists',
     'Начисление пенсии (ОПС)_exists',
     'Поступление взносов ОПС_exists',
     'Распределение ИД ОПС_exists',
     'Решение о единовременной выплате (ОПС)_exists']

    # Пример использования
    # Загрузите данные
    # data = pd.read_csv('your_file.csv')

    # Масштабируйте числовые признаки
    data_train = scale_data(data_train, num_features + num_merge_features)

    # print(data_train.columns)
    # data_train = data_train.drop(columns=drop_columns)
    data_ids = data_train[id_fetures]
    data_train = data_train.drop(columns=id_fetures)
    # categorical_features = data_train.select_dtypes(include=['object', 'category']).columns.tolist()
    # class_features = ["gndr", "prvs_npf", "addrss_type"]
    # categorical_features = ['rgn'] + class_features
    # print(categorical_features)
    data_train = data_train.drop(columns=['brth_plc', 'lk', 'pnsn_age'])

    # Определяем топ-10 значений для каждого категориального признака
    def get_top_values(df, column, top_n=15):
        top_values = df[column].value_counts().index[:top_n]
        return df[column].apply(lambda x: x if x in top_values else 'other')


    # Применяем функцию к каждому категориальному столбцу
    for col in categorical_features:
        data_train[col] = get_top_values(data_train, col)

    # Приводим все значения в категориальных столбцах к строковому типу
    data_train[categorical_features] = data_train[categorical_features].astype(str)

    # Загружаем или создаем OneHotEncoder


    encoded_df = encode_categorical_features(data_train, categorical_features)
    # Объединяем закодированные признаки с основным DataFrame
    data_train = pd.concat([data_train.drop(columns=categorical_features), encoded_df], axis=1)

    # Временные признаки забудем пока что
    data_train = data_train.drop(columns=date_features)



    print(data_train.columns)

    # Теперь у вас есть закодированный DataFrame
    print(data_train.head())  # Проверка первых строк итогового DataFrame

    assert data_train.select_dtypes(include=['object', 'category']).columns.tolist() == [], "Плохо предобработал"
    print(data_train.select_dtypes(include=['object', 'category']).columns.tolist())

    return data_ids, data_train

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import joblib

import numpy as np
from config import *

TRAIN_DATA_PATH = DATA_DIR + '/' + 'clear_train.csv'

data_train = pd.read_csv(TRAIN_DATA_PATH, sep=',', encoding='utf-8')  # в дальнейшем encoding

# helpfull
id_fetures = ["clnt_id", "accnt_id"]
num_features = ["prsnt_age", "cprtn_prd_d", "pnsn_age"]
bool_features = ["phn", "email", "lk", "assgn_npo", "assgn_ops"]
class_features = ["slctn_nmbr", "gndr", "prvs_npf",
                  "addrss_type"]  # сделать груп бай по прошлым банкам и удалить кринжей
date_features = ["accnt_bgn_date"]
label_features = ["erly_pnsn_flg"]
text_features = ["brth_plc", "rgn"]  # reg ?= class_f

IDS = data_train[id_fetures]

# удалим не нужные столбцы
data_train = data_train.drop(columns=(['brth_plc', 'Unnamed: 0'] + id_fetures))

# category_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
category_encoder = joblib.load('model/category_encoder.pkl')
encoded_features = category_encoder.transform(data_train[["rgn"] + class_features])

# сохранение - загрузка енкодера
# joblib.dump(category_encoder, 'model/category_encoder.pkl')

encoded_columns = category_encoder.get_feature_names_out(["rgn"] + class_features)

# Создание DataFrame из закодированных данных
encoded_df = pd.DataFrame(encoded_features, columns=encoded_columns)

# Объединение с исходным DataFrame
data_train = pd.concat([data_train, encoded_df], axis=1)
data_train = data_train.drop(columns=(["rgn"] + class_features))

# Удаление временной фичи(временно)
data_train = data_train.drop(columns=(['accnt_bgn_date']))





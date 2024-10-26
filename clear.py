import pandas as pd
import numpy as np


def normalize_feature(df, features, type='std'):
    if type=='std':
        df[features] = (df[features] - df[features].mean()) / df[features].std()
    elif type == 'log':
        df[features] = np.sign(df[features]) * np.log(np.abs(df[features]) + 1)
    elif type == 'minmax':
        df[features] = (df[features] - df[features].min()) / (df[features].max() - df[features].min())

def normalize_df(df, features, log=False):
    for nf in features:
        min_nf = df[nf].min()
        max_nf = df[nf].max()
        delta = max_nf - min_nf

        if log:
            print(nf + ":")
            print(delta, max_nf, min_nf)
            print()

        if delta > 1000:
            normalize_feature(df, nf, type="log")
        else:
            normalize_feature(df, nf, type="minmax")

        if log:
            min_nf = df[nf].min()
            max_nf = df[nf].max()
            # print(nf + " normalized:")
            # print(max_nf - min_nf)
            # print('___________________________________________')

def fill_nans(df, features, nan_value=None):
    for f in features:
        df[f] = df[f].fillna(nan_value)

def fill_bool_features(df, features, key_word="да"):
    for bf in features:
        df[bf] = df[bf].apply(lambda x: 1 if x == key_word else 0)

def fill_cat_features(df, features):
    for cf in features:
        lst = df[cf].unique().tolist()
        df[cf] = df[cf].apply(lambda x: lst.index(x) + 1)


def clear(users_data):
    # Drop columns
    users_data = users_data.drop(columns=["brth_yr", "pstl_code", "okato", "dstrct", "city", "sttlmnt", "slctn_nmbr"])
    users_data = users_data.drop(columns=["accnt_status", "cprtn_prd_d", "prsnt_age"])
    users_data = users_data.drop(columns=['Передача СПН в другой фонд по Уведомлениям ПФР о разделении ИЛС (ОПС)_exists',
                 'Приостановление/возобновление/прекращение выплат пенсии (ОПС)_exists',
                 'Перевод в резерв Фонда (ОПС)_exists',
                 'Перевод между счетами ОПС_exists',
                 'Закрытие договора ОПС_exists',
                 'Перевод в резерв Фонда (ОПС) summary',
                 'Передача СПН в другой фонд по Уведомлениям ПФР о разделении ИЛС (ОПС) summary'])

    # Structure features
    id_fetures = ["clnt_id", "accnt_id"]
    num_features = ["pnsn_age"]
    bool_features = ["phn", "email", "lk", "assgn_npo", "assgn_ops"]
    class_features = ["gndr", "addrss_type"]
    date_features = ["accnt_bgn_date", "min_oprtn_date", "max_oprtn_date"]
    label_features = ["erly_pnsn_flg"]
    text_features = ["rgn", "prvs_npf"]
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

    # remove nans
    fill_nans(users_data, id_fetures + num_features + num_merge_features + class_features + bool_features, 0)
    fill_nans(users_data, text_features + date_features, "None")

    # normalize
    normalize_df(users_data, num_features + num_merge_features)

    # fill cat and bool features
    fill_bool_features(users_data, bool_features)
    fill_cat_features(users_data, class_features)

    # return
    return users_data


# clear(r'C:\Users\User\Jupyter Notebooks\PENSII\train_data\merged.csv', 'clearData.csv')
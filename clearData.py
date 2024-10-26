import pandas as pd
import numpy as np
from extractDataFromCsv import *


def make_regions_dict(reg_df, reg_db, reg_population, reg_lifespan, reg_salary):
    """
    :param reg_df:
    :param reg_db:
    :param reg_population:
    :param reg_lifespan:
    :param reg_salary:
    :return: regions dict
    """
    reg_dict = {}

    # iterate by regions in user data
    for reg in reg_df:
        description = {
            'popularity': None,
            'lifespan': None,
            'salary': None
        }

        # iterate by database regions
        n = len(reg_db)
        for i in range(n):

            if type(reg) != str or type(reg_db[i]) != str:
                break

            # find similar regions
            if len(reg.lstrip()) > 5 and len(reg_db[i].lstrip()) > 5:
                if reg_db[i].lstrip().lower()[:5] == reg.lstrip().lower()[:5]:
                    description['popularity'] = reg_population[i]
                    description['lifespan'] = reg_lifespan[i]
                    description['salary'] = reg_salary[i]
                    break
        # if not founded
        if not description:
            description['popularity'] = sum(reg_population) / n
            description['lifespan'] = sum(reg_lifespan) / n
            description['salary'] = sum(reg_salary) / n
        reg_dict[reg] = description
    # return
    return reg_dict

def add_regions_features(df, db_path="Information.sqlite"):
    """
    :param df:
    :param db_path:
    :add: new features to dataframe
    """
    # form request to database
    cols = ['name', 'population', "average_lifespan", "average_salary"]
    result_data = extract_data_from_db("regions", cols, db_path)

    # form regions lsts and features lsts
    reg_df = df["rgn"].unique().tolist()

    reg_name = [x[0] for x in result_data]
    reg_population = [x[1] for x in result_data]
    reg_lifespan = [x[2] for x in result_data]
    reg_salary = [x[3] for x in result_data]

    # get dict with features
    reg_dict = make_regions_dict(reg_df, reg_name, reg_population, reg_lifespan, reg_salary)

    # change df
    df['rgn_popl'] = df['rgn'].apply(lambda x: reg_dict[x]['popularity'])
    df['rgn_lfspn'] = df['rgn'].apply(lambda x: reg_dict[x]['lifespan'])
    df['rgn_sal'] = df['rgn'].apply(lambda x: reg_dict[x]['salary'])

def normalize_feature(df, col, type='std'):
    """
    :param df:
    :param col: column of df
    :param type: type of normalization std / log / minmax
    :change: dataframe nums feature to normalized view
    """
    if type=='std':
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    elif type == 'log':
        df[col] = np.sign(df[col]) * np.log(np.abs(df[col]) + 1)
    elif type == 'minmax':
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

def normalize_df(df, features, log=False):
    """
    :param df:
    :param features: int or float columns of dataframe
    :param log: print information about normalization
    :return:
    """
    for nf in features:
        min_nf = df[nf].min()
        max_nf = df[nf].max()
        delta = max_nf - min_nf

        if log:
            print(nf + ":")
            print(delta, max_nf, min_nf)
            print()

        # if delta too large use log normalization, minmax else
        if delta > 1000:
            normalize_feature(df, nf, type="log")
        else:
            normalize_feature(df, nf, type="minmax")

        if log:
            min_nf = df[nf].min()
            max_nf = df[nf].max()
            print(nf + " normalized:")
            print(max_nf - min_nf)
            print('___________________________________________')

def fill_nans(df, features, nan_value=None):
    """
    :param df:
    :param features: columns of dataframe
    :param nan_value: value to fill nans
    :fill: nans if columns by default value
    """
    for f in features:
        df[f] = df[f].fillna(nan_value)

def fill_bool_features(df, features, key_word="да"):
    """
    :param df:
    :param features: bool columns of dataframe
    :param key_word: value to fill features if it equals to 1
    :fill: features to key_value
    """
    for bf in features:
        df[bf] = df[bf].apply(lambda x: 1 if x == key_word else 0)

def fill_cat_features(df, features):
    """
    :param df:
    :param features: cat columns of dataframe
    :fill: features different numbers
    """
    for cf in features:
        lst = df[cf].unique().tolist()
        df[cf] = df[cf].apply(lambda x: lst.index(x) + 1)


def clear(USERS_INFO_PATH, RESULT_PATH, encoding="windows-1251"):
    """
    :param USERS_INFO_PATH: path to user data
    :param RESULT_PATH: path to save result
    :param encoding: encoding of user data
    clear user data and save result
    """
    users_data = pd.read_csv(USERS_INFO_PATH, sep=';', encoding=encoding)

    # Parse region to it description
    add_regions_features(users_data)

    # Drop columns
    users_data = users_data.drop(columns=["brth_yr", "pstl_code", "okato", "dstrct", "city", "sttlmnt", "slctn_nmbr",
                                          "brth_plc"])
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

    # save
    users_data.to_csv(RESULT_PATH)


#clear(r'C:\Users\User\Jupyter Notebooks\PENSII\train_data\merged.csv', 'clearData.csv')
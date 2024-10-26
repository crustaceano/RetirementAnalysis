from merge import merge
from clear import *
from preprocess import *
from catboost import CatBoostClassifier

# Загрузка модели
model = CatBoostClassifier()
model.load_model('model/catboost_model.cbm')


def inference(users_info_path, transactions_info_path, result_path):
    data = merge(users_info_path, transactions_info_path, 'data/merged_train.csv')
    print("Merged succsessfuly")
    cleared_data = clear(data)
    print('cleared')
    data_ids, preprocessed_data = preprocess(cleared_data)
    print('preprocessed')
    y_pred = model.predict(preprocessed_data)
    print('predicted')
    predictions_df = pd.DataFrame({'erly_pnsn_flg': y_pred})

    result_df = pd.concat([data_ids[['accnt_id']].reset_index(drop=True), predictions_df], axis=1)
    result_df.to_csv(result_path, index=False)

inference('train_data/cntrbtrs_clnts_ops_trn.csv', 'train_data/trnsctns_ops_trn.csv', 'result/res.csv')






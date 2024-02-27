import pandas as pd
import numpy as np
from service.paths import *
from sys import argv
from sklearn.ensemble import RandomForestRegressor
from service.load import get_model
from training.train_data import prep_test_X
from datetime import datetime as dt

if len(argv) > 1:
    new_data = path_to_data_dir / Path(argv[1])
    # run_feature_clean(new_data)
try:
    new_test = pd.read_csv(new_data)
except FileNotFoundError:
    print("Новый датасет кладите в папку проекта data")
    exit(1)

model = get_model()


def get_temp_forecast_by_24(df: pd.DataFrame):
    result = []

    def make_dt_col(row_date, row_time):
        return pd.to_datetime(row_date) + pd.to_timedelta(row_time, unit='h')

    df['datetime'] = df.apply(lambda x: make_dt_col(x['date'], x['time']), axis=1)
    df.drop(["date",'weather_fact',"weather_pred"], inplace=True, axis=1)
    # print(type(df))
    for i in range(0, len(df), 24):
        slice_end = min(i + 24, len(df))
        result.append(prep_test_X(df.iloc[i:slice_end]) )
    return result


forecast = get_temp_forecast_by_24(new_test)
energy_set = pd.DataFrame(columns=["date", "predict"])

predicts=[]
dates=[]
for day in forecast:
    # print(day)
    energy = model.predict(day)
    # print(energy)
    predicts.append(sum(energy))
    last_row = day.iloc[-1].name
    dates.append(dt.fromtimestamp(int(last_row.timestamp())).date())
energy_set["predict"] = predicts
energy_set["date"] = dates
energy_set.to_csv("result.csv", float_format='%.2f', mode='w',index=False)

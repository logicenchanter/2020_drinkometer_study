import numpy as np
import pandas as pd
import os
from datetime import date
from os import listdir
from os.path import isfile, join
import sys
from writer import loco_writer2020
from weight_op import weight_organizer
from weight_op import wistar_w_w

def d_day_index(f, n):
    for i1 in range(n):
        f.loc[i1, ['day_index']] = i1+1
    return f


def state_hour(f, n):
    for i2 in range(n + 1):
        dn = 24 * i2
        f.loc[dn:dn + 6, ['state']] = str('dark')
        f.loc[dn + 7:dn + 18, ['state']] = str('light')
        f.loc[dn + 19:dn + 24, ['state']] = str('dark')
    return f


def m_day_and_hour_index(f, n):
    h_counter = 1
    for i3 in range(n + 1):
        dn = 24 * i3
        f.loc[dn:dn + 23, ['day_index']] = i3+1
        for j3 in range(24):
            interval_m = dn + j3
            f.loc[interval_m:interval_m + 1, ['hour_index']] = h_counter
            h_counter = h_counter + 1
    return f


def state_(f, n):
    for i4 in range(n + 1):
        dn = 1440 * i4
        f.loc[dn:dn + 419, ['state']] = str('dark')
        f.loc[dn + 420:dn + 1139, ['state']] = str('light')
        f.loc[dn + 1140:dn + 1439, ['state']] = str('dark')
    return f


def day_and_hour_index(f, n):
    h_counter = 1
    for i5 in range(n + 1):
        dn = 1440 * i5
        f.loc[dn:dn + 1439, ['day_index']] = i5+1
        for j5 in range(24):
            interval_m = dn + (j5*60)
            f.loc[interval_m:interval_m + 60, ['hour_index']] = h_counter
            h_counter = h_counter + 1
    return f

def threshup_():
    #DOI 10.1211/jpp.60.1.0008
    th_u_comft = 3.38 + 0.52
    #th_u_stretched = 4.63 + 0.44
    #th_u_burst = 6.63 + 0.92
    return th_u_comft


def real_consump(val, w, p):
    a = np.nan
    if p == 5:
        a = (val*0.05*0.789)/(w) *1000
    elif (p == 10):
        a = (val*0.1*0.789)/(w) *1000
    elif ( p == 20 ):
        a = (val*0.2*0.789)/(w) *1000
    else:
        print("You messed up the input in real_consump function")
    return(a)

def writer_(main_df, list_of_them, number, method, a_n, path):
    print(number)
    file = pd.read_excel("{}\{}".format(path, list_of_them[number]), skiprows=35)
    if method == str('dep_onlywater'):
        file_ = file.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'time', 'Unnamed: 2': 'animal',
                                     'Unnamed: 3': 'box', '[ml]': 'water'})
        extracted_a1 = file_[file_['box'] == a_n]
        list_index = list(file_[file_['box'] == a_n].index)
        for i6 in range(len(extracted_a1)):
            ind0 = main_df.loc[(main_df['date'] == extracted_a1['date'][list_index[i6]].strftime('%Y-%m-%d')) &
                               (main_df['time'] == extracted_a1['time'][list_index[i6]].strftime('%H:%M:%S'))].index[0]
            main_df.loc[ind0, 'water'] = extracted_a1['water'][list_index[i6]]
    elif method == str('ade_only'):
        file_ = file.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'time', 'Unnamed: 2': 'animal',
                                     'Unnamed: 3': 'box', '[ml]': 'water', '[ml].1': 'alcohol_5',
                                     '[ml].2': 'alcohol_10', '[ml].3': 'alcohol_20'})
        extracted_a1 = file_[file_['box'] == a_n]
        list_index = list(file_[file_['box'] == a_n].index)
        for i7 in range(len(extracted_a1)):
            ind1 = main_df.loc[(main_df['date'] == extracted_a1['date'][list_index[i7]].strftime('%Y-%m-%d')) &
                               (main_df['time'] == extracted_a1['time'][list_index[i7]].strftime('%H:%M:%S'))].index[0]
            main_df.loc[ind1, 'water'] = extracted_a1['water'][list_index[i7]]
            main_df.loc[ind1, 'alcohol_5'] = extracted_a1['alcohol_5'][list_index[i7]]
            main_df.loc[ind1, 'alcohol_10'] = extracted_a1['alcohol_10'][list_index[i7]]
            main_df.loc[ind1, 'alcohol_20'] = extracted_a1['alcohol_20'][list_index[i7]]
    elif method == str('ade_oxy'):
        file_ = file.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'time', 'Unnamed: 2': 'animal',
                                     'Unnamed: 3': 'box', '[ml]': 'water', '[ml].1': 'alcohol_5',
                                     '[ml].2': 'alcohol_10', '[ml].3': 'alcohol_20'})
        extracted_a1 = file_[file_['box'] == a_n]
        list_index = list(file_[file_['box'] == a_n].index)
        for i8 in range(len(extracted_a1)):
            ind2 = main_df.loc[(main_df['date'] == extracted_a1['date'][list_index[i8]].strftime('%Y-%m-%d')) &
                               (main_df['time'] == extracted_a1['time'][list_index[i8]].strftime('%H:%M:%S'))].index[0]
            main_df.loc[ind2, 'water'] = extracted_a1['water'][list_index[i8]]
            main_df.loc[ind2, 'alcohol_5'] = extracted_a1['alcohol_5'][list_index[i8]]
            main_df.loc[ind2, 'alcohol_10'] = extracted_a1['alcohol_10'][list_index[i8]]
            main_df.loc[ind2, 'alcohol_20'] = extracted_a1['alcohol_20'][list_index[i8]]
            main_df.loc[ind2, 'oxytocin'] = str('applied')
    elif method == str('dep_quinine'):
        file_ = file.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'time', 'Unnamed: 2': 'animal',
                                     'Unnamed: 3': 'box', '[ml]': 'water'})
        extracted_a1 = file_[file_['box'] == a_n]
        list_index = list(file_[file_['box'] == a_n].index)
        for i9 in range(len(extracted_a1)):
            ind3 = main_df.loc[(main_df['date'] == extracted_a1['date'][list_index[i9]].strftime('%Y-%m-%d')) &
                               (main_df['time'] == extracted_a1['time'][list_index[i9]].strftime('%H:%M:%S'))].index[0]
            main_df.loc[ind3, 'water'] = extracted_a1['water'][list_index[i9]]
            main_df.loc[ind3, 'quinine'] = str('applied')
    elif method == str('ade_quinine'):
        file_ = file.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'time', 'Unnamed: 2': 'animal',
                                     'Unnamed: 3': 'box', '[ml]': 'water', '[ml].1': 'alcohol_5',
                                     '[ml].2': 'alcohol_10', '[ml].3': 'alcohol_20'})
        extracted_a1 = file_[file_['box'] == a_n]
        list_index = list(file_[file_['box'] == a_n].index)
        for i10 in range(len(extracted_a1)):
            ind4 = main_df.loc[(main_df['date'] == extracted_a1['date'][list_index[i10]].strftime('%Y-%m-%d')) &
                               (main_df['time'] == extracted_a1['time'][list_index[i10]].strftime('%H:%M:%S'))].index[0]
            main_df.loc[ind4, 'water'] = extracted_a1['water'][list_index[i10]]
            main_df.loc[ind4, 'alcohol_5'] = extracted_a1['alcohol_5'][list_index[i10]]
            main_df.loc[ind4, 'alcohol_10'] = extracted_a1['alcohol_10'][list_index[i10]]
            main_df.loc[ind4, 'alcohol_20'] = extracted_a1['alcohol_20'][list_index[i10]]
            main_df.loc[ind4, 'quinine'] = str('applied')
    else:
        print("{} is non of them".format(list_of_them[number]))
    return main_df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Plz enter AnimalCode NumberofBox AnimalStrain AnimalGender after the main.py with one space from each other")
    animal = int(sys.argv[1])
    box = int(sys.argv[2])
    strain = str(sys.argv[3])
    gender = str(sys.argv[4])
    print(animal, box, strain, gender)

    date_i = date(2020, 2, 12)
    date_f = date(2020, 11, 17)

    delta = date_f - date_i
    number_of_days = int(delta.days) + 1
    print("The experiment was {} days long".format(number_of_days))

    path_ = 'C:\\Users\\mehrd\\PycharmProjects\\drinkometer\\data\\2020\\dataframes'
    print(path_)

    df1 = pd.read_excel("{}\drinkometer_df_{}_{}_{}_{}_consumption.xlsx".format(path_, strain, gender, animal, box))
    df1_wl = pd.read_excel("{}\drinkometer_df_{}_{}_{}_{}_consumption.xlsx".format(path_, strain, gender, animal, box))

    threshold_low = 0.08
    threshold_up = threshup_()
    total_length_h = number_of_days * 24

    df_h = pd.DataFrame(index=range(number_of_days * 24), columns=['date', 'time', 'day_index', 'hour_index', 'animal',
                                                                   'box', 'strain', 'state', 'oxytocin', 'quinine',
                                                                   'water', 'alcohol_5', 'alcohol_10', 'alcohol_20',
                                                                   'locomotive'])
    df_h = m_day_and_hour_index(df_h, number_of_days)
    df_h = state_hour(df_h, number_of_days)

    df_h['animal'] = animal
    df_h['box'] = box
    df_h['strain'] = strain
    df_h['date'] = pd.date_range("2020-02-12", periods=number_of_days * 24, freq="H").strftime('%Y-%m-%d')
    df_h['time'] = pd.date_range("2020-02-12", periods=number_of_days * 24, freq="H").strftime('%H:%M:%S')

    hours = sorted(set(np.array(df1.loc[(df1['quinine'] == str('applied'))].hour_index)))
    for i in range(len(hours)):
        df_h.loc[hours[i] - 1, 'quinine'] = str('applied')

    hours = sorted(set(np.array(df1.loc[(df1['oxytocin'] == str('applied'))].hour_index)))
    for i in range(len(hours)):
        df_h.loc[hours[i] - 1, 'oxytocin'] = str('applied')

    for hour in range(1, number_of_days * 24 + 1):
        df_temp = weight_organizer()
        y_ = df_temp.loc[df_temp['gender'] == gender]["weight"]
        x_ = df_temp.loc[df_temp['gender'] == gender]["week"]
        w_w = wistar_w_w(gender, hour, x_, y_, 40, box)
        # print(w_w)
        list_ = []
        ind = np.array(df_h.loc[(df_h['hour_index'] == hour)].index)
        df_extracted = df1.loc[(df1['hour_index'] == hour) & (df1['water'].notnull())]
        temp_arr = np.array(df_extracted['water'])
        if len(temp_arr[temp_arr > threshold_low]) > 1:
            _temp = np.nansum(temp_arr[temp_arr > threshold_low])
            if _temp < threshold_up:
                df_h.loc[ind, 'water'] = _temp
                _temp = np.nan

        list_ = []
        ind = np.array(df_h.loc[(df_h['hour_index'] == hour)].index)
        df_extracted = df1.loc[(df1['hour_index'] == hour) & (df1['alcohol_5'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_5'])
        if len(temp_arr[temp_arr > threshold_low]) > 1:
            _temp = np.nansum(temp_arr[temp_arr > threshold_low])
            if _temp < threshold_up:
                temp__ = real_consump(_temp, w_w, 5)
                df_h.loc[ind, 'alcohol_5'] = temp__
                _temp = np.nan
                temp__ = np.nan

        list_ = []
        ind = np.array(df_h.loc[(df_h['hour_index'] == hour)].index)
        df_extracted = df1.loc[(df1['hour_index'] == hour) & (df1['alcohol_10'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_10'])
        if len(temp_arr[temp_arr > threshold_low]) > 1:
            _temp = np.nansum(temp_arr[temp_arr > threshold_low])
            if _temp < threshold_up:
                temp__ = real_consump(_temp, w_w, 10)
                df_h.loc[ind, 'alcohol_10'] = temp__
                _temp = np.nan

        list_ = []
        ind = np.array(df_h.loc[(df_h['hour_index'] == hour)].index)
        df_extracted = df1.loc[(df1['hour_index'] == hour) & (df1['alcohol_20'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_20'])
        if len(temp_arr[temp_arr > threshold_low]) > 1:
            _temp = np.nansum(temp_arr[temp_arr > threshold_low])
            if _temp < threshold_up:
                temp__ = real_consump(_temp, w_w, 20)
                df_h.loc[ind, 'alcohol_20'] = temp__
                _temp = np.nan

    number_of_days = 280
    for hour in range(1, number_of_days * 24 + 1):
        list_ = []
        ind = np.array(df_h.loc[(df_h['hour_index'] == hour)].index)
        df_extracted = df1_wl.loc[(df1_wl['hour_index'] == hour) & (df1_wl['locomotive'].notnull())]
        temp_arr = np.array(df_extracted['locomotive'])
        if len(temp_arr) > 1:
            df_h.loc[ind, 'locomotive'] = np.nansum(temp_arr)

    df_h.to_excel(r'{}\drinkometer_df_{}_{}_{}_{}_hourly.xlsx'.format(path_, strain, gender, animal, box),
                  index=False, header=True)

    df_d_light = pd.DataFrame(index=range(number_of_days), columns=['date', 'day_index', 'animal', 'box',
                                                                    'strain', 'state', 'oxytocin', 'quinine', 'water',
                                                                    'alcohol_5', 'alcohol_10', 'alcohol_20',
                                                                    'locomotive'])

    df_d_dark = pd.DataFrame(index=range(number_of_days), columns=['date', 'day_index', 'animal', 'box',
                                                                   'strain', 'state', 'oxytocin', 'quinine',
                                                                   'water', 'alcohol_5', 'alcohol_10', 'alcohol_20',
                                                                   'locomotive'])

    df_d_light = d_day_index(df_d_light, number_of_days)
    df_d_dark = d_day_index(df_d_dark, number_of_days)

    df_d_light['animal'] = animal
    df_d_light['box'] = box
    df_d_light['strain'] = strain
    df_d_light['state'] = str('light')
    df_d_light['date'] = pd.date_range("2020-02-12", periods=number_of_days, freq="D").strftime('%Y-%m-%d')

    df_d_dark['animal'] = animal
    df_d_dark['box'] = box
    df_d_dark['strain'] = strain
    df_d_dark['state'] = str('dark')
    df_d_dark['date'] = pd.date_range("2020-02-12", periods=number_of_days, freq="D").strftime('%Y-%m-%d')

    days = sorted(set(np.array(df1.loc[(df1['quinine'] == str('applied'))].day_index)))
    for i in range(len(days)):
        df_d_dark.loc[days[i] - 1, 'quinine'] = str('applied')
        df_d_light.loc[days[i] - 1, 'quinine'] = str('applied')

    days = sorted(set(np.array(df1.loc[(df1['oxytocin'] == str('applied'))].day_index)))
    for i in range(len(days)):
        df_d_dark.loc[days[i] - 1, 'oxytocin'] = str('applied')
        df_d_light.loc[days[i] - 1, 'oxytocin'] = str('applied')

    for day in range(1, number_of_days + 1):
        list_ = []
        ind = np.array(df_d_light.loc[(df_d_light['day_index'] == day)].index)
        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('light')) & (df_h['water'].notnull())]
        temp_arr = np.array(df_extracted['water'])
        if len(temp_arr) > 1:
            df_d_light.loc[ind, 'water'] = np.nansum(temp_arr)
        df_extracted = df_h.loc[(df_h['day_index'] == day) & (df_h['state'] == str('dark')) & (df_h['water'].notnull())]
        temp_arr = np.array(df_extracted['water'])
        if len(temp_arr) > 1:
            df_d_dark.loc[ind, 'water'] = np.nansum(temp_arr)

        list_ = []

        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('light')) & (df_h['alcohol_5'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_5'])
        if len(temp_arr) > 1:
            df_d_light.loc[ind, 'alcohol_5'] = np.nansum(temp_arr)
        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('dark')) & (df_h['alcohol_5'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_5'])
        if len(temp_arr) > 1:
            df_d_dark.loc[ind, 'alcohol_5'] = np.nansum(temp_arr)

        list_ = []

        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('light')) & (df_h['alcohol_10'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_10'])
        if len(temp_arr) > 1:
            df_d_light.loc[ind, 'alcohol_10'] = np.nansum(temp_arr)
        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('dark')) & (df_h['alcohol_10'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_10'])
        if len(temp_arr) > 1:
            df_d_dark.loc[ind, 'alcohol_10'] = np.nansum(temp_arr)

        list_ = []

        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('light')) & (df_h['alcohol_20'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_20'])
        if len(temp_arr) > 1:
            df_d_light.loc[ind, 'alcohol_20'] = np.nansum(temp_arr)
        df_extracted = df_h.loc[
            (df_h['day_index'] == day) & (df_h['state'] == str('dark')) & (df_h['alcohol_20'].notnull())]
        temp_arr = np.array(df_extracted['alcohol_20'])
        if len(temp_arr) > 1:
            df_d_dark.loc[ind, 'alcohol_20'] = np.nansum(temp_arr)

    for day in range(1, number_of_days + 1):
        list_ = []
        ind = np.array(df_d_light.loc[(df_d_light['day_index'] == day)].index)
        df_extracted = df1_wl.loc[
            (df1_wl['day_index'] == day) & (df1_wl['state'] == str('light')) & (df1_wl['locomotive'].notnull())]
        temp_arr = np.array(df_extracted['locomotive'])
        if len(temp_arr) > 1:
            df_d_light.loc[ind, 'locomotive'] = np.nansum(temp_arr)
        df_extracted = df1_wl.loc[
            (df1_wl['day_index'] == day) & (df1_wl['state'] == str('dark')) & (df1_wl['locomotive'].notnull())]
        temp_arr = np.array(df_extracted['locomotive'])
        if len(temp_arr) > 1:
            df_d_dark.loc[ind, 'locomotive'] = np.nansum(temp_arr)

    df_d_dark.to_excel(
        r'{}\drinkometer_df_{}_{}_{}_daily_dark.xlsx'.format(path_, strain, gender, animal, box),
        index=False, header=True)
    df_d_light.to_excel(
        r'{}\drinkometer_df_{}_{}_{}_daily_light.xlsx'.format(path_, strain, gender, animal, box),
        index=False, header=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

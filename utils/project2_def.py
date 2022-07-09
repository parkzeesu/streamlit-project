import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager
#import datetime as dt
import glob


def get_file_list(file_path):
    file_list = glob.glob(file_path+'*')
    hour_file_name = []
    minute_file_name = []
    for i in file_list:
        if 'TIM' in i:
            hour_file_name.append(i)
        elif 'MI' in i:
            minute_file_name.append(i)
    return hour_file_name, minute_file_name

# 파일 불러오기
def get_data(file_name, index_column=2, parse_date=[2]):
    datas = {}
    for fn in file_name:
        data = pd.read_csv(fn, index_col = index_column, parse_dates = parse_date,
                           encoding='cp949', skiprows=[0],
                           names=['site', 'name', 'date', 'temp'] )
        data.drop(['site','name'], axis=1, inplace=True)
        datas[fn] = data
    return (datas)

# 결측데이터 확인
def missing_check(data, freqs):
    start = data.index[0]
    end = data.index[-1]
    timestamp = pd.date_range(start, end, freq=freqs)
    data = data.reindex(timestamp)
    return (data)

# 물리한계검사 (최대 & 최저기온)
def physical_check(data):
    data[data['temp'] < -33] = np.nan
    data[data['temp'] > 40] = np.nan
    return (data)

# 단계검사 (1분 동안 3도 차이가 나면 결측)
def step_check(data):
    data['step'] = abs(data.sub(data.shift(1)))
    data[data['step'] > 3] = np.nan
    
    data.drop(data.tail(1).index, inplace=True)
    return (data)

# 지속성검사 (1시간 동안 0.1도 차이 안나면 결측)
def persistence_check(data): 
    if 'step' in data.columns:
        hour_data = data.resample('H').sum() # 분단위
    else:
        data['step'] = abs(data.sub(data.shift(1))) # 시간 단위
        hour_data = data.copy()
    
    hour = hour_data[hour_data['step'] < 0.1].index.strftime('%Y.%m.%d %H')
    
    if len(hour):
        for i in hour:
            data.loc[i,'temp'] = np.nan      
            
    data.dropna(inplace=True)
    return (data)

# 리샘플링
def data_resample(data, resample_type, num):
    
    data = data.resample(resample_type).agg({'temp': ['size', 'mean', 'max', 'min']})
    data = data.droplevel(level=0, axis = 1)
    data.loc[data['size'] < num, 'mean'] = np.nan
    data.loc[data['size'] < num, 'max'] = np.nan
    data.loc[data['size'] < num, 'min'] = np.nan
    return (data)

def data_resample2(data, resample_type, num):
    
    data = data.resample(resample_type).agg({'mean':['size', 'mean'], 'max':['max'], 'min':['min']})
    data = data.droplevel(level=0, axis = 1)
    data.loc[data['size'] < num, 'mean'] = np.nan
    data.loc[data['size'] < num, 'max'] = np.nan
    data.loc[data['size'] < num, 'min'] = np.nan
    return (data)


# 데이터 합치기
def data_concat(data_list):
    data = pd.concat(data_list)
    return data

# 그래프 그리기
def make_line_chart(data, index_time, x_label_name, title_name, save_file_name):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = BASE_DIR+"\\data\\NanumBarunGothic.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    matplotlib.rc('font',family=font_name)
 
    data.columns = ['sizes','means', 'maxs', 'mins']
    data = data.round(1)

    plt.figure(figsize=(11, 5))
    plt.plot(data.index.strftime(index_time), data.maxs, 'ro--', linewidth=0.8, label='max')
    plt.plot(data.index.strftime(index_time), data.means, 'yo--', linewidth=0.8, label='mean') 
    plt.plot(data.index.strftime(index_time), data.mins, 'bo--', linewidth=0.8, label='min')
    
    if x_label_name == 'Month':
        for i in range(len(data)):
            plt.text(data.index[i].strftime(index_time), data.means[i]+0.5, data.means[i], fontsize=9)
            plt.text(data.index[i].strftime(index_time), data.maxs[i]+0.5, data.maxs[i], fontsize=9)
            plt.text(data.index[i].strftime(index_time), data.mins[i]+0.5, data.mins[i], fontsize=9)
    else :
        for i in range(len(data)):
            if data.means[i]>32 or data.means[i]<24:
                plt.text(data.index[i].strftime(index_time), data.means[i]+0.3, data.means[i], fontsize=9)
        for i in range(len(data)):
            if data.maxs[i]>37.6:
                plt.text(data.index[i].strftime(index_time), data.maxs[i]+0.3, data.maxs[i], fontsize=9)
        for i in range(len(data)):
            if data.mins[i]<21.6:
                plt.text(data.index[i].strftime(index_time), data.mins[i]+0.3, data.mins[i], fontsize=9)
    
    plt.xlabel(x_label_name)
    plt.ylabel("Temperature")
    plt.legend()
    plt.title(title_name,fontsize=20)
    plt.grid(linestyle = ':')
    plt.savefig(BASE_DIR+'\\data\\'+save_file_name+'.png')
    

    
# 시간 데이터 qc
def hour_data_qc(hour_data):
    for key, value in hour_data.items():
        h_data_m = missing_check(value, 'H')
        h_data_p = physical_check(h_data_m)
        h_data = persistence_check(h_data_p)       
    return h_data, h_data_m, h_data_p

# 분 데이터 qc
def minute_data_qc(minute_data):
    m_data_list = []
    m_data_list_m = []
    m_data_list_p = []
    m_data_list_s = []
    
    for key, value in minute_data.items():
        m_data_m = missing_check(value, 'T')
        m_data_p = physical_check(m_data_m)
        m_data_s = step_check(m_data_p)
        m_data = persistence_check(m_data_s)
        
        m_data_list.append(m_data)
        m_data_list_m.append(m_data_m)
        m_data_list_p.append(m_data_p)
        m_data_list_s.append(m_data_s)
        
    m_data_all = data_concat(m_data_list)
    m_data_all_m = data_concat(m_data_list_m)
    m_data_all_p = data_concat(m_data_list_p)
    m_data_all_s = data_concat(m_data_list_s)
    return m_data_all, m_data_all_m, m_data_all_p, m_data_all_s


# qc과정 선택박스
def qc_checkbox(title, data, data_colum):
    checkbox_btn = st.checkbox(title, value=False)
    if checkbox_btn:    
        st.line_chart(data.loc[:,data_colum])
        st.dataframe(data.loc[:,data_colum], 300, 200)

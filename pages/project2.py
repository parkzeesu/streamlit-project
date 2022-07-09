import streamlit as st
from PIL import Image

# 다른 폴더에 있는 파일 import 하는 방법 
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import project2_def as p2d

def app():  
    
    st.title("서울시 기온 데이터 분석")
    
    st.write('''
             서울시 기온의 시간, 분자료를 이용하여 QC검사를 통해 오류를 처리하고,       
             해당 자료를 분석해 시각화 하고자 한다. 
             
             폭염과 한파가 심했던 2018년도를 분석해봤다.
             ''')

    st.markdown('---')              
    
    # 현재경로
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = BASE_DIR+'\\data\\seoul_temp\\'
    
    # 시간자료, 분자료 불러오기
    hour_file_list, minute_file_list = p2d.get_file_list(file_path)
    # 시간자료
    hour_data = p2d.get_data(hour_file_list)
    # 분자료
    minute_data = p2d.get_data(minute_file_list)


    # 서울 1년 기온
    st.subheader("2018년도 월별 기온")
    st.write("기준 : 2018.01 ~ 2018.12")
    
    h_data_b, h_data_m, h_data_p = p2d.hour_data_qc(hour_data)
    
    h_data_D = p2d.data_resample(h_data_b, 'D', 20)
    h_data = p2d.data_resample2(h_data_D, 'M', 24)
    
    p2d.make_line_chart(h_data, '%m', 'Month', '2018년 월별 기온', 'month_line_chart')
    image = Image.open('../project_jisu1/data/month_line_chart.png')
    st.image(image)
    h_data = h_data.round(1)
    st.dataframe(h_data.loc[:,['means', 'maxs', 'mins']], 500, 300)
 
    
    st.markdown('---') 
    
    
    # 서울 일주일 기온
    st.subheader("2018년도 8월 일별 기온")
    st.write("기준 : 2018.08.01 ~ 2018.08.31")
    
    m_data_all_b, m_data_all_m, m_data_all_p, m_data_all_s= p2d.minute_data_qc(minute_data)
    
    m_data_all_H = p2d.data_resample(m_data_all_b, 'H', 48)
    m_data_all = p2d.data_resample2(m_data_all_H, 'D', 20)
    
    p2d.make_line_chart(m_data_all, '%d', 'Day', '2018년도 8월 일별 기온', 'day_line_chart')
    
    image = Image.open('../project_jisu1/data/day_line_chart.png')
    st.image(image)
    
    m_data_all = m_data_all.round(1)
    st.dataframe(m_data_all.loc[:,['means', 'maxs', 'mins']], 500, 300)
    
    
    st.markdown('---') 
     
    st.subheader("2018년도 시간자료 QC검사 (그래프 & 표)")
    
    p2d.qc_checkbox('시계열 결측데이터 검사 (시간자료)', h_data_m, 'temp')
    p2d.qc_checkbox('물리한계 검사 (시간자료)', h_data_p, 'temp')
    p2d.qc_checkbox('지속성 검사 (시간자료)', h_data_b, 'temp')
    p2d.qc_checkbox('일별 데이터 평균 값 ', h_data_D, 'mean')
    
    
    st.markdown('---') 
    
    st.subheader("2018년도 8월 분자료 QC검사 (그래프 & 표)")
    
    p2d.qc_checkbox('시계열 결측데이터 검사 (분자료)', m_data_all_m, 'temp')
    p2d.qc_checkbox('물리한계 검사 (분자료)', m_data_all_p, 'temp')
    p2d.qc_checkbox('단계 검사 (분자료)', m_data_all_s, 'temp')
    p2d.qc_checkbox('지속성 검사 (분자료)', m_data_all_b, 'temp')
    p2d.qc_checkbox('시간 데이터 평균 값', m_data_all_H, 'mean')



    
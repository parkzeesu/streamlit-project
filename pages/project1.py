import streamlit as st
from PIL import Image
from streamlit_folium import folium_static  # 화면에 바로 보이게 하는 라이브러리

# 다른 폴더에 있는 파일 import 하는 방법 
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import project1_dri as p1d

def app():
    
    st.title("서울시 따릉이 대여소 지도")
    
    st.write('''
             서울시 공공자전거 따릉이 대여소의 위치 현황을 파악하고,     
             지역구별 따릉이 대여소 개수와 인구수를 비교하여 지역구 간의 대여소 비율을 비교해보고자 한다. 
             ''')
    
    st.markdown('---') 
    
    st.subheader('따릉이 대여소 현황 지도')
    
    
    # 경로 확인 
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 파일 불러오기
    data_xlsx = BASE_DIR+'\\data\\seoul_ddareungi_info.xlsx'
    data_json = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
    file_txt = BASE_DIR+'\\data\\seoul_population.txt'
    
    # 데이터 저장하기 
    dri_data, dri_gu_data, seoul_geo = p1d.dri_maps_func(data_xlsx, data_json)
    
    # 지도 만들기
    maps = p1d.dri_map(dri_data, dri_gu_data, seoul_geo)
    
    # 지도 화면에 보이게 하기 
    folium_static(maps)
    
    st.write('''
             1. 지도 type
                 - stamenterrain : 기본 타입 
                 - Viw in Light Mode : 밝음 모드
                 - View in Dark Mode : 어둠 모드
             2. 따릉이 대여소
                 - 서울시 따릉이 대여소 현황 : 따릉이 대여소의 위치 현황을 알려준다.
                 - 지역구 별 따릉이 대여소 현황 : 지역구 별 따릉이 대여소 개수를 컬러맵을 통해 시각적으로 알려준다.
             ''')
    
    
    st.table(dri_gu_data)
    
    st.markdown('''           
             ```plaintext
             대여소의 개수가 많은 지역구는 송파구, 강서구, 강남구, 영등포구이고, 
             대여소의 개수가 적은 지역구는 강북구, 도봉구, 동작구이다. 

             ```
             ''')

    st.markdown('---') 
 
    st.subheader('따릉이 대여소 그래프')
    
    # 지역구별 인구수 데이터 불러오기
    pop_data = p1d.getData_txt(file_txt)
    
    # 지역구별 대여소, 인구수 데이터 합치기
    total_data = p1d.df_merge(dri_gu_data, pop_data)
    data_sort = p1d.LR_data(total_data)
    
    # 그래프 -> 이미지 저장
    p1d.seoul_d_p_graph(data_sort)
    
    # 저장된 그래프 이미지 보여주기 
    image = Image.open('../project_jisu1/data/seoul_dri_pop_graph.png')
    st.image(image)
    
    # 데이터 테이블로 보여주기
    st.dataframe(data_sort, 600, 300)
    st.markdown('''           
             ```plaintext
             인구수 대비 대여소의 개수가 많은 지역구는 송파구, 종로구, 강서구, 영등포구이고, 
             인구수 대비 대여소의 개수가 적은 지역구는 관악구, 성북구, 동작구이다. 

             ```
             ''')

    
    st.markdown('---') 
    
    st.subheader('결론')
    
    dri1 = Image.open('../project_jisu1/data/dri1.png')
    
    st.image(dri1)
    st.markdown('''           
             ```plaintext
             지역구별 대여소 개수와 인구수 대비 대여소 개수를 비교해 봤다. 
             
             대여소 개수가 많은 지역의 교집합 지역은 송파구, 강서구, 영등포구로,
             지역구민과 유동인구가 많으며, 한강 주변에 있는 지역구라는 사실을 알 수 있었다.
             
             대여소 개수가 적은 지역의 교집합 지역은 동작구이며,
             동작구에 대여소를 추가로 배치해야할 필요가 있다고 생각했다. 
             ```
             ''')


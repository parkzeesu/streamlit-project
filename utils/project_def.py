import streamlit as st
from PIL import Image

def app():
    st.title("PROJECT")
    
    st.write("2022.05.27 ~ 2022.06.27")
    
    st.subheader('서울시 공공자전거 따릉이 대여소 지도')
    
    st.markdown('''               
             - ###### 목적              
             서울시 공공자전거 따릉이 대여소의 위치 현황을 파악하고,     
             지역구별 따릉이 대여소 개수와 인구수를 비교하여 지역구 간의 대여소 비율을 비교해보고자 한다. 
             
             
             
             - ###### Data 
             
             1. 따릉이 대여소 정보.xlsx             
             ```plaintext
             대여소명, 자치구, 위도, 경도
             ```

             2. 서울시 행정구역.json 
             ```plaintext
             지역구(국문), 지역구 형태를 그릴 수 있는 좌표
             ```
             
             3. 서울시 지역구 인구 수.txt
             ```plaintext
             자치구, 인구(합계)
             ```
             
             
             
             - ###### 출처
             ```plaintext
             - 서울 열린데이터 광장 / 서울시 공공자전거 대여소 정보 (21.12월 기준)
             - url 형식 - https://raw.githubusercontent.com/...(2013년 기준)
             - 서울 열린데이터 광장 / 서울시 주민등록인구 (구별) 통계 (22.04월 기준)
             ```
             
             ''')
             
             
    st.markdown('---')         
    
    
    st.subheader('서울시 기온 데이터 분석')
    

    st.markdown('''
             - ###### 목적             
             서울시 기온의 시간, 분자료를 이용하여 QC검사를 통해 오류를 처리하고,       
             해당 자료를 분석해 시각화 하고자 한다. 
             
             폭염과 한파가 심했던 2018년도를 살펴보고자 했다. 



             - ###### Data 
             
             1. 서울시 2018년도 기온 데이터.csv (시간자료) 
             ```plaintext
             날짜, 기온
             ```

             2. 서울시 1일 기온 데이터.csv (분자료) 18년도 8월 (총 31일) 
             ```plaintext
             날짜, 기온
             ```
            
            
             - ###### 출처
             ```plaintext
             기상자료개방포털 / 서울 기온 시간 & 분 자료
             ```
             
             
             - ###### QC검사               
             조건 | 내용
             --|--
             결측 | 시간 데이터 중 없는 데이터 생성
             물리한계 | -33℃ 미만, 40℃ 초과된 기온 결측처리
             단계 | 1분 동안 3℃초과된 기온 결측처리
             지속성 | 1시간 동안 0.1℃미만인 기온 결측처리 
                 
             ''')

    st.markdown('---') 
    
    st.subheader('Dataflow')

    image = Image.open('../project_jisu1/data/img.png')
    st.image(image)
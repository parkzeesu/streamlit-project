import pandas as pd
import numpy as np
import folium
import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager
from branca.colormap import linear
from folium.plugins import MarkerCluster  # 좁은 지역에 있는 방대한 자료 모아서 보여주는 라이브러리
from sklearn.linear_model import LinearRegression


# 서울시 따릉이 대여소 현황 파일 불러오기
def getData(data_xlsx):
    datas = pd.read_excel(data_xlsx,'대여소현황', skiprows=[0,1,2,3], usecols = [0,1,2,3,4,5,9], 
                          names=['lendplace_id','lendplace_name','area','address','lat','long','type'])
    return datas

# 서울시 따릉이 지역구 별 개수 현황 
def getData2(datas):
    datas2 = datas.area.value_counts().rename_axis('gu').reset_index(name='dri_total')
    return datas2

# 서울 행정구역 json raw파일(githubcontent)
def getData_json(data_json):
    r = requests.get(data_json)
    c = r.content
    seoul_geo = json.loads(c)
    return seoul_geo

# 따릉이 지도 만들기
def dri_map(datas, datas2, seoul_geo):
    # 맵
    maps = folium.Map(location = [37.5602, 126.982], zoom_start = 11, tiles = 'Stamen Terrain')
    
    # 그룹화 (name > 컨트롤러에 표시되는 텍스트, overlay > 지도 위에 덮어씌울지 유/무, False 하면 뒤에 지도가 안뜬다)
    fg1 = folium.FeatureGroup(name='서울시 따릉이 대여소 현황',overlay=True).add_to(maps)
    fg2 = folium.FeatureGroup(name='지역구 별 따릉이 대여소 현황',overlay=True).add_to(maps)
    
    # fg1 / 서울시 따릉이 대여소 현황
    marker_cluster = MarkerCluster().add_to(fg1)
    for i in range(len(datas)):
        latitude = datas.loc[i,'lat']
        longitude = datas.loc[i,'long']
        name = datas.loc[i,'lendplace_name']
        folium.Marker([latitude, longitude], popup = name, icon=folium.Icon(color='green',icon='star')).add_to(marker_cluster)
    
    
    # fg2 / 지역구 별 따릉이 대여소 현황
    New_cases = folium.Choropleth(
                seoul_geo,
                data = datas2,
                columns=['gu', 'dri_total'],
                key_on='properties.name', 
                fill_color='YlGn', # 컬러맵과 색을 맞춰줘야함 
                nan_fill_color="White", # 지역은 있는데 사용할 데이터가 없는 경우 흰색으로 나온다.
                fill_opacity=0.7,
                line_opacity=0.2,
                #highlight=True,
                #overlay=False,
                #line_color='black'
                ).geojson.add_to(fg2)
    
    # 지역 마우스 오버 했을 때 지역구 명 tooltip
    folium.GeoJson(
        data = seoul_geo, 
        name = '지역구', 
        smooth_factor = 2, # 지역구 테두리 곡선의 강도(숫자가 낮을수록 더 곡선형)
        style_function = lambda x: {
            'color':'grey',
            'fillColor':'transparent',
            'weight':0.3},
        tooltip = folium.GeoJsonTooltip(
            fields = ['name'], 
            labels=False, # tooltip에 name항목 표시
            sticky=True), # tooltip이 마우스를 따라다니게 하는 것
        # 지역구가 선택되었을 때 해당 지역의 변화되는 style
        highlight_function = lambda x: {'weight':2},
        ).add_to(New_cases)
    
    # 오른쪽 상단, 컬러맵
    colormap = linear.YlGn_09.scale(datas2['dri_total'].min(), datas2['dri_total'].max(), 6)
    colormap.caption = '지역구 별 따릉이 대여소 현황'
    colormap.add_to(maps)
    
    # 지도 타입
    folium.TileLayer('cartodbpositron',overlay=False,name="Viw in Light Mode").add_to(maps)
    folium.TileLayer('cartodbdark_matter',overlay=False,name="View in Dark Mode").add_to(maps)
    folium.LayerControl(collapsed = False, position = 'bottomright').add_to(maps)
    
    return maps

# 따릉이 지도 데이터 불러오는 함수를 합친 거  
def dri_maps_func(data_xlsx, data_json):
    datas = getData(data_xlsx)
    datas2 = getData2(datas)
    seoul_geo = getData_json(data_json)
    return datas, datas2, seoul_geo


# 서울시 지역구별 인구 현황 파일 불러오기
def getData_txt(file_txt):
    data = pd.read_table(file_txt, skiprows=[0,1,2,3],
                         names=['gu','gen', 'total', 'man','woman', 'k_total', 'k_man', 
                                'k_woman','f_total', 'f_man', 'f_woman', 'per_gen', '65_up'],
                         thousands = ',')
    data = data.reset_index(drop=True)
    data = data.loc[:, ['gu', 'total']]
    return data
    
# 데이터 프레임 합치기
def df_merge(dri_data, pop_data):
    data = pd.merge(dri_data, pop_data, on='gu')
    return data


# 통계 선형 회귀식 
def LR_data(data):
    x = data.total.values[:, np.newaxis]
    y = data.dri_total
    model = LinearRegression()
    model.fit(x,y)
    model.coef_
    model.intercept_
    data['predict_lr'] = model.predict(x)
    data['res']=data.dri_total-data.predict_lr
    data_sort = data.sort_values(by='res', ascending=False)
    data_sort = data_sort.reset_index(drop=True)
    return data_sort

# 그래프 
def seoul_d_p_graph(data_sort):   
 
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #폰트 경로
    font_path = BASE_DIR+"\\data\\NanumBarunGothic.ttf"
    #폰트 이름 얻어오기
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    #font 설정
    matplotlib.rc('font',family=font_name)
    
    
    plt.figure(figsize=(9,6))
    plt.scatter(data_sort.total, data_sort.dri_total, c=data_sort.res, s=30)
    for n in range(25):
        if n <= 3:
            plt.text(data_sort.loc[n, 'total']-15000, data_sort.loc[n, 'dri_total']+3,
                     data_sort.loc[n, 'gu'], fontsize=9)
        elif n >= 22:
            plt.text(data_sort.loc[n, 'total']-15000, data_sort.loc[n, 'dri_total']-6,
                     data_sort.loc[n, 'gu'], fontsize=9)
        else:
            plt.text(data_sort.loc[n, 'total']+9000, data_sort.loc[n, 'dri_total']-1,
                     data_sort.loc[n, 'gu'], fontsize=8, color='gray')

    
    plt.plot(data_sort.total, data_sort.predict_lr, lw=1, color='r')
    plt.xlabel('인구수')
    plt.ylabel('따릉이 대여소 개수')
    plt.title('따릉이 대여소', fontsize=20)
    plt.colorbar()
    plt.grid(linestyle = ':') 
    plt.savefig(BASE_DIR+'\\data\\seoul_dri_pop_graph.png')
    
    
    
    
    
    
    
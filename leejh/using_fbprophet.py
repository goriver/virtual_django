import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from fbprophet import Prophet
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

class PredictByProphet :
    def make_train_data(index_code, want_date):
        
        # index_code = '000100'  # 종목코드 넣어줌
        # want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

        input_date = want_date-7

        wd = str(want_date)

        day = wd[6:8]

        int_day = int(day)

        frames = []

        for i in range(7):
            url='https://finance.naver.com/item/sise_time.nhn?code='+ index_code +'&thistime='+ str(input_date) + '16'
            
            resp = requests.get(url)
            html = BeautifulSoup(resp.content, 'html.parser')
            
            holiday = html.find("td",{"class":"pgRR"})
            
            if holiday is None:  #주말은 제외
                
                input_date+=1
                continue
                
            else:
                
                last_page = html.find("td",{"class":"pgRR"}).find('a')['href'].split('&')[2].split('=')[1]
                lastpage = int(last_page)
                df=pd.DataFrame()
                
                for page in range(1, lastpage+1):
                    pg_url = '{url}&page={page}'.format(url=url, page=page)
                    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
                    
                rdf = df.dropna(axis=0)
                
                rdf['date'] = input_date
                
                rdf['date'] = rdf['date'].astype(str)
                rdf["date"] = rdf["date"].str[0:4] + "-" + rdf["date"].str[4:6] + "-" + rdf["date"].str[6:8]
                rdf["date"] = rdf["date"].astype('datetime64[ns]')

                rdf['DateTime'] = pd.to_datetime(rdf.date.dt.strftime("%Y-%m-%d") + " " + rdf.체결시각)

                frames.append(rdf)
                input_date+=1

        frames.reverse()

        final_frame = pd.concat(frames, ignore_index=True)

        data = final_frame[::-1].reset_index(drop=True)

        return data, int_day


    def make_test_data(index_code, want_date):
        
        # index_code = '000100'  # 종목코드 넣어줌
        # want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

        input_date = want_date

        wd = str(want_date)

        day = wd[6:8]

        int_day = int(day)

        frames = []

        for i in range(1):
            url='https://finance.naver.com/item/sise_time.nhn?code='+ index_code +'&thistime='+ str(input_date) + '16'
            
            resp = requests.get(url)
            html = BeautifulSoup(resp.content, 'html.parser')
            
            holiday = html.find("td",{"class":"pgRR"})
            
            if holiday is None:  #주말은 제외
                
                input_date+=1
                continue
                
            else:
                
                last_page = html.find("td",{"class":"pgRR"}).find('a')['href'].split('&')[2].split('=')[1]
                lastpage = int(last_page)
                df=pd.DataFrame()
                
                for page in range(1, lastpage+1):
                    pg_url = '{url}&page={page}'.format(url=url, page=page)
                    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
                    
                rdf = df.dropna(axis=0)
                
                rdf['date'] = input_date
                
                rdf['date'] = rdf['date'].astype(str)
                rdf["date"] = rdf["date"].str[0:4] + "-" + rdf["date"].str[4:6] + "-" + rdf["date"].str[6:8]
                rdf["date"] = rdf["date"].astype('datetime64[ns]')

                rdf['DateTime'] = pd.to_datetime(rdf.date.dt.strftime("%Y-%m-%d") + " " + rdf.체결시각)

                frames.append(rdf)
                input_date+=1

        frames.reverse()

        final_frame = pd.concat(frames, ignore_index=True)

        data = final_frame[::-1].reset_index(drop=True)

        return data, int_day

    def main(code, date):
        # pass
        temp, what_day = make_train_data(code, date)

        df = pd.DataFrame(columns=['ds', 'y'])

        df['ds'] = temp['DateTime']  # 훈련용 데이터프레임 생성

        df['y'] = temp['체결가']  # 앞으로 쓸 y값 지정

        df['y'].plot()
        plt.savefig('weekend.png', dpi=400)


        m = Prophet(changepoint_range=0.1).fit(df)
        future = m.make_future_dataframe(periods=1500, freq='min')

        future2 = future[(future['ds'].dt.day == what_day)]

        am = future2[ (future2['ds'].dt.hour >= 9) & (future2['ds'].dt.hour < 12) ]
        pm = future2[ (future2['ds'].dt.hour >= 12) & (future2['ds'].dt.hour < 16) ]


        am_pred = m.predict(am)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=am_pred['ds'],y=am_pred['yhat'],
                    mode='lines+markers', name='실제값'))
        fig.update_layout(title='<b>해당 요일 오전의 예측 주가</b>')
        pio.write_html(fig, "C:/Users/A0501660/djangogirls/djangogirls/django/templates/blog/leejh/AM_{}.html".format(index_code), config=None, auto_play=True, include_plotlyjs=True, include_mathjax=False, post_script=None, full_html=True, animation_opts=None, validate=True, default_width='100%', default_height='100%', auto_open=False)



        pm_pred = m.predict(pm)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pm_pred['ds'],y=pm_pred['yhat'],
                    mode='lines+markers', name='실제값'))
        fig.update_layout(title='<b>해당 요일 오후의 예측 주가</b>')
        pio.write_html(fig, "C:/Users/A0501660/djangogirls/djangogirls/django/templates/blog/leejh/PM_{}.html".format(index_code), config=None, auto_play=True, include_plotlyjs=True, include_mathjax=False, post_script=None, full_html=True, animation_opts=None, validate=True, default_width='100%', default_height='100%', auto_open=False)



        print("해당 종목의 오전 추천 매수가는 ", am_pred['yhat'].min(), "입니다.")
        print("해당 종목의 오전 추천 매도가는 ", am_pred['yhat'].max(), "입니다.")

        print("해당 종목의 오후 추천 매수가는 ", pm_pred['yhat'].min(), "입니다.")
        print("해당 종목의 오후 추천 매도가는 ", pm_pred['yhat'].max(), "입니다.")




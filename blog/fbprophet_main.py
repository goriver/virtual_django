import blog.using_fbprophet 
from fbprophet import Prophet
import datetime
import pandas as pd
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# 매일 저녁에 서버 다운 or 점검 시간에 수행


# index_code = '000100'  # 종목코드 넣어줌
# want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

# K,LG,KT
# 카카오,삼성,네이버 로 fix
def get_json():
    corporation = ['034730', '003550','030200','035720','005930','035420']
    # fbpro = PredictByProphet.main()
    today = datetime.datetime.today() 
    date = today.strftime('%Y%m%d') 
    date = int(date)
    pd.set_option('mode.chained_assignment',  None)

    chart_am = []
    chart_pm = []
    # using_fbprophet.
    for index_code in corporation:
        temp, what_day = using_fbprophet.make_train_data(index_code, date)

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

        am_data = fig.to_json()
        pm_data = fig.to_json()
        
        pm_pred = m.predict(pm)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pm_pred['ds'],y=pm_pred['yhat'],
                    mode='lines+markers', name='실제값'))
        fig.update_layout(title='<b>해당 요일 오후의 예측 주가</b>')


        chart_am.append({index_code : am_data})
        chart_pm.append({index_code : pm_data})

        # pio.write_html(fig, "./templates/blog/leejh/Path_PM_{}.html".format(index_code))
        # pio.write_html(fig, "./templates/blog/leejh/Path_PM_{}.html".format(index_code))

        # templates=""" {% extends 'blog/index.html' %} 
        # {% block content %}
        # <div class="container"> 
        #     <div id = 'divPlotly'></div>
        #     <script>
        #         var plotly_data={}
        #         Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
        #     </script>
        # </div>
        # {% endblock %}
        # """
        # print(templates)
        # # C:\Users\ka030\hello_django\env\Scripts\virtual_django\templates\blog\leejh\Path_AM_005930.html
        # with open("./templates/blog/leejh/Path_AM_{}.html".format(index_code), 'w') as f:
        #     f.write(templates.format(am_data))

        # with open("./templates/blog/leejh/Path_PM_{}.html".format(index_code), 'w') as f:
        #     f.write(templates.format(pm_data))


        print("해당 종목의 오전 추천 매수가는 ", am_pred['yhat'].min(), "입니다.")
        print("해당 종목의 오전 추천 매도가는 ", am_pred['yhat'].max(), "입니다.")

        print("해당 종목의 오후 추천 매수가는 ", pm_pred['yhat'].min(), "입니다.")
        print("해당 종목의 오후 추천 매도가는 ", pm_pred['yhat'].max(), "입니다.")
    return chart_am, chart_pm







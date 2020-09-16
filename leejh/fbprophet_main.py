import using_fbprophet 
import datetime
import pandas as pd
# 매일 저녁에 서버 다운 or 점검 시간에 수행


# index_code = '000100'  # 종목코드 넣어줌
# want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

# K,LG,KT
# 카카오,삼성,네이버 로 fix
if __name__ == "__main__":
    corporation = ['034730', '003550','030200','035720','005930','035420']
    # fbpro = PredictByProphet.main()
    today = datetime.datetime.today() 
    date = today.strftime('%Y%m%d') 
    date = int(date)
    pd.set_option('mode.chained_assignment',  None)
    # using_fbprophet.
    for i in corporation:
        temp, what_day = using_fbprophet.make_train_data(i, date)

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







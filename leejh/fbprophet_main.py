from using_fbprophet import PredictByProphet
import datetime
# 매일 저녁에 서버 다운 or 점검 시간에 수행


# index_code = '000100'  # 종목코드 넣어줌
# want_date = 20200915   # 예측하고 싶은 요일을 넣어줌

# K,LG,KT
# 카카오,삼성,네이버 로 fix
if __name__ == "__main__":
    corporation = ['034730', '003550','030200','035720','005930','035420']
    fbpro = PredictByProphet.main()
    today = datetime.datetime.today() 
    date = today.strftime('%Y%m%d') 
    for i in corporation:
        fbpro(i, date)


#-*- coding:utf-8 -*-
import datetime,setting,jsm
from pandas import Series ,DataFrame
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from models import dbcontrol
import math



class StockGetTop(object):
    def __init__(self, stocknum = None):
        self.stocknum = stocknum
        self.Y = datetime.datetime.today().year
        self.M = datetime.datetime.today().month
        self.D = datetime.datetime.today().day

class StockGet(StockGetTop):
    def __init__(self, stocknum = None):
        super().__init__(stocknum)
        get_stock_f = setting.GET_STOCK_F
        if get_stock_f == 0:
            self.stockgetdayjsm(datetime.date(self.Y-1, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)
            self.stockgetweekjsm(datetime.date(self.Y-2, self.M, self.D),datetime.date(self.Y, self.M, self.D), self.stocknum)
        elif get_stock_f == 1:
            #print(setting.HOME_PATH + str(self.stocknum) + ".csv")
            self.db_s = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".csv", index_col=0, parse_dates=True , names=["Stock"])
            #print(self.db_s)
            self.db_sw = pd.read_csv(setting.HOME_PATH + str(self.stocknum) + ".week.csv", index_col=0, parse_dates=True,
                            names=["Stock"])

    def stockgetdayjsm(self, start_date, end_date, stock_num):
        q = jsm.Quotes()
        stock = q.get_historical_prices(stock_num, jsm.DAILY, start_date, end_date)  # 指定期間、指定銘柄の株価取得
        close_stock = [data.close for data in stock]  # 終値の取得
        date_stock = [data.date for data in stock]  # 日付の取得
        db_s = Series(close_stock, date_stock)  # 日付と終値をドッキング
        self.db_s = db_s.sort_index(ascending=True)  # 古い順に並び替える。
        self.db_s.to_csv(setting.HOME_PATH + str(stock_num) + ".csv")
        self.db_s = DataFrame(self.db_s, columns=['Stock'])  #列名'Stock'を付与する。
        return self.db_s


    def stockgetweekjsm(self,start_date,end_date,stock_num):
        q = jsm.Quotes()
        stock = q.get_historical_prices(stock_num, jsm.WEEKLY, start_date, end_date)   #指定期間、指定銘柄の株価取得
        close_stock = [data.close for data in stock]   #終値の取得
        date_stock = [data.date for data in stock]      #日付の取得
        db_sw = Series(close_stock, date_stock)   #日付と終値をドッキング
        self.db_sw = db_sw.sort_index(ascending=True) #古い順に並び替える。
        self.db_sw.to_csv(setting.HOME_PATH + str(stock_num) +".week.csv")
        self.db_sw = DataFrame(self.db_sw, columns=['Stock'])  #列名'Stock'を付与する。
        return self.db_sw


class Technical(StockGet):
    def __init__(self,stocknum):
        #print("analyze0")
        super().__init__(stocknum)
        #print("analyze1")
        self.vol_get(self.db_s) #Volatirity calculation
        self.getsymbol(self.db_s) #日足情報
        self.week_getsymbol(self.db_sw) #週足情報        
        #print("analyze2")
        self.macd(self.db_s)
        self.smaget(self.db_s)
        #print("analyze3")
        self.getbps()
        #print("analyze4")
        self.getper(self.db_s)
        self.smacross(self.db_s)
        self.bolinger(self.db_s)
        self.smaweekget(self.db_sw)
        self.kairi(self.db_s)       
        self.combine()
        #print("self.db_sw")
        #print(self.db_sw)

    def vol_get(self, mat): #銘柄のVolatirityを取得する
        self.stock_vol = 100 * mat.pct_change()
        self.stock_vol = self.stock_vol.dropna()
        self.volatirity = np.std(self.stock_vol) #過去1年の株価のボラティリティーの標準偏差計算
        self.mean_vol = np.mean(self.stock_vol) #過去1年の株価のボラティリティーの平均計算抽出
        self.stockvolmat = DataFrame(self.stock_vol, columns=['Stock', '+sigma', '-sigma', '+2sigma', '-2sigma', '+3sigma', '-3sigma'])
        #print("stockvolmat")
        #print(len(stockvolmat))
        self.stockvolmat['+sigma'] = np.full(len(self.stockvolmat), self.mean_vol + self.volatirity)
        self.stockvolmat['+2sigma'] = np.full(len(self.stockvolmat), self.mean_vol+2*self.volatirity)
        self.stockvolmat['+3sigma'] = np.full(len(self.stockvolmat), self.mean_vol+3*self.volatirity)
        self.stockvolmat['-sigma'] = np.full(len(self.stockvolmat), self.mean_vol - self.volatirity)
        self.stockvolmat['-2sigma'] = np.full(len(self.stockvolmat), self.mean_vol - 2*self.volatirity)
        self.stockvolmat['-3sigma'] = np.full(len(self.stockvolmat), self.mean_vol - 3*self.volatirity)
        #self.vol = [self.stock_vol, self.volatirity]
        #print(stockvolmat)
        #return stockvolmat



    def macd(self, mat): #MACDデータを取得する
        self.s_dur = setting.S_DUR  #MACD parameter
        self.l_dur = setting.L_DUR  #MACD parameter
        self.sig_dur = setting.SIG_DUR #MACD parameter
        mat = DataFrame(mat.dropna())
        self.dmatmacd = DataFrame(mat, columns=['Stock', 'LONG', 'SHORT', 'V_MACD', 'V_SIG', 'DIF_MACD', 'ZERO'])
        self.dmatmacd['ZERO'] = np.full(self.dmatmacd.shape[0], 0)
        self.dmatmacd['LONG'] = self.dmatmacd['Stock'].ewm(span=self.l_dur).mean()
        self.dmatmacd['SHORT'] = self.dmatmacd['Stock'].ewm(span=self.s_dur).mean()
        self.dmatmacd['V_MACD'] = self.dmatmacd['SHORT'] - self.dmatmacd['LONG']
        self.dmatmacd['V_SIG'] = self.dmatmacd['V_MACD'].rolling(window=self.sig_dur, center=False).mean()
        self.dmatmacd['DIF_MACD'] = self.dmatmacd['V_MACD'] - self.dmatmacd['V_SIG']

        #return self.dmatmacd
        #dmat['LONG'] = pd.ewma(dmat['Stock'], span=self.l_dur)
        #dmat['SHORT'] = pd.ewma(dmat['Stock'], span=self.s_dur)
        #dmat['V_MACD'] = dmat['SHORT'] - dmat['LONG']
        #dmat['V_SIG'] = pd.rolling_mean(MA['V_MACD'], self.sig_dur)
        #dmat['DIF_MACD'] = dmat['V_MACD'] - dmat['V_SIG']



    def smaget(self, mat): #SMAデータを取得する。
        self.s_idou=setting.S_IDOU
        self.m_idou=setting.M_IDOU
        self.l_idou=setting.L_IDOU
        mat = DataFrame(mat.dropna())
        self.dmatsma = DataFrame(mat, columns=['Stock', 'MA_S', 'MA_M', 'MA_L'])
        self.dmatsma['MA_S'] = self.dmatsma['Stock'].rolling(window=self.s_idou, center=False).mean()
        self.dmatsma['MA_M'] = self.dmatsma['Stock'].rolling(window=self.m_idou, center=False).mean()
        self.dmatsma['MA_L'] = self.dmatsma['Stock'].rolling(window=self.l_idou, center=False).mean()
        self.dmat_2month = self.dmatsma['Stock'][datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=60):
                          datetime.datetime(self.Y, self.M, self.D)]
        self.stockmax = np.nanmax(self.dmat_2month) * 1.02
        self.stockmin = np.nanmin(self.dmat_2month) * 0.98

        #MA['MA_M'] = pd.rolling_mean(MA['Stock'], m_idou)
        #MA['MA_L'] = pd.rolling_mean(MA['Stock'], l_idou)
        self.stock_p1sig = round(self.stock_now*(math.e**(self.volatirity/100)), 0)
        self.stock_p05sig = round(self.stock_now*(math.e**(0.5*self.volatirity/100)), 0)
        self.stock_n1sig = round(self.stock_now*(math.e**(-self.volatirity/100)), 0)
        self.stock_n05sig = round(self.stock_now*(math.e**(-0.5*self.volatirity/100)), 0)
        #print("self.dmatsma['MA_S']")
        #print(self.dmatsma['MA_S'])
        self.smatoday = self.dmatsma['MA_S'].tail(1)[0]
        #print("self.smatoday")
        #print(self.smatoday)

        #self.stockinfo = [stock_p1sig["Stock"][0], stock_p05sig["Stock"][0], stock_n1sig["Stock"][0], stock_n05sig["Stock"][0]]
        #print("self.stockinfo")
        #print(self.stockinfo)
        return self.dmatsma, self.stockmax, self.stockmin


    def getsymbol(self, mat):
        mat = DataFrame(mat.dropna())
        self.dmatstock = DataFrame(mat, columns=['Stock'])
        self.stock_old = self.dmatstock.head(1)  # 1年前の株価を取得
        self.stock_now = self.dmatstock.tail(1)  # 本日の株価を取得する
        self.stock_exp =100* math.log(self.stock_now['Stock'][0]/self.stock_old['Stock'][0] , math.e)   #1年前の株価と本日の株価の変化率を計算
        self.stock_kinou = self.dmatstock[len(self.dmatstock)-2:len(self.dmatstock)-1]['Stock'][0] #昨日の株価を取得する
        self.stock_ototoi = self.dmatstock[len(self.dmatstock)-3:len(self.dmatstock)-2]['Stock'][0] # おとといの株価を取得する
        self.dif_kinou_ototoi = self.stock_kinou - self.stock_ototoi  # 昨日の株価 - おとといの株価
        self.dif_today_kinou = self.stock_now - self.stock_kinou  # 今日の株価 - 昨日の株価

        #print("self.stock_kinou")
        #print(self.stock_kinou)
        #print("self.stock_ototoi")
        #print(self.stock_ototoi)

        #self.volatirity=np.std(self.stock_vol) #過去1年の株価のボラティリティーの標準偏差計算
        #self.mean_vol=np.mean(self.stock_vol) #過去1年の株価のボラティリティーの平均計算抽出
        #print(self.volatirity)
        #print(self.mean)

    def week_getsymbol(self, mat):
        mat = DataFrame(mat.dropna())
        #print("week")
        #print(mat)

        self.dmatstock = DataFrame(mat, columns=['Stock'])
        self.stock_1weekmae = self.dmatstock[len(self.dmatstock)-2:len(self.dmatstock)-1]['Stock'][0] #週足(1週間前)の株価を取得する
        self.stock_2weekmae = self.dmatstock[len(self.dmatstock)-3:len(self.dmatstock)-2]['Stock'][0] #週足(2週間前)の株価を取得する
        self.stock_3weekmae = self.dmatstock[len(self.dmatstock)-4:len(self.dmatstock)-3]['Stock'][0] #週足(3週間前)の株価を取得する       
        self.dif_3_2_week = self.stock_2weekmae - self.stock_3weekmae  #週足(3週間前) -  週足(2週間前) を取得する
        self.dif_2_1_week = self.stock_1weekmae - self.stock_2weekmae  #週足(3週間前) -  週足(2週間前)　を取得する
        #print("self.dif_3_2_week")
        #print(self.dif_3_2_week)
        #print("self.dif_2_1_week")
        #print(self.dif_2_1_week )






    def getbps(self): #指定銘柄のBPS(一株当たりの利益)
        #print("self.bps")      
        self.record_stockdb = pd.read_csv(setting.CSV_DB_PATH, names=setting.CSV_DB_PATH_COLUMNS) #全登録銘柄の情報を読み込み
        #self.record_stockdb = pd.read_csv("/home/pi/Desktop/stock/sqltest.csv", names=setting.CSV_DB_PATH_COLUMNS) #全登録銘柄の情報を読み込み
        #print("record_stockdb")
        #print(self.record_stockdb)
        #print("record_stockdb end")
        self.getinfo_of_stock = DataFrame(self.record_stockdb.ix[self.record_stockdb['STOCK_NUM'] == int(self.stocknum)]) #対象銘柄1行を抽出
        #print("getinfo_of_stock")
        #print(self.getinfo_of_stock)
        #print("getinfo_of_stock end")
        self.getinfo_of_stock = self.getinfo_of_stock.set_index('STOCK_NUM')  # STOCK_NUM列をindexに指定した
        #print("1")
        self.stockinfo = DataFrame(self.getinfo_of_stock['LASTYEAR_PROFIT_PER_STOCK'])  # 'LASTYEAR_PROFIT_PER_STOCK'列のみを抽出
        print("self.stockinfo")
        print(self.stockinfo)
        self.bps = self.stockinfo['LASTYEAR_PROFIT_PER_STOCK'][int(self.stocknum)]  # インデックス stockget_numの'LASTYEAR_PROFIT_PER_STOCK'列を取り出す
        #print("self.bps")
        #print(self.bps)
        #print(hen)


    def getper(self,mat): #指定銘柄のPER推移を計算する。

        if self.bps == 0:
            print("SKIP of PER_Dict")
            self.per_now = 0
            self.per_max = 1
            self.per_min = 0
            #return round(per_now, 1), round(per_max, 1)
        else:
            mat = DataFrame(mat.dropna())
            self.maper = DataFrame(mat, columns=['Stock', 'PER', 'PER_MIN', 'PER1', 'PER2', 'PER3', 'PER4', 'PER_MAX'])
            self.maper['PER'] = self.maper['Stock'] / float(self.bps)  # 取得株価についてPER計算実施
            # print('MA')
            # print(MA)
            self.maper['PER_MAX'] = np.nanmax(self.maper['PER'])
            self.maper['PER_MIN'] = np.nanmin(self.maper['PER'])
            self.maper['PER1'] = self.maper['PER_MIN'] + (self.maper['PER_MAX'] - self.maper['PER_MIN']) / 5
            self.maper['PER2'] = self.maper['PER_MIN'] + 2 * (self.maper['PER_MAX'] - self.maper['PER_MIN']) / 5
            self.maper['PER3'] = self.maper['PER_MIN'] + 3 * (self.maper['PER_MAX'] - self.maper['PER_MIN']) / 5
            self.maper['PER4'] = self.maper['PER_MIN'] + 4 * (self.maper['PER_MAX'] - self.maper['PER_MIN']) / 5

            self.per_max = self.maper['PER_MAX'][0]
            self.per1 = self.maper['PER1'][0]
            self.per2 = self.maper['PER2'][0]
            self.per3 = self.maper['PER3'][0]
            self.per4 = self.maper['PER4'][0]
            self.per_min = self.maper['PER_MIN'][0]

            per_now_mat = DataFrame(self.maper['PER'])
            per_now = per_now_mat.tail(1)['PER'][0]
            self.per_now = float(per_now)


            # print( MA['PER'])
            # print('PER_NOW')
            # print(PER_NOW)
            # print("PER_MAX")
            # print(PER_MAX)
            #print("PER_MIN")
            #print(per_min)


    def smacross(self,mat):
        mat = DataFrame(mat.dropna())
        self.ma_smacross = DataFrame(mat, columns=['Stock', 'ZERO', 'DIF_SMA'])
        self.ma_smacross['ZERO'] = np.full(self.ma_smacross.shape[0], 0)
        self.ma_smacross['DIF_SMA'] = self.ma_smacross['Stock'] - self.dmatsma['Stock'].rolling(window=self.s_idou, center=False).mean()
        #self.dmatsma['MA_S'] = self.dmatsma['Stock'].rolling(window=self.s_idou, center=False).mean()


    def bolinger(self, mat):
        mat = DataFrame(mat.dropna())
        self.ma_boli = DataFrame(mat, columns=['Stock', 'MA_M', 'B_U1', 'B_U2', 'B_U3', 'B_L1', 'B_L2', 'B_L3', 'B_STV'])
        self.ma_boli['MA_M'] = self.ma_boli['Stock'].rolling(window=self.m_idou, center=False).mean()
        self.ma_boli['B_STV'] = self.ma_boli['Stock'].rolling(window=self.m_idou, center=False).std()
        self.ma_boli['B_U1'] = self.ma_boli['MA_M'] + self.ma_boli['B_STV']
        self.ma_boli['B_U2'] = self.ma_boli['MA_M'] + 2 * self.ma_boli['B_STV']
        self.ma_boli['B_U3'] = self.ma_boli['MA_M'] + 3 * self.ma_boli['B_STV']
        self.ma_boli['B_L1'] = self.ma_boli['MA_M'] - self.ma_boli['B_STV']
        self.ma_boli['B_L2'] = self.ma_boli['MA_M'] - 2 * self.ma_boli['B_STV']
        self.ma_boli['B_L3'] = self.ma_boli['MA_M'] - 3 * self.ma_boli['B_STV']
        #print("self.ma_boli")
        #print(self.ma_boli)

        #MA['Stock'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='-', marker='*', color='blue')
        #MA['MA_M'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='red')
        #MA['B_U1'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #MA['B_U2'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #MA['B_U3'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #MA['B_L1'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #MA['B_L2'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #MA['B_L3'].plot(ax=ax40, figsize=(FST, FSY), legend=True, linestyle='--', marker='', color='black')
        #ax40.set_xlim([datetime.datetime(Y, M - 2, 1), datetime.datetime(Y, M, D)])  # 縦軸の表示範囲。2か月前の1日から現在まで。1日にしたのはバグ回避
        #ax40.set_ylabel("Bolinger")
        #ax40.yaxis.tick_right()
        #ax40.legend_.remove()

    def smaweekget(self,mat):
        s_idou_w = setting.S_IDOU_W
        m_idou_w = setting.M_IDOU_W
        l_idou_w = setting.L_IDOU_W
        mat = DataFrame(mat.dropna())
        #print(mat)
        self.ma_smawkget = DataFrame(mat, columns=['Stock', 'MA_S', 'MA_M', 'MA_L'])
        self.ma_smawkget['MA_S'] = self.ma_smawkget['Stock'].rolling(window=s_idou_w, center=False).mean()
        self.ma_smawkget['MA_M'] = self.ma_smawkget['Stock'].rolling(window=m_idou_w, center=False).mean()
        self.ma_smawkget['MA_L'] = self.ma_smawkget['Stock'].rolling(window=l_idou_w, center=False).mean()

    def kairi(self,mat):
        #U0_NUM=5
        #U1_NUM=10
        self.m_idou=setting.M_IDOU
        mat = DataFrame(mat.dropna())
        self.ma_kairi = DataFrame(mat, columns=['Stock','MA_M','KAIRI','MAX','MIN','L1','L2','L3','ZERO'])



        self.ma_kairi['MA_M'] = self.dmatsma['Stock'].rolling(window=self.m_idou, center=False).mean()

        self.ma_kairi['KAIRI'] =(self.ma_kairi['Stock'].tail(200)/self.ma_kairi['MA_M'].tail(200))*100-100 
        self.kairi_max=round(np.max(self.ma_kairi['KAIRI']),1)
        self.kairi_min=round(np.min(self.ma_kairi['KAIRI']),1)       
        #print("MAX")   
        #print(self.kairi_max)
        #print("MIN")          
        #print(self.kairi_min)        
        self.ma_kairi['MAX'] = self.kairi_max
        self.ma_kairi['MIN'] = self.kairi_min
        self.ma_kairi['L1'] = self.kairi_min+ (self.kairi_max-self.kairi_min)/4
        self.ma_kairi['L2'] = self.kairi_min + 2*(self.kairi_max-self.kairi_min)/4
        self.ma_kairi['L3'] = self.kairi_min + 3*(self.kairi_max-self.kairi_min)/4     
        self.ma_kairi['ZERO'] = 0
        self.kairi_sig=np.std(self.ma_kairi['KAIRI']) #過去1年の株価のボラティリティーの標準偏差計算
        self.kairi_mean=np.mean(self.ma_kairi['KAIRI']) #過去1年の株価のボラティリティーの平均計算抽出
        #print("self.ma_kairi")       
        #print(self.ma_kairi)


        kairi_today=round(self.ma_kairi['KAIRI'].tail(1)[0],1) #本日の乖離率 
        if  kairi_today <= self.kairi_min + 1*(self.kairi_max-self.kairi_min)/4 :
            self.kairi_rank=0
        elif kairi_today > self.kairi_min + 1*(self.kairi_max-self.kairi_min)/4 and kairi_today <= self.kairi_min + 2*(self.kairi_max-self.kairi_min)/4:
            self.kairi_rank=1
        elif kairi_today > self.kairi_min + 2*(self.kairi_max-self.kairi_min)/4 and kairi_today <= self.kairi_min + 3*(self.kairi_max-self.kairi_min)/4:
            self.kairi_rank=2
        elif kairi_today > self.kairi_min + 3*(self.kairi_max-self.kairi_min)/4 and kairi_today <= self.kairi_min + 4*(self.kairi_max-self.kairi_min)/4+0.1:  # kairi_today=kairi_maxにてエラー発生。計算誤差の影響と思われる。+0.1を追加しエラーから逃げた。2019/01/15
            self.kairi_rank=3

        #print("kairi_today")    
        #print(kairi_today)  
        #print("kairi_min")    
        #print(self.kairi_min)
        #print("kairi_max")    
        #print(self.kairi_max)
        #print("kairi_rank")    
        #print(self.kairi_rank)  





        #print("ma_kairi")
        #print(self.ma_kairi)      
        #self.dmatsma['KAIRI'] = 100*math.log(self.dmatsma['MA_M'].tail(60)/self.dmatsma['Stock'].tail(60))
        #print()
        #print(self.dmatsma)
                 


    def combine(self):


        #今日-昨日の株価 , #昨日-おとといの株価の計算を含む 
        #self.comb = [round(self.volatirity[0],2),round(self.stock_exp,2), self.stock_now['Stock'][0], self.stock_kinou, self.stock_ototoi, round(self.per_max,2), round(self.per_min,2),round(self.per_now,2),self.stocknum
        #             , self.stock_n05sig['Stock'][0], self.stock_p05sig['Stock'][0], self.stock_n1sig['Stock'][0], self.stock_p1sig['Stock'][0], self.smatoday,self.kairi_max,self.kairi_min,self.kairi_rank]

        #1week前-2week前 , #2week前-3week前 株価の計算を含む 
        self.comb = [round(self.volatirity[0],2),round(self.stock_exp,2), self.stock_now['Stock'][0], self.dif_2_1_week, self.dif_3_2_week, round(self.per_max,2), round(self.per_min,2),round(self.per_now,2),self.stocknum
                     , self.stock_n05sig['Stock'][0], self.stock_p05sig['Stock'][0], self.stock_n1sig['Stock'][0], self.stock_p1sig['Stock'][0], self.smatoday,self.kairi_max,self.kairi_min,self.kairi_rank,self.stock_kinou]

        #print("self.comb")
        #print(self.comb)

        #print("self.dif_3_2_week")
        #print(self.dif_3_2_week)
        #print("self.dif_2_1_week")
        #print(self.dif_2_1_week )
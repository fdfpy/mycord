#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt


import setting
import datetime
import numpy as np
from pandas import Series ,DataFrame
import pandas as pd



class DictProcess(object):
    def __init__(self, data, stocknum):
        #self.data = data
        self.fig, (ax00, ax10, ax20, ax30, ax40, ax50, ax60, ax70) = plt.subplots(nrows=8, ncols=1, figsize=(setting.FST, setting.FSY))
        stock_now = data.stock_now["Stock"][0]

        dictmacd = Dict(data.dmatmacd)  #MACD Dict
        dictmacd.macd(ax70,"MACD chart")    #MACD Dict

        #dictsma = Dict(data.dmatsma)  #SMA Dict
        dictsma = Dict(data)  #SMA Dict
        dictsma.sma(ax10)    #SMA Dict

        dictvol = Dict(data.stockvolmat)  #Volatirity Dict
        dictvol.voldict(ax00, data.mean_vol[0], data.volatirity[0], stock_now, data.stocknum)    #Volatirity Dict

        dictsmacross = Dict(data.ma_smacross)  #Volatirity Dict
        dictsmacross.smacrossdict(ax30)

        dictboli = Dict(data.ma_boli)   #Bolinger Dict
        dictboli.bolidict(ax40)

        dictma_smawkget = Dict(data.ma_smawkget)   #SMA Week Dict
        dictma_smawkget.smaweekdict(ax50)


        dict_kairi = Dict(data)   #SKairi Dict     
        dict_kairi.kairidict(ax20)




        if data.bps == 0:
            pass
        else:
            dictper = Dict(data.maper)   #PER Week Dict
            dictper.perdict(ax60, data.bps, data.per_min, data.per1, data.per2, data.per3, data.per4, data.per_min)

        #plt.savefig(setting.HOME_PATH + str(stocknum) + ".png")
        plt.savefig("/var/www/html/" + str(stocknum) + ".png")

        plt.close()

class DictSummary(object):
    def __init__(self, data):
        self.dictsum(data)

    def dictsum(self,data):
        self.fig1, (bx00, bx01) = plt.subplots(nrows=2, ncols=1, figsize=(setting.FST, setting.FSY))
        dict_record_stockdb = Dict(data.record_stockdb)
        dict_record_stockdb.mean_vola_dict(bx00)   # MEAN-VOLATIRITY CHART
        #dict_record_stockdb.per_analyze_dict(bx01) # PER-ANALYZE CHART

        dict_record_stockdb.dif_updown_count(bx01) # PER-ANALYZE CHART       
        plt.close()



class DictTop(DictProcess):
    def __init__(self,Y = None ,M = None,D = None):
        self.Y = Y
        self.M = M
        self.D = D

        #self.stocknum = stocknum

    def xaxis_range(self, ax):
        ax.set_xlim([datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=setting.DAYPERIOD),
                          datetime.datetime(self.Y, self.M, self.D)])
    def xaxis_range_w(self, ax):
        ax.set_xlim([datetime.datetime(self.Y-2, self.M, self.D),
                          datetime.datetime(self.Y, self.M, self.D)])

    def settitle(self, ax, title):
        ax.set_title(title, fontsize=20)  # グラフのタイトル

    def ylabelset(self, ax, title): #y軸ラベル
        ax.set_ylabel(title, fontsize=30)


class Dict(DictTop):
    def __init__(self, data):
        super().__init__(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        self.data = data

    def macd(self, ax, title):

        self.data['DIF_MACD'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='+')
        self.data['ZERO'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='+')
        #self.ax.set_xlim([datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=60),
                          #datetime.datetime(self.Y, self.M, self.D)])
        self.xaxis_range(ax)  # X軸レンジ設定
        self.ylabelset(ax, "MACD")
        ax.yaxis.tick_right()
        self.settitle(ax,title)



    def sma(self, ax):

        dat = self.data.dmatsma
        comb = self.data.comb
        #comp = data.comp
        #print("comp")
        #print(comp)
        #self.ax = ax
        #print(self.data)
        #print('dat')
        #print(dat)
        dat['Stock'].plot(ax=ax, figsize=(setting.FST, setting.FSY),legend=True,linestyle='-',marker='*')
        dat['MA_S'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True,linestyle='--',marker='',color='red')
        dat['MA_M'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='',
                               color='green')
        dat['MA_L'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='',
                               color='black')

        self.xaxis_range(ax)  # X軸レンジ設定
        self.ylabelset(ax, "SMA")
        ax.yaxis.tick_right()
        data_lim = dat['Stock'][datetime.date(self.Y, self.M, self.D)-datetime.timedelta(days=60):datetime.date(self.Y, self.M, self.D)]
        yaxis_max = np.nanmax(data_lim) * 1.02
        yaxis_min = np.nanmin(data_lim) * 0.98
        ax.set_ylim((yaxis_min,yaxis_max))
        xlist = [datetime.datetime(self.Y, self.M, self.D) - datetime.timedelta(hours=6),
                 datetime.datetime(self.Y, self.M, self.D) - datetime.timedelta(hours=6),
                 datetime.datetime(self.Y, self.M, self.D) - datetime.timedelta(hours=6),
                 datetime.datetime(self.Y, self.M, self.D) - datetime.timedelta(hours=6)]
        ylist = [comb[9], comb[11], comb[10], comb[12]]
        col_name = ['-1shigma', '-0.5shigma', '+0.5shigma', '+1shigma']
        ax.text(datetime.datetime(self.Y,self.M,self.D)+datetime.timedelta(days=2),comb[2],'Today stock ' + str(comb[2]),fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)+datetime.timedelta(days=2),comb[2]*1.05,'Stock +(1/2)shigma ' + str(comb[10]),fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)+datetime.timedelta(days=2),comb[2]*1.1,'Stock +1shigma ' + str(comb[12]),fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)+datetime.timedelta(days=2),comb[2]*0.95,'Stock -(1/2)shigma ' + str(comb[9]),fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)+datetime.timedelta(days=2),comb[2]*0.9,'Stock -1shigma ' + str(comb[11]),fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)-datetime.timedelta(days=7),comb[13],'SMA_TODAY' + str(comb[13]),fontsize=15)
        ax.scatter(xlist,ylist,s=90,c='red') #sはplotのサイズ

        for label, x, y in zip(col_name, xlist, ylist):
          ax.annotate(
            label,
            xy = (x, y), xytext = (-20, -40),
            textcoords = 'offset points', ha = 'right',
            arrowprops = dict(arrowstyle='-', connectionstyle= 'arc3,rad=0.5'),size=10)


        #self.comb = [(0)round(self.volatirity[0],2),(1)round(self.mean_vol[0],2), (2)self.stock_now['Stock'][0], (3)self.stock_kinou, (4)self.stock_ototoi, (5)round(self.per_max,2), (6)round(self.per_min,2),(7)round(self.per_now,2),(8)self.stocknum
         #            , (9)self.stock_n05sig, (10)self.stock_p05sig, (11)self.stock_n1sig, (12)self.stock_p1sig, (13) self.smatoday]


    def kairidict(self, ax):
        dat = self.data.ma_kairi
        comb = self.data.comb

        #print(dat)
        dat['KAIRI'].plot(ax=ax, figsize=(setting.FST, setting.FSY),legend=True,linestyle='-',marker='*')
        dat['L1'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='--', marker='', color='green')      
        dat['L2'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='--', marker='', color='green')     
        dat['L3'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='--', marker='', color='green')     
        dat['MAX'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='--', marker='', color='green')  
        dat['MIN'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='--', marker='', color='green')      
        dat['ZERO'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=False, linestyle='-', marker='', color='black') 

        
        yaxis_max = round(comb[14] +0.5,1)
        yaxis_min = round(comb[15] -0.5,1)
        #print("yaxis_max")
        #print(yaxis_max)
        #print("yaxis_min")
        #print(yaxis_min)        

        ax.set_ylim((yaxis_min,yaxis_max))   # Y軸レンジ設定
        self.xaxis_range(ax)  # X軸レンジ設定
        self.ylabelset(ax, "KAIRI")
        ax.yaxis.tick_right()
        self.settitle(ax,"SMA25day kairi")
        ax.text(datetime.datetime(self.Y,self.M,self.D)-datetime.timedelta(days=30),yaxis_max-1.0,'KAIRI_MAX ' + str(yaxis_max) +'%' ,fontsize=15)
        ax.text(datetime.datetime(self.Y,self.M,self.D)-datetime.timedelta(days=30),yaxis_min+1.0,'KAIRI_MIN ' + str(yaxis_min) +'%',fontsize=15)




    def voldict(self, ax, mean_vol, volatirity, stock_now,stocknum):
        self.data['Stock'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='*', color='blue')
        self.data['+sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['+2sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='green')
        self.data['+3sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='red')
        self.data['-sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['-2sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='green')
        self.data['-3sigma'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='red')
        self.xaxis_range(ax)  # X軸レンジ設定
        ax.legend(loc='upper right', bbox_to_anchor=(-1, 1))
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol + volatirity + 0.1,'shig ' + str(round(mean_vol + volatirity, 2)) + '%')
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol + 2*volatirity + 0.1,'2shig ' + str(round(mean_vol + 2*volatirity, 2)) + '%')
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol + 3*volatirity + 0.1,'shig ' + str(round(mean_vol + 3*volatirity, 2)) + '%')
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol - volatirity + 0.1,'2shig ' + str(round(mean_vol - volatirity, 2)) + '%')
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol - 2*volatirity + 0.1,'shig ' + str(round(mean_vol -2 *volatirity, 2)) + '%')
        ax.text(datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30), mean_vol - 3*volatirity + 0.1,'2shig ' + str(round(mean_vol - 3*volatirity, 2)) + '%')
        print("stock_now")
        print(stock_now)
        ax.set_title(str(stocknum) + ' / ' + str(datetime.datetime.now().strftime("%Y/%m/%d")) + ' Today' + str(stock_now) ,fontsize=40)  # グラフのタイトル
        #ax.set_title(self.stocknum + ' / ' + str(datetime.datetime.now()) + ' Today' + stocknum,fontsize=40)  #
        self.ylabelset(ax, "delta %")
        ax.legend_.remove()
        ax.yaxis.tick_right()

    def smacrossdict(self, ax):
        self.data['DIF_SMA'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='+')  # 株価と短期単純移動平均線との差
        self.data['ZERO'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='+')
        ax.set_xlim([datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=60),
                          datetime.datetime(self.Y, self.M, self.D)])
        self.ylabelset(ax, "SMA_DIF")
        ax.yaxis.tick_right()

    def bolidict(self, ax):
        self.data['Stock'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='*', color='blue')
        self.data['MA_M'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='red')
        self.data['B_U1'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['B_U2'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['B_U3'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['B_L1'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['B_L2'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        self.data['B_L3'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
        ax.set_xlim([datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=60), datetime.datetime(self.Y, self.M, self.D)])
        self.ylabelset(ax, "Bolinger")
        ax.yaxis.tick_right()
        ax.legend_.remove()

    def smaweekdict(self,ax):
        #print(self.data)
        self.data['Stock'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='*',color='blue')
        self.data['MA_S'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle=':', marker='', color='red')
        self.data['MA_M'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle=':', marker='', color='green')
        self.data['MA_L'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle=':', marker='', color='blue')
        data_lim = self.data['Stock'][datetime.date(self.Y-2, self.M, self.D):datetime.date(self.Y, self.M, self.D)]
        yaxis_max = np.nanmax(data_lim) * 1.02
        yaxis_min = np.nanmin(data_lim) * 0.98
        #print("yaxis_min")
        #print(yaxis_min)
        ax.set_ylim((yaxis_min,yaxis_max))
        self.xaxis_range_w(ax)
        self.ylabelset(ax, "SMA WEEK")
        ax.yaxis.tick_right()

    def perdict(self, ax, en, per_min, per1, per2, per3, per4, per_max):
        if en == 0:
            pass
        else:
            #print("PER_MIN")
            #print(per_min)
            self.data['PER'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='-', marker='*', color='blue')
            self.data['PER_MIN'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.data['PER1'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.data['PER2'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.data['PER3'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.data['PER4'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.data['PER_MAX'].plot(ax=ax, figsize=(setting.FST, setting.FSY), legend=True, linestyle='--', marker='', color='black')
            self.ylabelset(ax, "PER")
            self.xaxis_range(ax)
            ax.text(datetime.datetime(self.Y, self.M, 1), per_min + 0.1, 'PER_MIN ' + str(round(per_min, 1)))
            ax.text(datetime.datetime(self.Y, self.M, 1), per1 + 0.1, 'PER1 ' + str(round(per1, 1)))
            ax.text(datetime.datetime(self.Y, self.M, 1), per2 + 0.1, 'PER2 ' + str(round(per2, 1)))
            ax.text(datetime.datetime(self.Y, self.M, 1), per3 + 0.1, 'PER3 ' + str(round(per3, 1)))
            ax.text(datetime.datetime(self.Y, self.M, 1), per4 + 0.1, 'PER4 ' + str(round(per4, 1)))
            ax.text(datetime.datetime(self.Y, self.M, 1), per_max + 0.1, 'PER_MAX ' + str(round(per_max, 1)))
            ax.yaxis.tick_right()

    def mean_vola_dict(self,bx):  # 各銘柄の過去1年の株価上昇率と1日単位でのボラティリティーの関係をグラフ化する。
        #MEIGARA_DB = pd.read_csv('/home/pi/Desktop/stock/sqltest.csv', names=(
        #'STOCK_NUM', 'COM_NAME', 'URL', 'SIGMA', 'EXPECTATION', 'KESSAN', 'OTOTOI', 'YESTERDAY', 'TODAY', 'PER',
        #'LASTYEAR_PROFIT_PER_STOCK', 'THISYEAR_PROFIT_PER_STOCK', 'KESSAN_MONTH', 'PERMAX', 'PERMIN'))
        x_num = self.data['EXPECTATION']

        y_num = self.data['SIGMA']
        #print("x_num")       
        #print(x_num)
        #print("y_num")
        #print(y_num)
        col_name = self.data['STOCK_NUM']
        ototoi_num = self.data['OTOTOI']
        kinou_num = self.data['YESTERDAY']

        etf_info =DataFrame(self.data.ix[self.data['STOCK_NUM'] == 1570])
        #print("etf_info")
        #print(etf_info)
        #print("etf_info['EXPECTATION']")
        #print(etf_info['EXPECTATION'])
        #print("etf_info['EXPECTATION'][1]")   
        #print(etf_info['EXPECTATION'][1])        
        #print(etf_info['EXPECTATION'][0])
        #print(etf_info['SIGMA'])    
        #print(etf_info['EXPECTATION'][1])        
        #print(etf_info['SIGMA'][0])

        #print(x_num)
        #print("y_num")
        #print(y_num)
        #print("np.max(y_num)")       
        #print(np.max(y_num))
        #print(col_name)
        #print("ototoi,kinou")
        #print(ototoi_num)
        #print(kinou_num)
        #Set the x and y limits of the plot (optional, remove this if you don't see anything in your plot)
        bx.set_xlim([np.min(x_num) - 0.05*abs(np.min(x_num)) , 1.05 * np.max(x_num)])
        bx.set_ylim([0, 1.05 * np.max(y_num)])
        # Set the plot axis titles
        bx.set_xlabel('Expected returns %', fontsize=60)
        bx.set_ylabel('Volatirity %', fontsize=60)
        bx.tick_params(labelsize=60)
        bx.scatter(x_num, y_num, s=120)  # sはplotのサイズ
        bx.set_title("Expected Returns vs Volatility", fontsize=60)  # グラフのタイトル
        bx.plot([etf_info['EXPECTATION'][1], etf_info['EXPECTATION'][1]], [0, 1.05 * np.max(y_num)], '--',color="blue") #20190105 pre
        #bx.plot([etf_info['EXPECTATION'][0], etf_info['EXPECTATION'][0]], [0, 1.05 * np.max(y_num)], '--',color="blue") #20190105 modified
        #bx.plot([30, 30], [0, 1.05 * np.max(y_num)], '--',color="blue")
        bx.plot([np.min(x_num) - 2, 1.05 * np.max(x_num)], [etf_info['SIGMA'][1], etf_info['SIGMA'][1]], '--',color="blue") #20190105 pre
        #bx.plot([np.min(x_num) - 2, 1.05 * np.max(x_num)], [etf_info['SIGMA'][0], etf_info['SIGMA'][0]], '--',color="blue")  #20190105 modified
        #bx.plot([np.min(x_num) - 25, etf_info['EXPECTATION'][0]], [1.05 * np.max(x_num), etf_info['EXPECTATION'][0]], '--')

        for label, x, y, ototoi, kinou in zip(col_name, x_num, y_num, ototoi_num, kinou_num):

            if (ototoi > 4 and kinou > 4):
                iro = 'red'
            else:
                iro = 'black'

            bx.annotate(
                label,
                xy=(x, y), xytext=(0, 20), color=iro,
                textcoords='offset points', ha='right',
                arrowprops=dict(arrowstyle='-', connectionstyle='arc3'), size=25)


        #plt.savefig(setting.HOME_PATH + "MEANVOL.png")
        #plt.savefig("/var/www/html/MEANVOL.png")


    def dif_updown_count(self,bx):
        updownDB = pd.read_csv('/home/pi/Desktop/stock/count.csv', names=['DATE','COUNT'],index_col=0,parse_dates=True)
        #print(updownDB)
        #updownDB['COUNT'].plot(bx=bx, figsize=(setting.FST, setting.FSY),legend=True,linestyle='-',marker='*')
        #bx.set_xlim([-10,10])
        #bx.set_ylim([-10,10])

        #bx.plot([1,2],[3,4], '--')
        #updownDB.plot(bx=bx)
        bx.set_xlim([datetime.datetime(self.Y, self.M, self.D)-datetime.timedelta(days=30),datetime.datetime(self.Y, self.M, self.D)])
        bx.set_ylim([-30,30])   
   
        bx.plot(updownDB, linestyle='-', marker='*',color='blue',markersize=30)
        bx.tick_params(labelsize=30)
        bx.set_xlabel('DATE', fontsize=60)     
        bx.set_ylabel('UP COUNT - DOWN COUNT', fontsize=60)
        bx.set_title(" UP COUNT - DOWN COUNT of STOCKs" , fontsize=60)  # グラフのタイトル
        bx.locator_params(axis='y',tight=True, nbins=11)
        bx.yaxis.tick_right()
        plt.savefig("/var/www/html/MEANVOL.png")



    def per_analyze_dict(self,bx):  # 各銘柄の過去1年のPER最大値に対する現在のPERの割合とPERをグラフ化する。
        #MEIGARA_DB = pd.read_csv('/home/pi/Desktop/stock/sqltest.csv', names=(
        #'STOCK_NUM', 'COM_NAME', 'URL', 'SIGMA', 'EXPECTATION', 'KESSAN', 'OTOTOI', 'YESTERDAY', 'TODAY', 'PER',
        #'LASTYEAR_PROFIT_PER_STOCK', 'THISYEAR_PROFIT_PER_STOCK', 'KESSAN_MONTH', 'PERMAX', 'PERMIN'))
        # plt.scatter(MEIGARA_DB['SIGMA'], MEIGARA_DB['EXPECTION'])
        # fig1, ((ax01)) = plt.subplots(nrows=1, ncols=1, figsize=(FST,FSY/3+5))
        permax = self.data['PERMAX']
        y_num = self.data['PER']
        permin = self.data['PERMIN']
        x_num = 100 * (y_num - permin) / (permax - permin)
        col_name = self.data['STOCK_NUM']
        ototoi_num = self.data['OTOTOI']
        kinou_num = self.data['YESTERDAY']

        #print('x_num')
        #print(x_num)
        #print('y_num')
        #print(y_num)
        #col_name = self.data['STOCK_NUM']
        #ototoi_num = self.data['OTOTOI']
        #kinou_num = self.data['YESTERDAY']




        # print("PERDICT")
        # print(permax)
        # print(permin)
        # print(x_num)
        # print(y_num)
        # print(col_name)
        # Set the x and y limits of the plot (optional, remove this if you don't see anything in your plot)
        bx.set_xlim([0, 1.01 * np.max(x_num)])
        bx.set_ylim([4, 1.01 * np.max(y_num)])
        # Set the plot axis titles
        bx.set_xlabel('PER/PERMAX (%)', fontsize=60)
        bx.set_ylabel('PER ', fontsize=60)
        bx.tick_params(labelsize=60)
        bx.scatter(x_num, y_num, s=180)  # sはplotのサイズ
        bx.set_title("PER/PERMAX vs PER", fontsize=60)  # グラフのタイトル
        bx.plot([0, 0], [0, 10], '--')

        # print("CHECK")
        # グラフにアノテーションを付けます。詳しくは、以下を参照してみてください。
        # http://matplotlib.org/users/annotations_guide.html
        #for label, x, y in zip(col_name, x_num, y_num):
        # bx01.annotate(
        # label,
        # xy = (x, y), xytext = (0, 20),
        # textcoords = 'offset points', ha = 'right',
        # arrowprops = dict(arrowstyle='-', connectionstyle= 'arc3'),size=40)

        for label, x, y, ototoi, kinou in zip(col_name, x_num, y_num, ototoi_num, kinou_num):

            if (ototoi > 4 and kinou > 4):
                iro = 'red'
            else:
                iro = 'black'

            bx.annotate(
                label,
                xy=(x, y), xytext=(0, 20), color=iro,
                textcoords='offset points', ha='right',
                arrowprops=dict(arrowstyle='-', connectionstyle='arc3'), size=25)
        #plt.savefig(setting.HOME_PATH + "MEANVOL.png")
        plt.savefig("/var/www/html/MEANVOL.png")
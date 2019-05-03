#-*- coding:utf-8 -*-
from models import dbcontrol,analyze
from views import dict
import setting




def allproc(stocknum,i,leng) :
    csvmodel = dbcontrol.CSVModel()   #CSVファイルの作成
    technical = analyze.Technical(stocknum) #株価データの収集とテクニカル分析の実施
    dbcont = dbcontrol.DBCONT(technical.comb) #テクニカル分析の結果をstock.dbとcsvファイルに書き込み
    dictprocess = dict.DictProcess(technical,stocknum) #テクニカル分析の結果のグラフ作成
    if  i==(leng-1):  #全銘柄の分析完了後に、EXP-VOLグラフとPER時系列グラフを作成
        dictsummary = dict.DictSummary(technical)
        print("dictsummary")


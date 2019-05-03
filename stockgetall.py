#-*- coding:utf-8 -*-
import controller.process
import pandas as pd
import setting
import datetime

stocknum_db = pd.read_csv(setting.CSV_DB_PATH, names=setting.CSV_DB_PATH_COLUMNS) #分析する銘柄一覧を取得
i = 0
stocknum_db_len = int(len(stocknum_db['STOCK_NUM']))

while i < stocknum_db_len:
    print(i)
    controller.process.allproc(stocknum_db['STOCK_NUM'][i],i,stocknum_db_len)
    i=i+1
    d = datetime.datetime.today()
    print (d.strftime("%Y-%m-%d %H:%M:%S"))

print("## done ##")

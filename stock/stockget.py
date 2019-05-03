#-*- coding:utf-8 -*-
import controller.process
import pandas as pd
import setting
import datetime
import sys

#stocknum_db = pd.read_csv(setting.CSV_DB_PATH, names=setting.CSV_DB_PATH_COLUMNS) #分析する銘柄一覧を取得
#i = 0
print("## start ##")

d = datetime.datetime.today()
print (d.strftime("%Y-%m-%d %H:%M:%S"))

stocknum = sys.argv[1]
controller.process.allproc(stocknum,0,1)

d = datetime.datetime.today()
print (d.strftime("%Y-%m-%d %H:%M:%S"))

#while i < len(stocknum_db['STOCK_NUM']):
#    print(i)
#    controller.process.allproc(stocknum_db['STOCK_NUM'][i])
#    i=i+1
#    date2 = datetime.datetime.now()
#    print(date2)

print("## done ##")

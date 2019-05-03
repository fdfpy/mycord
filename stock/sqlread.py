# coding: utf-8

import sys
import sqlite3
import setting
import csv
from models import dbcontrol
reload(sys)
sys.setdefaultencoding('utf-8')




stock_num=sys.argv[1]
#sel=unicode(sel, 'utf-8')

dbcontrol.SQLDBCONT(stock_num,setting.CSV_READ_PATH)


print("stocknum")
print(stock_num)
print("//")






# coding: utf-8

import sys
import sqlite3
import pandas as pd
import csv
from models import dbcontrol
reload(sys)
sys.setdefaultencoding('utf-8')
import setting

sel=sys.argv[1]
#sel=unicode(sel, 'utf-8')

print(sel)

sqldbcont = dbcontrol.SQLDBCONT(sel,setting.CSV_CYU_DB_PATH)





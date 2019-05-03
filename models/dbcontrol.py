#-*- coding:utf-8 -*-
import os
import pathlib
import pandas as pd
import setting
import sqlite3
import csv


#SEC_CSV_FILE_PATH =r'C:\Users\Takeshi\PycharmProjects\Stock\stockdata.csv'
CSV_COLUMNS = ['STOCK_NUM', 'COM_NAME', 'URL', 'SIGMA', 'EXPECTATION', 'KESSAN', 'OTOTOI', 'YESTERDAY', 'TODAY', 'PER', 'LASTYEAR_PROFIT_PER_STOCK', 'THISYEAR_PROFIT_PER_STOCK', 'KESSAN_MONTH', 'PERMAX', 'PERMIN','KAIRI_MIN', 'KAIRI_MAX','KAIRI_RANK']


class DBCONT(object):

    def __init__(self, data):
        #self.stocknum = stocknum
        #print("DBCOMT data")
        #print(data)
        self.csv_file = setting.CSV_FILE_PATH
        self.csv_cyu_file=setting.CSV_CYU_DB_PATH
        self.db_path = setting.DB_PATH
        self.csv_db_path = setting.CSV_DB_PATH
        self.csv_cyu_db_path = setting.CSV_CYU_DB_PATH
        v_sigma = data[0]
        v_exp =data[1]
        s_num =data[8]
        s_ototoi_yesterday =data[3]-data[4]
        s_yesterday_today =data[2]-data[3]
        per_now =data[7]
        today =data[2]
        per_max = data[5]
        per_min =data[6]
        kairi_max = data[14]
        kairi_min =data[15]
        kairi_rank=data[16]
        #print("kairi max")
        #print(kairi_max)
        #print("kairi min")
        #print(kairi_min)
        ##comb = (v_sigma, v_exp, s_num, s_ototoi_yesterday, s_yesterday_today, per_now, today, per_max, per_min)
        comb = (v_sigma, v_exp, s_num, s_ototoi_yesterday, s_yesterday_today, per_now, today, per_max, per_min,kairi_min,kairi_max)
        #print("self.comb")
        #print(comb)
        ##self.dbkakikomi(v_sigma, v_exp, str(s_num), int(s_ototoi_yesterday), int(s_yesterday_today), per_now, today, per_max, per_min)
        self.dbkakikomi(v_sigma, v_exp, str(s_num), int(s_ototoi_yesterday), int(s_yesterday_today), per_now, today, per_max, per_min,kairi_min,kairi_max,kairi_rank)


    ##def dbkakikomi(self,v_sigma,v_exp,s_num,s_ototoi_yesterday,s_yesterday_today,per_now,today,per_max,per_min):  #各銘柄のボラティリティーをDBに追加する関数
    def dbkakikomi(self,v_sigma,v_exp,s_num,s_ototoi_yesterday,s_yesterday_today,per_now,today,per_max,per_min,kairi_min,kairi_max,kairi_rank):  #各銘柄のボラティリティーをDBに追加する関数
        con = sqlite3.connect(self.db_path)
        print("self.db_path")
        print(self.db_path)
        con.text_factory = str
        cur = con.cursor()
        #print(s_num)
        #print(s_ototoi_yesterday)
        today = int(today)
        #print(today)
        #print("ZXX")
        ##insert_sql='UPDATE STOCK_INFO SET SIGMA=?, EXPECTATION=?,OTOTOI=?,YESTERDAY=?,TODAY=?,PER=?,PERMAX=?,PERMIN=? WHERE STOCK_NUM=?'
        insert_sql='UPDATE STOCK_INFO SET SIGMA=?, EXPECTATION=?,OTOTOI=?,YESTERDAY=?,TODAY=?,PER=?,PERMAX=?,PERMIN=?,KAIRI_MIN=?,KAIRI_MAX=?,KAIRI_RANK=? WHERE STOCK_NUM=?'
        ##cur.execute(insert_sql,(v_sigma,v_exp,s_ototoi_yesterday,s_yesterday_today,today,per_now,per_max,per_min,s_num))
        cur.execute(insert_sql,(v_sigma,v_exp,s_ototoi_yesterday,s_yesterday_today,today,per_now,per_max,per_min,kairi_min,kairi_max,kairi_rank,s_num))
        print("#")
        con.commit()
        self.db_dump(cur)
        con.close()

    def db_dump(self,c):  #SQLITE3 DBの値をCSVファイルにダンプする関数
        con = sqlite3.connect(self.db_path)
        con.text_factory = str
        cur = con.cursor()
        sql_com = 'SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
        tmp = c.execute(sql_com)
        with open(self.csv_db_path, 'w',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(tmp)
            f.close()
        con.close()



class SQLDBCONT():

    def __init__(self, sel,csv_cyu_db_path):

        self.csv_cyu_db_path = csv_cyu_db_path
        self.db_path = setting.DB_PATH
        self.selectdb3(sel)


    def selectdb3(self,sel): #指定した銘柄のみを抽出する
        InxARY = sel.split(',')  #文字列を配列に分解する
        #print(InxARY)
        self.sqlcommake(InxARY) #SQL文を自動記述する
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        #print("C1")
        df = pd.read_sql_query(self.sqlcommand,con)
        #print("C2")
        df=df.set_index('STOCK_NUM')
        #print(df)
        #print("C")
        df.to_csv(self.csv_cyu_db_path,header=False)
        #print("D")
        #self.dump_csv(df,self.csv_cyu_db_path)
        #self.db_dump(self.db_cyusyutsu_path,self.csv_cyu_db_path, cur)
        #print(df1)
        #df2 = df.set_index('STOCK_NUM')


    def sqlcommake(self,vec): #list vecに入っている複数銘柄について　　SELECT * FROM STOCK_INFO WHERE STOCK_NUM IN (*,*,)というSQLコマンドを自動記述する
        moji = "("
        for j in range(len(vec)-1):
            moji = moji + vec[j] + ","
        moji = moji+ vec[len(vec)-1] +")"
        self.sqlcommand = "SELECT * FROM STOCK_INFO WHERE STOCK_NUM IN" + moji

    #def dump_csv(self,df,csv_file_path):
        #with open(csv_file, 'w',encoding='utf-8') as f:
            #writer = csv.writer(f)
        #df.to_csv(csv_file_path)
            #writer.writerows(map(lambda x: [x], tmp))
            #f.close()








class DBModel(object):   #指定した箇所にCSVファイルがない場合、新たにcsvファイルを作成する。
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()  #指定したパスにcsvファイルを作成する。


class CSVModel(DBModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kwargs):
        if not csv_file:
            csv_file = self.get_csv_file_path()

        super().__init__(csv_file, *args, **kwargs)
        self.column = CSV_COLUMNS
        self.load_data()

    def get_csv_file_path(self):
        """Set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        try:
            import setting
            if setting.CSV_FILE_PATH:
                csv_file_path = setting.CSV_FILE_PATH
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = SEC_CSV_FILE_PATH
        return csv_file_path



    def load_data(self):
        """Load csv data.

        Returns:
            dict: Returns ranking data of dict type.
        """
        self.data = pd.read_csv(self.csv_file, names=CSV_COLUMNS)
        return self.data
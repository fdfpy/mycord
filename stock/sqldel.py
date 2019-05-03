# coding: utf-8

import sys
import sqlite3
import pandas as pd
import csv
reload(sys)
sys.setdefaultencoding('utf-8')

###########################
#入力情報の読みとり
###########################

#Inx0=sys.argv[0]
#Inx1=Inx0[1]
#print(Inx0)
#print("AAA")
Inx=sys.argv[1]
Inx=unicode(Inx, 'utf-8')
#print(Inx)
InxARY=Inx.split(',')
#print('watch')
#print(InxARY[0])





#NAM_S=sys.argv[2]
f=open('/home/pi/Desktop/stock/sqltest.txt','w')
f.write(sys.argv[1])
#f.write("sys.argv[2]")
#f.write(sys.argv[4])
f.close()

#print(sys.argv[1])

########################################
# DBに記録した情報をcsvファイルにダンプする
########################################


def delete_task(c,num):

    sql='DELETE FROM STOCK_INFO WHERE STOCK_NUM=?'
    cur=c.cursor()
    cur.execute(sql,(num,))
    c.commit()

def db_dump(c):
    sql_com='SELECT * FROM STOCK_INFO ORDER BY STOCK_NUM ASC'
    #print("1")
    cur=c.cursor()
    #print("2")
    tmp=cur.execute(sql_com)
    #print(tmp)
    #print("3")   
    with open('/home/pi/Desktop/stock/stockdata.csv','w') as f:
        #print("4")
        writer=csv.writer(f)
        #print(writer)
        #print("5")
        writer.writerows(tmp)
        #print("6")  





    
    #f=open('/home/pi/Desktop/stock/sqltest.txt','w')
    #sql_com='SELECT * FROM STOCK_INFO'
    #for row in c.execute(sql_com):
       # f.write(str(row))
    #f.close()


###########################################
# メイン処理
###########################################

if __name__=='__main__':



    
    try:

######################
# 指定行を削除する
######################
        for i in InxARY:
            #print("A")
            con=sqlite3.connect("/home/pi/Desktop/stock/stock.db3")
            #print("X")
            delete_task(con,i)
            #print("ZZ")
            #con.text_factory=str
            #cur=con.cursor()
            #insert_sql='INSERT INTO STOCK_INFO (STOCK_NUM,COM_NAME,BUY_VAL,PER,PROFIT_R) values (?,?,?,?,?)'
            #insert_sql='DELETE FROM STOCK_INFO WHERE STOCK_NUM=120'      
            #print(Inx)
            #STOCK_INFO=(NUM_S,NAM_S,V_BUY,0,0)
            #cur.execute(insert_sql)
            #con.commit()
            db_dump(con)
            #print("ZZZ")
            con.close()
            print("DEL DONE")
            #print 'parameter1 is ' + sys.argv[1]
            #print 'parameter2 is ' + sys.argv[2]
            #f=open('/home/pi/Desktop/stock/sqltest.txt','w')
            #f.write(sys.argv[1])
            #f.write(sys.argv[2])
            #f.close()
    except Exception as ex:
        f=open('/home/pi/Desktop/stock/sqltest.txt','w')
        f.write(format(ex))
        f.close()



#except sqlite3.IntegrityError.datatype mismatch      

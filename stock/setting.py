
CSV_READ_PATH=r'/home/pi/Desktop/stock/read.csv'
CSV_CYUSYUTSU_PATH =r'/home/pi/Desktop/stock/csvcyusyutsu.csv'
SEC_CSV_FILE_PATH =r'/home/pi/Desktop/stock/stockdata.csv'
CSV_FILE_PATH = r'/home/pi/Desktop/stock/stockdata.csv'
HOME_PATH = r'/home/pi/Desktop/stock/'
CSV_DB_PATH = r'/home/pi/Desktop/stock/stockdata.csv'
CSV_DB_PATH_COLUMNS = ('STOCK_NUM', 'COM_NAME', 'URL', 'SIGMA', 'EXPECTATION', 'KESSAN', 'W2W3', 'W1W2', 'TODAY', 'PER',
        'LASTYEAR_PROFIT_PER_STOCK', 'THISYEAR_PROFIT_PER_STOCK', 'KESSAN_MONTH', 'PERMAX', 'PERMIN','KAIRIMIN','KAIRIMAX','KAIRI_RANK','KINOU')
CSV_CYU_DB_PATH = r'/home/pi/Desktop/stock/stockdatacyu.csv'


DB_PATH = r'/home/pi/Desktop/stock/stock.db3'


GET_STOCK_F = 0  # 0: getting stockdata from Web ,  1: getting stockdata from localfile



#######  chart duration day  #######

DAYPERIOD=120

#######  MACD parameter #########

S_DUR = 5  #short period parameter
L_DUR = 25 #long period paramter
SIG_DUR = 9 #signal period parameter


#######  SMA parameter day #########

S_IDOU = 5  #short period parameter
M_IDOU = 25 #long period paramter
L_IDOU = 75 #signal period parameter

#######  SMA parameter week #########

S_IDOU_W = 13  #short period parameter
M_IDOU_W = 26 #long period paramter
L_IDOU_W = 52 #signal period parameter







####### Chart parameter ###########
FST = 40
FSY = 40


import  database_function
import pandas as pd
import numpy as np
import rqdatac as rq
rq.init()

price_config = {"host":"10.63.27.118","user":"test","password":"123456","data_base":"AshareDayPrices","port":3306}
price_db ,price_cur = database_function.db_connect(price_config)

sql="select trade_dt,stcode,adj_close from stock_daily_price where trade_dt>='20070101' and trade_dt<='20190101'"
price_result = list(database_function.db_select(price_cur,sql ))
price_result = pd.DataFrame(price_result)

price_result=price_result.rename(columns={0:'trade_date',1:'stcode',2:'price'})
price_result.to_csv("price.csv",index=None)
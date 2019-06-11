import pandas as pd
import numpy as np
####建立持仓信息
#读入信号值
signal_60=pd.read_csv("factor60.csv",index_col=0)
signal_120=pd.read_csv("factor120.csv",index_col=0)
signal_250=pd.read_csv("factor250.csv",index_col=0)
signal_60=signal_60.stack(dropna=False)
signal_120=signal_120.stack(dropna=False)
signal_250=signal_250.stack(dropna=False)
signal_60=signal_60.reset_index()
signal_120=signal_120.reset_index()
signal_250=signal_250.reset_index()
signal_60=signal_60.rename(columns={'level_0':'trade_date','level_1':'stcode',0:'signal_60'})
signal_120=signal_120.rename(columns={'level_0':'trade_date','level_1':'stcode',0:'signal_120'})
signal_250=signal_250.rename(columns={'level_0':'trade_date','level_1':'stcode',0:'signal_250'})

#读入股票状态
status=pd.read_csv("stock_status.csv")
df_combined=signal_60.merge(signal_120,left_on=['trade_date','stcode'],right_on=['trade_date','stcode'],how='inner')
df_combined=df_combined.merge(signal_250,left_on=['trade_date','stcode'],right_on=['trade_date','stcode'],how='inner')
df_combined=df_combined.merge(status,left_on=['trade_date','stcode'],right_on=['trade_date','stcode'],how='left')

#建仓
def set_position(rank,threshold,D):
    """

    :param rank: 排序期 60 120 250
    :param threshold: 阈值 -0.1，-0.05，-0.02，-0.01，0，0.01,0.02,0.05,0.1
    :param D: 5,10,20,40
    :return: D天一次的持仓信息
    """
    #超过阈值的记为1
    df_combined1=df_combined
    df_combined1['sign']=None
    df_combined1['sign'][df_combined1['signal_'+str(rank)]>threshold]=1
    df_position=df_combined1[['trade_date','stcode','status','sign']]
    #与股票状态相乘
    df_position['sign']=df_position['status']*df_position['sign']
    #变形
    df_position=df_position.pivot(index='trade_date',columns='stcode',values='sign')
    #切片
    df_position=df_position.iloc[range(0,len(df_position),D),:]
    df_position=df_position.reset_index()

    return df_position

for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [0.3]:
            print("rank"+str(rank)+"D"+str(D)+"threshold"+str(threshold)+".csv")
            position=set_position(rank,threshold,D)
            position.to_csv("rank"+str(rank)+"D"+str(D)+"threshold"+str(threshold)+"_position.csv",index=None)


price=pd.read_csv("price.csv")
price=price.pivot(index='trade_date',columns='stcode',values='price')
#转换日期格式
price.index=pd.to_datetime(price.index,format='%Y%m%d')
price.index=price.index.strftime("%Y-%m-%d")
#转换股票代码
import rqdatac as rq
rq.init()
new_col=rq.id_convert(list(price.columns))
price.columns=new_col
##处理个股收益率
def forward_return(price,holding_period):
    """

    :param price: 收盘价
    :param holding_period:持有期
    :return: 收益率序列
    """
    df_return=price/price.shift(-1*holding_period)-1
    return df_return
forward_return(price,5).to_csv("rt_5.csv")
forward_return(price,10).to_csv("rt_10.csv")
forward_return(price,20).to_csv("rt_20.csv")
forward_return(price,40).to_csv("rt_40.csv")





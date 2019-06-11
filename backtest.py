import pandas as pd
import numpy as np
import math


def cal_riskrt(filename,D):
    source=pd.read_csv(filename,index_col=0)
    source=source.dropna()
    #新建一个数据框记录各种指标
    df=pd.DataFrame(columns=['rt','volatility','mdd','sharpe','calmar'],index=['rt1','rt2','rt3'])
    #计算多头各项指标
    rt=pd.DataFrame(source['rt1'])
    rt['prod'] = np.cumprod(rt['rt1'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['rt1'].std() * (math.sqrt(250) )
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    #计算胜率
    win_rate=len(rt[rt['rt1']>0])/len(rt.dropna(subset=['rt1']))

    df.loc['rt1','rt']=annual_ret
    df.loc['rt1','volatility']=volatility
    df.loc['rt1','mdd']=mdd
    df.loc['rt1','sharpe']=sharpe
    df.loc['rt1','calmar']=calmar
    df.loc['rt1','win']=win_rate


    # 计算多头各项指标
    rt = pd.DataFrame(source['rt2'])
    rt['prod'] = np.cumprod(rt['rt2'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['rt2'].std() * (math.sqrt(250))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    win_rate = len(rt[rt['rt2'] > 0]) / len(rt.dropna(subset=['rt2']))
    df.loc['rt2', 'rt'] = annual_ret
    df.loc['rt2', 'volatility'] = volatility
    df.loc['rt2', 'mdd'] = mdd
    df.loc['rt2', 'sharpe'] = sharpe
    df.loc['rt2', 'calmar'] = calmar
    df.loc['rt2','win']=win_rate

    # 计算多头各项指标
    rt = pd.DataFrame(source['rt3'])
    rt['prod'] = np.cumprod(rt['rt3'] + 1)
    holding_period = pd.to_datetime(rt.index.values[-1]) - pd.to_datetime(rt.index.values[0])
    # #年化收益率
    annual_ret = pow(rt['prod'][-1], 365 / holding_period.days) - 1
    # #年化波动率
    volatility = rt['rt3'].std() * (math.sqrt(250))
    # #sharpe
    sharpe = annual_ret / volatility
    # #计算最大回撤
    rt['max2here'] = rt['prod'].expanding(1).max()
    rt['dd2here'] = (rt['prod'] / rt['max2here']) - 1
    mdd = rt['dd2here'].min()
    calmar = annual_ret / abs(mdd)
    win_rate = len(rt[rt['rt3'] > 0]) / len(rt.dropna(subset=['rt3']))
    df.loc['rt3', 'rt'] = annual_ret
    df.loc['rt3', 'volatility'] = volatility
    df.loc['rt3', 'mdd'] = mdd
    df.loc['rt3', 'sharpe'] = sharpe
    df.loc['rt3', 'calmar'] = calmar
    df.loc['rt3', 'win'] = win_rate


    return df

#等权组合
iterables=[['rank60','rank120','rank250'],['D5','D10','D20','D40']]
index=pd.MultiIndex.from_product(iterables, names=['ranking', 'holding_period'])
df_rt1=pd.DataFrame(index=index,columns=[-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1])

for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1]:
            ratio=cal_riskrt("rank" + str(rank) + "D" + str(D) + "threshold" + str(threshold) + "_new.csv",D)
            df_rt1.loc[('rank'+str(rank),'D'+str(D)),threshold]=ratio.iloc[0,5]
#总市值加权
iterables=[['rank60','rank120','rank250'],['D5','D10','D20','D40']]
index=pd.MultiIndex.from_product(iterables, names=['ranking', 'holding_period'])
df_rt2=pd.DataFrame(index=index,columns=[-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1])

for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1]:
            ratio=cal_riskrt("rank" + str(rank) + "D" + str(D) + "threshold" + str(threshold) + "_new.csv",D)
            df_rt2.loc[('rank'+str(rank),'D'+str(D)),threshold]=ratio.iloc[1,5]
#流通市值加权
df_rt3=pd.DataFrame(index=index,columns=[-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1])

for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1]:
            ratio=cal_riskrt("rank" + str(rank) + "D" + str(D) + "threshold" + str(threshold) + "_new.csv",D)
            df_rt3.loc[('rank'+str(rank),'D'+str(D)),threshold]=ratio.iloc[2,5]
#df_rt1.to_excel("等权组合年化收益率.xls")
#df_rt2.to_excel("总市值加权.xls")
#df_rt3.to_excel("流通市值加权.xls")
#test=cal_riskrt("rank60D5threshold0.1_new.csv",5)
#test.to_csv("ratio.csv")
#df_rt1.to_csv("mdd_1.csv")
#df_rt2.to_csv("mdd_2.csv")
#df_rt3.to_csv("mdd_3.csv")

df_rt1.to_csv("win_1.csv")
df_rt2.to_csv("win_2.csv")
df_rt3.to_csv("win_3.csv")



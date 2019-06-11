import pandas as pd
import numpy as np
import math

#读入市值
mkt_value=pd.read_csv("mkt_value.csv")
mkt_value=mkt_value.rename(columns={'trade_dt':'trade_date'})
total_value=mkt_value.pivot(index='trade_date',columns='stcode',values='mkt_value')
flow_value=mkt_value.pivot(index='trade_date',columns='stcode',values='flow_mkt_value')
#处理日期形式
total_value.index=pd.to_datetime(total_value.index,format='%Y%m%d')
total_value.index=total_value.index.strftime("%Y-%m-%d")
flow_value.index=pd.to_datetime(flow_value.index,format='%Y%m%d')
flow_value.index=flow_value.index.strftime("%Y-%m-%d")

total_value=total_value.stack().reset_index()
flow_value=flow_value.stack().reset_index()
total_value=total_value.rename(columns={'level_0':'trade_date',0:'mkt_value'})
flow_value=flow_value.rename(columns={'level_0':'trade_date',0:'flow_mkt_value'})
#循环
for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [0.1]:
            # 读入收益率信息
            rt = pd.read_csv("rt_" + str(D) + ".csv", index_col=0)
            rt = rt.stack().reset_index()
            rt = rt.rename(columns={'level_0': 'trade_date', 'level_1': 'stcode', 0: 'rt'})
            rt['rt'][rt['rt'] > 0.1] = 0.1
            rt['rt'][rt['rt'] < -0.1] = -0.1
            position = pd.read_csv("rank" + str(rank) + "D" + str(D) + "threshold" + str(threshold) + "_position.csv",
                                   index_col=0)
            ##计算费率
            position_fill = position.fillna(0)
            position_abs = (position_fill - position_fill.shift(1)).abs()
            position_sum = position_abs.sum(axis=1)
            positon_len = position.apply(lambda x: len(x.dropna()), axis=1)
            # 计算换手率
            turnover = position_sum / positon_len
            # 计算费率
            cost = turnover * 0.001
            cost[cost == float('inf')] = 0
            # 费率同样前置
            cost = cost.shift(-1)
            cost = pd.DataFrame(cost)
            cost = cost.rename(columns={0: 'cost'})

            ##计算三种组合下的收益率
            # 首先把 个股收益率、持仓、市值、成本合并
            position = position.stack().reset_index()
            position = position.rename(columns={'level_1': 'stcode', 0: 'position'})
            df_combined = position.merge(total_value, left_on=['trade_date', 'stcode'],
                                         right_on=['trade_date', 'stcode'], how='inner')
            df_combined = df_combined.merge(flow_value, left_on=['trade_date', 'stcode'],
                                            right_on=['trade_date', 'stcode'], how='inner')
            df_combined = df_combined.merge(rt, left_on=['trade_date', 'stcode'], right_on=['trade_date', 'stcode'],
                                            how='inner')

            df_combined['rt1'] = df_combined['position'] * df_combined['rt']
            # rt2 为市值加权组合的中间变量
            df_combined['rt2'] = df_combined['position'] * df_combined['rt'] * df_combined['mkt_value']
            # rt3 为流通市值加权组合的中间变量
            df_combined['rt3'] = df_combined['position'] * df_combined['rt'] * df_combined['flow_mkt_value']


            # 等权组合收益率时间序列
            ##两个市值加权组合 建立函数 计算组合收益率
            def cal_rt2(df):
                return df['rt2'].sum(min_count=1) / df['mkt_value'].sum(min_count=1)


            def cal_rt3(df):
                return df['rt3'].sum(min_count=1) / df['flow_mkt_value'].sum(min_count=1)


            rt1 = pd.DataFrame(df_combined.groupby('trade_date')['rt1'].mean())
            rt2 = pd.DataFrame(df_combined.groupby('trade_date')['mkt_value', 'rt2'].apply(cal_rt2))
            rt3 = pd.DataFrame(df_combined.groupby('trade_date')['flow_mkt_value', 'rt3'].apply(cal_rt3))
            rt_df = rt1.join(rt2, how='outer', rsuffix='rt2')
            rt_df = rt_df.join(rt3, how='outer', rsuffix='rt3')
            rt_df = rt_df.rename(columns={'0': 'rt2', '0rt3': 'rt3'})
            rt_df = rt_df.join(cost, how='left')

            rt_df['rt1'] = rt_df['rt1'] - rt_df['cost']
            rt_df['rt2'] = rt_df['rt2'] - rt_df['cost']
            rt_df['rt3'] = rt_df['rt3'] - rt_df['cost']
            rt_df = rt_df.drop(columns='cost')
            rt_df = rt_df.reset_index()
            rt_df.to_csv("rank" + str(rank) + "D" + str(D) + "threshold" + str(threshold) + "_new.csv", index=None)


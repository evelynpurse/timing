import pandas as pd
import numpy as np
benchmark=pd.read_csv("中证500.csv")
rt=pd.read_csv("rank60D5threshold0.1_new.csv")
benchmark=benchmark.rename(columns={'Unnamed: 0':'trade_date'})
df_combined=rt.merge(benchmark[['trade_date','daily_rt']],left_on='trade_date',right_on='trade_date',how='left')
df_combined.to_excel("画图.xls")
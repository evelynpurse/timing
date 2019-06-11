import pandas as pd
import  numpy as np
iterables=[['rank60','rank120','rank250'],['D5','D10','D20','D40']]
index=pd.MultiIndex.from_product(iterables, names=['ranking', 'holding_period'])
df=pd.DataFrame(index=index,columns=[-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1])
for rank in [60,120,250]:
    for D in [5,10,20,40]:
        for threshold in [-0.1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,0.1]:
            position=pd.read_csv("rank"+str(rank)+"D"+str(D)+"threshold"+str(threshold)+"_position.csv",index_col=0)
            df.loc[('rank'+str(rank),'D'+str(D)),threshold]=position.sum(axis=1).mean()
df.to_csv("平均持仓.csv")
import datetime
from jqdatasdk import *
import pandas as pd
auth("18274054038",'054038')
print(datetime.date(2021,2,2))


pd.set_option('display.max_columns',None)
'''计算贵州茅台的最新市值'''
q = query(valuation).filter(valuation.code == "600519.XSHG")
df = get_fundamentals(q,'2021-4-8')
print(df)

#获取总股本,以及总市值
gzmt_total_num = df['capitalization'][0]
gzmt_market_val = df['market_cap']
print("总股本:",gzmt_total_num,"\n\n")

#获取收盘价
gzmt_close = get_price("600519.XSHG",start_date = '2021-04-08', end_date = '2021-04-08',fields=['close'])['close'][0]
print("收盘价:",gzmt_close,"\n\n")

#计算总市值
total_val = gzmt_total_num*gzmt_close
print("计算所得总市值:",total_val,"\n\n")
print("实际总市值:",gzmt_market_val,"\n\n")

#







# stoc_num = df['capitalization']
# # stoc_total_m = df['market_cap']
# ret = get_fundamentals(df, statDate='2020')
# print(ret)


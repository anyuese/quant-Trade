import strategy.ma_strategy as ma
import data.stock as st
# 参数2：周期参数
params = [5,10,20,60,120,250]

stocks = ['000001.XSHE']
data = st.get_csv_price('000001.XSHE','price',start_date='2016-01-01',end_date='2021-01-01')
# 匹配并计算不同的周期参数对：5-10,5-20...

for short in params:
    for long in params:
        if long > short:
            print('==========当前周期参数==========', short, long)
            ma.ma_strategy(data, short_window=short, long_window=long)

#
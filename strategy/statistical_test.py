# import strategy.ma_strategy as ma
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import data.stock as st
import ma_strategy as ma


def ttest(data_return):
    '''
    对策略收益进行t检验
    :param strat_return: dataframe 单次收益率
    :return: float,t值和p值
    '''
    # 调用假设检验ttest函数：scipy
    t, p_value = stats.ttest_1samp(data_return, 0, nan_policy='omit')

    # 判断是否与理论均值有显著性差异 α=0.05
    p_value = p_value / 2  # 获取单边p值
    print('t_value', t)
    print('p_value', p_value)
    print('是否拒绝H0：收益均值=0：', p_value < 0.05)
    return t, p_value


if __name__ == '__main__':
    # code = '000001.XSHE'
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    cum_profits = pd.DataFrame()
    for code in stocks:
        df = st.get_single_stock_price(code, 'daily', '2016-12-01', '2021-01-01')
        df = ma.ma_strategy(df)
        returns = df['profit_pct']
        ttest(returns)


    # 策略的单次收益率

    # 绘制一下分布图

    # 调用假设检验ttest函数 ： scipy

    # 获取t, p

    # 判断是否与理论均值有显著性差异

    # 对多个股票进行计算，测试

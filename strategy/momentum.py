import data.stock as st
import pandas as pd
import base

pd.set_option('display.max_columns', None)
import numpy as np
import matplotlib.pyplot as plt


def get_data(start_date, end_date, columns, index_symbol='000300.XSHG', ):
    '''
    获取股票收盘价数据,并拼接为一个df
    :param start_date:
    :param end_date:
    :param columns:
    :param index_symbol:
    :return:
    '''
    # 获取股票代码列表
    stocks = st.get_index_list(index_symbol)
    # 拼接数据容器
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_price(code, start_date=start_date, end_date=end_date, columns=columns)
        print('========股票数据', code)
        # print(data.tail())
        data.columns = [code]
        # 拼接多个股票的收盘价: 日期 股票A收盘价 股票B收盘价
        data_concat = pd.concat([data_concat, data], axis=1)
        # 生成交易的信号 根据收益率进行排行
    return data_concat


def momentum(data_concat, top_n, shift_n=1):
    '''

    :param data_concat:
    :param shift_n: 业绩统计周期,单位:月
    :return:
    '''
    # 转换时间频率:日->月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('M').last()
    # 计算过去N个月的收益率 = 期末值/期初值 -1
    # 对数收益率:log(期末值/期初值)
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return.head())
    # print(shift_return.shift(-1))

    # 生成交易信号
    buy_signal = get_top_stocks(shift_return, top_n)
    sell_signal = get_top_stocks(shift_return * -1, top_n)
    signal = buy_signal - sell_signal
    print(signal.head())

    # 计算投资组合收益率
    returns = base.caculate_portfolio_return(shift_return, signal, top_n * 2)
    print(returns.head())

    # 评估
    base.evaluate_strategy(returns)
    return returns

def get_top_stocks(data, top_n):
    '''
    找到前n位的极值,并转换位信号返回
    :param data:
    :param top_n:
    :return:
    '''
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # 对data的每一行进行遍历,找到里面的最大值,并利用bool函数标注0和1信号
    for index, row in data.iterrows():
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int32)
    return signals


if __name__ == '__main__':
    data = get_data('2016-01-01', '2021-04-04', ['date', 'close'])
    returns = momentum(data, 2)
    returns.to_csv('./momentum_return.csv')
    returns['cum_prof'].plot()
    plt.show()

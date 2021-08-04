import numpy as np
import pandas as pd

import data.stock as st

pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)

def evaluate_strategy(data):
    '''
    评估策略收益表现
    :param data:
    :return:
    '''
    # 评估策略效果:总收益率
    print(data)
    data = caculate_cum_prof(data)
    # 获取总收益率
    total_return = data['cum_prof'].iloc[-1]
    # 获取年化收益率(每月开仓)
    annualized_return = data['profit_pct'].mean() * 12
    # 计算一年的最大回撤
    data = caculate_max_drawdown(data,12)
    print(data)
    # 获取一年的最大回撤
    max_drawndown = data['max_dd'].iloc[-1]
    # 计算夏普比率: 每日收益率 * 252 = 每年收益率
    sharp, annual_sharp = caculate_sharpe(data)

    # 放到dict中
    results = {'总收益率':total_return, '年化收益率':annualized_return,
               '最大回撤':max_drawndown,'夏普比率':annual_sharp}
    # 打印评估指标数据
    for key,value in results.items():
        print(key,value)

    return data





def compose_signal(data):
    '''

    :param data:
    :return:
    '''
    # 整合信号
    data.loc[:,'buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data.loc[:,'sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data.loc[:,'signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_prof_pct(data):
    '''

    :param data:
    :return:
    '''
    data.loc[data['signal'] != 0, 'profit_pct'] = data.loc[data['signal'] != 0,'close'].pct_change()
    data = data[data['signal'] == -1]
    return data


def week_period_strategy(code, start_date, end_date,time_freq='daily'):
    """

    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    """
    data = st.get_single_stock_price(code, time_freque=time_freq, start_date=start_date, end_date=end_date)
    # 新建周期字段
    data.loc[:,'weekday'] = data.index.weekday

    # 周四买入
    data.loc[:,'buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data.loc[:,'sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 模拟错误的连续买入，卖出
    # data['buy_signal'] = np.where(((data['weekday'] == 3) | (data['weekday'] == 4)), 1, 0)
    # data['sell_signal'] = np.where((data['weekday'] == 0) | ((data['weekday']) == 1), -1, 0)

    data = compose_signal(data)  # 整合信号
    data = calculate_prof_pct(data)  # 计算收益率
    data2 = calculate_prof_pct_(data)
    data = caculate_cum_prof(data)  # 计算累积收益率
    # data = caculate_max_drawdown(data, None)
    return data


def calculate_prof_pct_(data):
    '''

    :param data:
    :return:
    '''
    data = data[data['signal'] != 0]
    data.loc[:, 'profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]
    return data

def caculate_portfolio_return(data, signal, n):

    returns = data.copy()
    # 投组收益率(等权重) = 收益率之和 / 股票个数
    returns.loc[:,'profit_pct'] = (signal * returns.shift(-1)).T.sum() / n
    returns = caculate_cum_prof(returns)
    return returns.shift(1)




def caculate_cum_prof(data):
    '''

    :param data:
    :return:
    '''
    data.loc[:,'cum_prof'] = (1 + data['profit_pct']).cumprod() - 1
    return data


def caculate_max_drawdown(data, windows=252):
    '''

    :param data:
    :param windows:
    :return:
    '''
    # 选取时间周期（时间窗口）

    # 选取时间周期中的最大净值
    data['close'] = (data['cum_prof'] +1) * 10000
    data.loc[:,'roll_max'] = data['close'].rolling(window=windows, min_periods=1).max()
    # 计算当天回撤比：（峰值 - 谷值）/ 峰值 = 谷值/峰值 -1
    data.loc[:,'daily_dd'] = 1 - data['close'] / data['roll_max']
    # 选取时间周期内的最大的回撤比，即最大回撤
    data.loc[:,'max_dd'] = data['daily_dd'].rolling(windows, min_periods=1).max()

    return data


def caculate_sharpe(data):
    """

    :param data:
    :return:
    """
    # 公式: sharpe = （回报率的均值 - 无风险利率）/回报率的标准差
    # 因子项
    # daily_return = data['close'].pct_change()
    daily_return = data['profit_pct']
    avg_return = daily_return.mean()
    sd_return = pd.DataFrame(daily_return).std()
    # 计算夏普比率 : 每日收益率 * 252 = 每年收益率
    sharpe = float(avg_return / sd_return)
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


if __name__ == '__main__':
    code = '000001.XSHE'
    data = week_period_strategy(code,time_freq='daily', start_date='2016-04-01',end_date= '2021-04-01')
    data1 = calculate_prof_pct_(data)
    data2 = calculate_prof_pct(data1)
    data1.loc[:,'profit_pct2'] = data2['profit_pct']
    print(data1)


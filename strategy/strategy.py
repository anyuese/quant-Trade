import data.stock as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)


def compose_signal(data):
    '''

    :param data:
    :return:
    '''
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_prof_pct(data):
    '''

    :param data:
    :return:
    '''
    data = data[data['signal'] != 0]                # 筛选
    data['profit_pct'] = data['close'].pct_change
    data = data[data['signal'] == -1]
    return data


def caculate_cum_prof(data):
    '''

    :param data:
    :return:
    '''
    data['cum_prof'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def week_period_strategy(code, time_freq, start_date, end_date):
    """

    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    """
    data = st.get_single_stock_price(code, time_freque=time_freq, start_date=start_date, end_date=end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday

    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 模拟错误的连续买入，卖出
    # data['buy_signal'] = np.where(((data['weekday'] == 3) | (data['weekday'] == 4)), 1, 0)
    # data['sell_signal'] = np.where((data['weekday'] == 0) | ((data['weekday']) == 1), -1, 0)

    data = compose_signal(data)  # 整合信号
    data = calculate_prof_pct(data)  # 计算收益率
    data = caculate_cum_prof(data)  # 计算累积收益率
    # data = caculate_max_drawdown(data, None)
    return data


def caculate_max_drawdown(data, windows):
    '''

    :param data:
    :param windows:
    :return:
    '''
    # 选取时间周期（时间窗口）
    if windows is None:
        windows = 252

    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=windows, min_periods=1).max()
    # 计算当天回撤比：（峰值 - 谷值）/ 峰值 = 谷值/峰值 -1
    data['daily_dd'] = 1 - data['close'] / data['roll_max']
    # 选取时间周期内的最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(windows, min_periods=1).max()

    return data


def caculate_sharpe(data):
    """

    :param data:
    :return:
    """
    # 公式: sharpe = （回报率的均值 - 无风险利率）/回报率的标准差
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = pd.DataFrame(daily_return).std()
    # 计算夏普比率 : 每日收益率 * 252 = 每年收益率
    sharpe =float(avg_return / sd_return)
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


if __name__ == '__main__':
    # df = week_period_strategy('000001.XSHE', 'daily', start_date=None, end_date='2020-03-01')
    # print(df[['close', 'signal', 'profit_pct','cum_prof']])
    # print(df.describe())
    # df['profit_pct'].plot()
    # plt.show()

    # df = st.get_single_stock_price('000001.XSHE', start_date='2006-01-01', end_date='2021-01-01', time_freque='daily')
    # df = caculate_max_drawdown(df, windows=252)
    # print(df.loc[:, ['close', 'roll_max', 'daily_dd', 'max_dd']])
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    # 计算夏普比率
    df = st.get_single_stock_price('000001.XSHE', start_date='2006-01-01', end_date='2021-01-01', time_freque='daily')
    sharpe = caculate_sharpe(df)
    print(sharpe)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base as strat
import data.stock as st

pd.set_option("display.max_columns", None)


def ma_strategy(data, short_window=3, long_window=10):
    '''

    :param data:
    :param short_window:
    :param long_window:
    :return:
    '''
    # 计算技术指标：ma短期,ma长期
    data.loc[:,'short_ma'] = data['close'].rolling(window=short_window).mean()
    data.loc[:,'long_ma'] = data['close'].rolling(window=long_window).mean()

    # 生成信号：金叉买入，死叉卖出
    data.loc[:,'buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data.loc[:,'sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    # 整合信号
    data = strat.compose_signal(data)

    # 计算单次收益，计算累积收益
    data = strat.calculate_prof_pct(data)
    data = strat.caculate_cum_prof(data)
    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1,inplace=True)
    return data


if __name__ == '__main__':
    stocks = ['002418.XSHE']
    cum_profits = pd.DataFrame()
    for code in stocks:
        df = st.get_single_stock_price(code, 'daily', '2021-01-01', '2021-07-24')
        df = ma_strategy(df)                
        cum_profits.loc[:,code] = df['cum_prof'].reset_index(drop=True)
        df['cum_prof'].plot(label=code)
        print('开仓次数：', int(len(df) / 2))

    plt.legend()
    plt.show()
    print(cum_profits)

    # df = strat.caculate_max_drawdown(df, 252)
    # df = df[df['signal'] != 0]
    #
    # print('开仓次数：',int(len(df)/2))
    # print(df[['close', 'profit_pct', 'cum_prof','max_dd']])

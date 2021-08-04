import datetime
import sys
import time
import os
import pandas as pd
from jqdatasdk import *

auth("18274054038", "054038")

# 全局变量
root = "./"


def get_stock_list():
    """
    :return:
    """
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_index_list(index_symbol='000300.XSHG'):
    '''

    :param index_symbol:
    :return:
    '''
    stocks = get_index_stocks(index_symbol)
    return stocks


def get_single_stock_price(code, time_freque='daily', start_date='2021-01-01', end_date=None) -> object:
    """

    :param code:
    :param start_date:
    :param end_date:
    :param time_freque:
    :return:is
    """
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freque)
    return data


def export_data(data, filename, type='price', mode=None):
    """
    :param data:
    :param filename:
    :param type:
    :return:
    """
    file_root = root + type + filename + '.csv'
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)
        data.drop_duplicates(subset=['date'], inplace=True)
        data.set_index('date', inplace=True)
        data.to_csv(file_root)  # 重新写入
        print('已成功添加至', file_root)
    else:
        data.to_csv(file_root)
        print(data)
        print("已成功储存至", file_root)


def transfer_price_freq(data, time_freq):
    """

    :param data:
    :param time_freq:
    :return:
    """
    df_trans = pd.DataFrame()
    df_trans.loc[:,'open'] = data['open'].resample(time_freq).first()
    df_trans.loc[:,'close'] = data['close'].resample(time_freq).last()
    df_trans.loc[:,'max'] = data['high'].resample(time_freq).max()
    df_trans.loc[:,'min'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finace(code, date, stateDate):
    '''

    :param code:
    :param date:
    :param stateDate:
    :return:
    '''
    data = get_fundamentals(query(indicator).filter(indicator.code == code),
                            date=date, statDate=stateDate)
    return data


def get_single_valuation(code, date, statDate):
    '''

    :param code:
    :param date:
    :param statDate:
    :return:
    '''
    data = get_fundamentals(query(valuation).filter(valuation.code == code),
                            statDate=statDate, date=date)
    return data


def get_csv_data(code, type):
    '''

    :param code:
    :param type:
    :return:
    '''
    file_root = root + type + code + '.csv'
    return pd.read_csv(file_root)


def calculate_change_pct(data):
    '''

    :param data: dataframe
    :return: dataframe
    '''
    data.loc[:,'close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data


def update_daily_price(stock_code, type='price'):
    '''
    :param stock_code:
    :param type:
    :return:
    '''
    file_root = root + type + stock_code + '.csv'
    if os.path.exists(file_root):
        start_date = pd.read_csv(file_root, usecols=['date']).iloc[-1]
        start_date = list(start_date)[0]
        df = get_single_stock_price(code=stock_code, time_freque='daily', start_date=start_date)
        df.index.names = ['date']
        export_data(df, filename=stock_code, type='price', mode='a')
    else:
        df = get_single_stock_price(code=stock_code, time_freque='daily')
        export_data(data=df, filename=stock_code, type='price')


def init_db():
    '''
    初始化数据库
    :return:
    '''
    stocks = get_stock_list()
    for code in stocks:
        df = get_single_stock_price(code, 'daily')
        export_data(data=df, filename=code, type='price')


def get_csv_price(code, start_date, end_date, type='price',columns=None):
    '''

    :param code:
    :param type:
    :param start_date:
    :param end_date:
    :return:
    '''
    # 使用update直接更新数据
    update_daily_price(code)
    # 读取数据库对应的股票csv文件
    file_root = root + type + code + '.csv'
    # 如果有,直接获取
    if columns is None:
        data = pd.read_csv(file_root, index_col='date')
    else:
        data = pd.read_csv(file_root,usecols=columns, index_col='date')
    df = data[(data.index >= start_date) & (data.index <= end_date)]
    return data[(data.index >= start_date) & (data.index <= end_date)]


# # 获取A股所有行情数据
# stocks = list(get_all_securities(['stock']).index)
# # print(stocks)
#
# # 如何获取股票行情数据
# # for stock_code in stocks:
# #     print("正在获取股票行情数据.....")
# #     df = get_price(stock_code,end_date= "2021-04-09",count=10,
# #                    frequency = 'daily')
# #     time.sleep(10)
# #     print(df)
#
# '''resample函数的使用'''
#
# # 转换周期:转换日K为周K
# df = get_price("000001.XSHG", count=100, end_date='2021-04-09',
#                frequency='daily')
# df['weekday'] = df.index.weekday
#
# # 获取周K(当周的):开盘价(当周第一天),收盘价(当周最后一天),最高价(当周),最低价(当周)
# df_week = pd.DataFrame()
# df_week['open'] = df['open'].resample("W").first()
# df_week['close'] = df['close'].resample("W").first()
# df_week['max'] = df['high'].resample("W").first()
# df_week['min'] = df['low'].resample("W").first()
#
# # 汇总统计: 获取当周的成交总额,成交总金额
# df_week['volume(sum)'] = df['volume'].resample('W').sum()
# df_week['money(sum)'] = df['money'].resample('W').sum()
# print(df_week)
#
# '''获取股票财务数据指标'''
# df = get_fundamentals(query(indicator), statDate="2020")
# df.to_csv("./finace2020.csv")
#
# '''基于盈利指标选股:eps,operating_profit,roe,inc_net_profit_year_on_year'''
# df = df[(df["eps"] > 0) & (df["roe"] > 10 & (df['inc_net_profit_year_on_year'] > 10))]
# df.index = df['code']
# print(df)
#
# '''获取股票估值数据指标'''
# df_valuation = get_fundamentals(query(valuation), statDate=datetime.datetime.today())
# df_valuation.index = df_valuation['code']
# df['pe_ratio'] = df_valuation['pe_ratio']
# df = df[df['pe_ratio'] < 50]
# print("拼凑的来的", df)

# 获取沪深300指数成分股

print(get_index_list())

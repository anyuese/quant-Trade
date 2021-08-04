import data.stock as st

# 获取平安银行的行情数据（日K）
# data = st.get_single_stock_price("000001.XSHE", start_date="2021-01-01", end_date='2021-03-01', time_freque="daily")
#
# st.export_data(data, '000001.XSHE', 'price')
# # 存取数据
#
# # 计算涨跌幅
# data = st.calculate_change_pct(data)
# print(data)
#
# # 获取周K
# data = st.transfer_price_freq(data,"W")
st.init_db()
# 计算周K的涨跌幅
# st.update_daily_price('000001.XSHE', type='price')
# print(data)



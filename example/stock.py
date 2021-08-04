import data.stock as st
import jqdatasdk as jq

#初始化变量
# code = "000001.XSHE"
#
#
# #调用一支股票行情数据
# data = st.get_csv_price(code, 'price', "2021-01-01", "2021-04-12")
# print(data)
jq.logout()
jq.auth('18274054038','054038')
st.init_db()
# #存入csv
# st.export_data(data,code,"price")
#
# #从csv中获取数据
# data = st.get_csv_data(code,"price")
# print(data)

#实时更新数据：假设每天更新日K数据 > 存到csv文件

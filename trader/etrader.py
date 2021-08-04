import easytrader


user = easytrader.use('universal_client')
user.enable_type_keys_for_editor()
user.connect(r'F:\Download\同花顺\xiadan.exe')


# 获取资金明细
# balance = user.balance
# print(balance)
#
# # 获取持仓
# position = user.position
# print(position)
#
# # 查询当日成交
# today_trades = user.today_trades
# print(today_trades)
#
# # 查询当日委托
# today_entrusts = user.today_entrusts
# print(today_entrusts)
#
# buy_no = user.buy('000002',price=0,amount=100)
# print(buy_no)
#
# sell_no = user.sell('000001',price=0,amount=100)
# print(sell_no)

# 撤单
cancel = user.cancel_entrust('2094102408')
print(cancel)

# 撤单：全部撤单
cancel = user.cancel_all_entrusts()
print(cancel)
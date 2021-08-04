import data.stock as st
import strategy.base as stb
import pandas as pd
from matplotlib import pyplot as plt

# 获取3只股票的数据：比亚迪，宁德时代，隆基

codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
sharpes = []
for code in codes:
    data = st.get_single_stock_price(code=code, time_freque='daily',start_date='2018-10-01', end_date='2021-01-01')
    print(data.head())
    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.caculate_sharpe(data)
    sharpes.append([code, annual_sharpe])  # 存放[[c1,s1],[c2,s2],[c3.s3]]

# 可视化3只股票进行比较
print(sharpes)
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpes']).set_index('code')
print(sharpes)

# 绘制bar图
sharpes.plot.bar()
plt.xticks(rotation = 30)
plt.show()

import baostock as bs
import pandas as pd
import BaseTool as tool
from PointQueue import PointQueue

DATE = 0
CODE = 1
OPEN = 2
HIGH = 3
LOW = 4
CLOSE = 5
PRECLOSE = 6
VOLUME = 7
AMOUNT = 8
ADJUST_FLAG = 9
TURN = 10
TRADE_STATUS = 11
PCT_CHG = 12
PE_TTM = 13
PB_MRQ = 14
PS_TTM = 15
PCF_NCF_TTM = 16
IS_ST = 17

# STOCK = 'sh.601012'
# STOCK = 'sz.002230'
STOCK = 'sz.002415'

# 快慢均线
speed = 10
slow = 30

# === 登陆系统 ===#
lg = bs.login()

# === 获取沪深A股历史K线数据 ===#
rs = bs.query_history_k_data_plus(STOCK,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,"
                                  "pctChg,isST",
                                  start_date='2017-05-08', end_date='2020-05-08',
                                  frequency="d", adjustflag="2")

data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())

# 数据长度
len_list = len(data_list)

# 计算快慢线，起始日期与慢线保持一致（因为慢线能统计的天数更少）
# 快线
maSp = tool.avg_line(speed, *data_list)
# 慢线
maSl = tool.avg_line(slow, *data_list)

# 总共统计天数，以慢线为准，因为慢线统计天数更少
sl_len = len(maSl) - 1
sp_len = len(maSp) - 1

# ****************************************************寻找交易点**********************************************************
buy = PointQueue()
sell = PointQueue()
# 计算快慢均线偏移量
offset_avg = 0
offset_day = 0
for sp in maSp:
    if tool.compare_time(sp.date, maSl[0].date) < 0:
        offset_avg += 1

for day in data_list:
    if tool.compare_time(day[DATE], maSl[0].date) < 0:
        offset_day += 1

for k in range(0, sl_len):
    sp = k + offset_avg
    day = k + offset_day
    # 快线上穿慢线，买点
    if maSp[sp - 1].val < maSl[k - 1].val and maSp[sp].val >= maSl[k].val:
        buy.enQueue(data_list[day], data_list[day][DATE])
    # 快线下穿慢线，卖点
    elif maSp[sp - 1].val >= maSl[k - 1].val and maSp[sp].val < maSl[k].val:
        sell.enQueue(data_list[day], data_list[day][DATE])
# ****************************************************寻找交易点**********************************************************


# ******************************************************统计*************************************************************
# 本次建仓成本
cost = 0
# 总盈利情况
total = 0
while buy.length > 0 and sell.length > 0:
    # 开始建仓，卖点出现前的买点全部用来建仓
    if tool.compare_time(buy.first().data[DATE], sell.first().data[DATE]) < 0:
        cost += float(buy.deQueue().data[CLOSE])
    # 清仓
    else:
        # cost为0的时候表示收集到的第一个卖点之前，还未建仓，因此该卖点直接出队即可
        if cost == 0:
            sell.deQueue()
        else:
            sell_data = sell.deQueue().data
            profit = float(sell_data[CLOSE]) - cost
            total += profit / cost
            cost = 0
            print('此次盈利情况：', round(profit, 2), '清仓日期', sell_data[DATE])

print('总盈利情况', round(total, 2), '%')
# *******************************************************统计************************************************************


result = pd.DataFrame(data_list, columns=rs.fields)

# 结果集输出到csv文件 #
# result.to_csv("C:\\AppData\stockData\601012.csv", index=False)
# 登出系统 #
bs.logout()

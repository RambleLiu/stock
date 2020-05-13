import datetime

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


# 均线元素
class Avg:
    val = None
    date = None


# 计算均线
# start:开始日期        ma：均线天数     list:k线数组
def avg_line(ma, *dataList):
    list_len = len(dataList)
    avg_list = []
    for start in range(ma - 1, list_len):
        count = 0
        # 统计ma天内的平均值
        for offset in range(0, ma):
            count += float(dataList[start - offset][CLOSE])
        avg = Avg()
        avg.val = round(count / ma, 2)
        avg.date = dataList[start][DATE]
        avg_list.append(avg)
    return avg_list


# 计算time1和time2的日期之差
def compare_time(time1, time2):
    date1 = time1.split('-')
    date2 = time2.split('-')
    d1 = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]))
    d2 = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]))
    return (d1 - d2).days

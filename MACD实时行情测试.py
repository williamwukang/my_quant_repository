import talib

para_dict=dict()
symbol_list=[
    "SHFE|Z|RB|MAIN","SHFE|Z|AG|MAIN","SHFE|Z|FU|MAIN","SHFE|Z|BU|MAIN","SHFE|Z|SP|MAIN",
    "ZCE|Z|MA|MAIN","ZCE|Z|SR|MAIN","ZCE|Z|TA|MAIN","ZCE|Z|CF|MAIN","ZCE|Z|UR|MAIN","ZCE|Z|RM|MAIN",
    "DCE|Z|M|MAIN","DCE|Z|I|MAIN","DCE|Z|P|MAIN","DCE|Z|C|MAIN","DCE|Z|PP|MAIN",
]
for symbol in symbol_list:
    para_dict[symbol]={
        "golden_long":0,
        "generate_low_long":0,
        "diff_his_low_long":0,
        "bar_his_low_long":0,
        "low_price_long":0,
        "wait_break_low_long":0,
        "dead_long":0,
        "generate_top_long":0,
        "diff_his_top_long":0,
        "bar_his_top_long":0,
        "top_price_long":0,
        "wait_break_top_long":0,
        "golden_mid":0,
        "generate_low_mid":0,
        "diff_his_low_mid":0,
        "bar_his_low_mid":0,
        "low_price_mid":0,
        "wait_break_low_mid":0,
        "dead_mid":0,
        "generate_top_mid":0,
        "diff_his_top_mid":0,
        "bar_his_top_mid":0,
        "top_price_mid":0,
        "wait_break_top_mid":0,
        "golden_short":0,
        "diff_his_low_short":0,
        "low_price_short":0,
        "dead_short":0,
        "diff_his_top_short":0,
        "top_price_short":0,
    }

# 策略参数字典
def macd_long(symbol,bartype,barinterval):     
    if CurrentBar(symbol,bartype,barinterval)<26:
       return
    diff_long,dea_long,bar_long=talib.MACD(Close(symbol,bartype,barinterval))
    if diff_long[-2]<=dea_long[-2] and diff_long[-1]>dea_long[-1]:
        para_dict[symbol]["golden_long"]=1  
        if para_dict[symbol]["generate_low_long"]==0 and para_dict[symbol]["dead_long"]>0: 
            para_dict[symbol]["diff_his_low_long"]=min(diff_long[-para_dict[symbol]["dead_long"]:])    #记录从第一根绿柱到第一根红柱范围内的diff最小值
            para_dict[symbol]["bar_his_low_long"]=min(bar_long[-para_dict[symbol]["dead_long"]:])    #记录从第一根绿柱到第一根红柱范围内的macd最小值
            para_dict[symbol]["low_price_long"]=min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_long"]:])   ##记录从第一根绿柱到第一根红柱范围内的价格最小值
            para_dict[symbol]["generate_low_long"]=1  #标记为第一个底
        elif para_dict[symbol]["generate_low_long"]==1 and para_dict[symbol]["low_price_long"]>min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_long"]:]):   
            para_dict[symbol]["diff_his_low_long"]=min(diff_long[-para_dict[symbol]["dead_long"]:])
            para_dict[symbol]["bar_his_low_long"]=min(bar_long[-para_dict[symbol]["dead_long"]:])
            para_dict[symbol]["low_price_long"]=min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_long"]:])
            para_dict[symbol]["wait_break_low_long"]=1    #两个底不断降低，确认下降趋势，下次破新低判断是否存在潜在底
            para_dict[symbol]["generate_top_long"]=0  #下降趋势确认，顶部数量清零
            para_dict[symbol]["wait_break_top_long"]=0
    elif diff_long[-2]>=dea_long[-2] and diff_long[-1]<dea_long[-1]:
        para_dict[symbol]["dead_long"]=1
        if para_dict[symbol]["generate_top_long"]==0 and para_dict[symbol]["golden_long"]>0:
            para_dict[symbol]["diff_his_top_long"]=max(diff_long[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["bar_his_top_long"]=max(bar_long[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["top_price_long"]=max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["generate_top_long"]=1
        elif para_dict[symbol]["generate_top_long"]==1 and para_dict[symbol]["top_price_long"]<max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_long"]:]):
            para_dict[symbol]["diff_his_top_long"]=max(diff_long[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["bar_his_top_long"]=max(bar_long[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["top_price_long"]=max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_long"]:])
            para_dict[symbol]["generate_low_long"]=0
            para_dict[symbol]["wait_break_top_long"]=1
            para_dict[symbol]["wait_break_low_long"]=0     
    if para_dict[symbol]["golden_long"]>0:
        para_dict[symbol]["golden_long"]=para_dict[symbol]["golden_long"]+1
    if para_dict[symbol]["dead_long"]>0:
        para_dict[symbol]["dead_long"]=para_dict[symbol]["dead_long"]+1
def macd_long_last(symbol,bartype,barinterval):
    if CurrentBar(symbol,bartype,barinterval)<26:
       return
    diff_long,dea_long,bar_long=talib.MACD(Close(symbol,bartype,barinterval))
    if para_dict[symbol]["wait_break_top_long"]==1 and Q_Last(symbol)>para_dict[symbol]["top_price_long"]:
        if max(diff_long[-para_dict[symbol]["dead_long"]:])<para_dict[symbol]["diff_his_top_long"] or max(bar_long[-para_dict[symbol]["dead_long"]:])<para_dict[symbol]["bar_his_top_long"]:
            para_dict[symbol]["wait_break_top_long"]=2
    elif para_dict[symbol]["wait_break_top_long"]==2 and diff_long[-1]>=para_dict[symbol]["diff_his_top_long"] and bar_long[-1]>=para_dict[symbol]["bar_his_top_long"]:
        para_dict[symbol]["wait_break_top_long"]=0
    if para_dict[symbol]["wait_break_low_long"]==1 and Q_Last(symbol)<para_dict[symbol]["low_price_long"]:
        if min(diff_long[-para_dict[symbol]["golden_long"]:])>para_dict[symbol]["diff_his_low_long"] or min(bar_long[-para_dict[symbol]["golden_long"]:])>para_dict[symbol]["bar_his_low_long"]:
            para_dict[symbol]["wait_break_low_long"]=2
    elif para_dict[symbol]["wait_break_low_long"]==2 and diff_long[-1]<=para_dict[symbol]["diff_his_low_long"] and bar_long[-1]<=para_dict[symbol]["bar_his_low_long"]:
        para_dict[symbol]["wait_break_low_long"]=0
def macd_mid(symbol,bartype,barinterval):
    if CurrentBar(symbol,bartype,barinterval)<26:
       return
    diff_mid,dea_mid,bar_mid=talib.MACD(Close(symbol,bartype,barinterval))
    if diff_mid[-2]<=dea_mid[-2] and diff_mid[-1]>dea_mid[-1]:
        para_dict[symbol]["golden_mid"]=1
        if para_dict[symbol]["generate_low_mid"]==0 and para_dict[symbol]["dead_mid"]>0:
            para_dict[symbol]["diff_his_low_mid"]=min(diff_mid[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["bar_his_low_mid"]=min(bar_mid[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["low_price_mid"]=min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["generate_low_mid"]=1
        elif para_dict[symbol]["generate_low_mid"]==1 and para_dict[symbol]["low_price_mid"]>min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_mid"]:]):
            para_dict[symbol]["diff_his_low_mid"]=min(diff_mid[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["bar_his_low_mid"]=min(bar_mid[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["low_price_mid"]=min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_mid"]:])
            para_dict[symbol]["generate_top_mid"]=0
            para_dict[symbol]["wait_break_low_mid"]=1
            para_dict[symbol]["wait_break_top_mid"]=0                  
    elif diff_mid[-2]>=dea_mid[-2] and diff_mid[-1]<dea_mid[-1]:
        para_dict[symbol]["dead_mid"]=1
        if para_dict[symbol]["generate_top_mid"]==0 and para_dict[symbol]["golden_mid"]>0:
            para_dict[symbol]["diff_his_top_mid"]=max(diff_mid[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["bar_his_top_mid"]=max(bar_mid[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["top_price_mid"]=max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["generate_top_mid"]=1
        elif para_dict[symbol]["generate_top_mid"]==1 and para_dict[symbol]["top_price_mid"]<max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_mid"]:]):
            para_dict[symbol]["diff_his_top_mid"]=max(diff_mid[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["bar_his_top_mid"]=max(bar_mid[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["top_price_mid"]=max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_mid"]:])
            para_dict[symbol]["wait_break_top_mid"]=1
            para_dict[symbol]["generate_low_mid"]=0   
            para_dict[symbol]["wait_break_low_mid"]=0     
    if para_dict[symbol]["golden_mid"]>0:
        para_dict[symbol]["golden_mid"]=para_dict[symbol]["golden_mid"]+1
    if para_dict[symbol]["dead_mid"]>0:
        para_dict[symbol]["dead_mid"]=para_dict[symbol]["dead_mid"]+1
def macd_mid_last(symbol,bartype,barinterval):
    if CurrentBar(symbol,bartype,barinterval)<26:
       return
    diff_mid,dea_mid,bar_mid=talib.MACD(Close(symbol,bartype,barinterval))
    if para_dict[symbol]["wait_break_top_mid"]==1 and Q_Last(symbol)>para_dict[symbol]["top_price_mid"]:
        if max(diff_mid[-para_dict[symbol]["dead_mid"]:])<para_dict[symbol]["diff_his_top_mid"] or max(bar_mid[-para_dict[symbol]["dead_mid"]:])<para_dict[symbol]["bar_his_low_mid"]:
            para_dict[symbol]["wait_break_top_mid"]=2
    elif para_dict[symbol]["wait_break_top_mid"]==2 and diff_mid[-1]>=para_dict[symbol]["diff_his_top_mid"] and bar_mid[-1]>=para_dict[symbol]["bar_his_top_mid"]:
        para_dict[symbol]["wait_break_top_mid"]=0
    if para_dict[symbol]["wait_break_low_mid"]==1 and Q_Last(symbol)<para_dict[symbol]["low_price_mid"]:
        if min(diff_mid[-para_dict[symbol]["golden_mid"]:])>para_dict[symbol]["diff_his_low_mid"] or min(bar_mid[-para_dict[symbol]["golden_mid"]:])>para_dict[symbol]["bar_his_low_mid"]:
            para_dict[symbol]["wait_break_low_mid"]=2
    elif para_dict[symbol]["wait_break_low_mid"]==2 and diff_mid[-1]<=para_dict[symbol]["diff_his_low_mid"] and bar_mid[-1]<=para_dict[symbol]["bar_his_low_mid"]:
        para_dict[symbol]["wait_break_low_mid"]=0

def macd_short(symbol,bartype,barinterval):
    if CurrentBar(symbol,bartype,barinterval)<26:
       return
    diff_short,dea_short,bar_short=talib.MACD(Close(symbol,bartype,barinterval))
    if diff_short[-2]<=dea_short[-2] and diff_short[-1]>dea_short[-1]:
        para_dict[symbol]["golden_short"]=1
        if para_dict[symbol]["dead_short"]!=0:
            if para_dict[symbol]["low_price_short"]!=0 and min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_short"]:])<para_dict[symbol]["low_price_short"] and min(diff_short[-para_dict[symbol]["dead_short"]:])>para_dict[symbol]["diff_his_low_short"]:
                if para_dict[symbol]["wait_break_low_long"]==2 and para_dict[symbol]["wait_break_low_mid"]==2:
                    LogInfo(Date(symbol,bartype,barinterval),Time(symbol,bartype,barinterval),f"{symbol,bartype,barinterval}:<买>入建仓")
            para_dict[symbol]["diff_his_low_short"]=min(diff_short[-para_dict[symbol]["dead_short"]:])
            para_dict[symbol]["low_price_short"]=min(Low(symbol,bartype,barinterval)[-para_dict[symbol]["dead_short"]:])
    elif diff_short[-2]>=dea_short[-2] and diff_short[-1]<dea_short[-1]:
        para_dict[symbol]["dead_short"]=1
        if para_dict[symbol]["golden_short"]!=0:
            if para_dict[symbol]["top_price_short"]!=0 and max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_short"]:])>para_dict[symbol]["top_price_short"] and max(diff_short[-para_dict[symbol]["golden_short"]:])<para_dict[symbol]["diff_his_top_short"]:
                if para_dict[symbol]["wait_break_top_long"]==2 and para_dict[symbol]["wait_break_top_mid"]==2:
                    LogInfo(Date(symbol,bartype,barinterval),Time(symbol,bartype,barinterval),f"{symbol,bartype,barinterval}:<卖>出建仓")
            para_dict[symbol]["diff_his_top_short"]=max(diff_short[-para_dict[symbol]["golden_short"]:])
            para_dict[symbol]["top_price_short"]=max(High(symbol,bartype,barinterval)[-para_dict[symbol]["golden_short"]:])
    if para_dict[symbol]["dead_short"]>0:
        para_dict[symbol]["dead_short"]=para_dict[symbol]["dead_short"]+1
    if para_dict[symbol]["golden_short"]>0:
        para_dict[symbol]["golden_short"]=para_dict[symbol]["golden_short"]+1

# 策略开始运行时执行该函数一次
def initialize(context): 
    for symbol in symbol_list:
        SetBarInterval(symbol,"M",60,"20230601",isTrigger=True)
        SetBarInterval(symbol,"M",12,"20230601",isTrigger=True)
        SetBarInterval(symbol,"M",3,"20230601",isTrigger=True)


# 策略触发事件每次触发时都会执行该函数
def handle_data(context):
    global symbol_list
    for symbol in symbol_list:
        if context.contractNo()==symbol:
            if context.kLineSlice()==60:
                macd_long(symbol,"M",60)
            if context.kLineSlice()==12:
                macd_mid(symbol,"M",12)
            if context.kLineSlice()==3:
                macd_short(symbol,"M",3)
            if context.strategyStatus()=="C":
                macd_long_last(symbol,"M",60)
                macd_mid_last(symbol,"M",12)
# 历史回测阶段结束时执行该函数一次
def hisover_callback(context):
    pass


# 策略退出前执行该函数一次
def exit_callback(context):
    pass



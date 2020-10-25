import ccxt
import pandas as pd
from datetime import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover,SignalStrategy
from backtesting.test import SMA, GOOG

class SmaCross(Strategy):
    def init(self):
        # super().init()
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        # super().next()
        if crossover(self.ma1, self.ma2):
            self.position.close()
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.position.close()
            self.sell()
        # if crossover(self.ma2, self.ma1):
        #     self.position.close()
        #     self.sell()
        # elif crossover(self.ma1, self.ma2):
        #     self.position.close()
        #     self.buy()

# class Strategy(SignalStrategy):
    
    # def init(self):
    #     super().init()
        
    #     # Precompute the two moving averages
    #     close = pd.Series(self.data.Close)
    #     sma1 = close.rolling(20).mean()
    #     sma2 = close.rolling(60).mean()
        
    #     # Precompute signal
    #     signal_long = (sma1 > sma2) & (sma1.shift() < sma2.shift())
    #     signal_short = (sma1 < sma2) & (sma1.shift() > sma2.shift())
        
    #     signal = signal_long
    #     signal[signal_short] = -1
        
    #     self.set_signal(signal)
        
        
    # def next(self):
    #     super().next()

# K-line
binance_exchange = ccxt.binance({
    'timeout':15000,
    'enableRateLimit':True
})
BinanceMarket = binance_exchange.load_markets()

print('交易所id：', binance_exchange.id)
# print('交易所名称：', binance_exchange.name)
# print('是否支持共有API：', binance_exchange.has['publicAPI'])
# print('是否支持私有API：', binance_exchange.has['privateAPI'])
print('支持的时间频率：', binance_exchange.timeframes)
# print('最长等待时间(s)：', binance_exchange.timeout / 1000)
# print('访问频率(s)：', binance_exchange.rateLimit / 1000)
# print('交易所名称：', binance_exchange.name)
# print('支持的时间频率：', binance_exchange.timeframes)
# print('支持幣種: ',list(BinanceMarket.keys()))

start_time = binance_exchange.parse8601('2020-07-15T12:00:00Z')  #會執行
start_time2 = binance_exchange.parse8601('2020-08-15T16:00:00Z') #不會執行
end_time  = binance_exchange.parse8601('2019-12-31T00:00:00Z')

if binance_exchange.has['fetchOHLCV']:
    kline_data = pd.DataFrame(binance_exchange.fetch_ohlcv('BTC/USDT',timeframe='1h',since=start_time))
    # kline_data = pd.DataFrame(binance_exchange.fetch_ohlcv('BTC/USDT',timeframe='4h'))
    kline_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    kline_data['Datetime'] = kline_data['Datetime'].apply(binance_exchange.iso8601)
    # kline_data.to_csv("BTC-USDT_Binance.txt")
    # print(kline_data.tail()) 
    # print(kline_data.head(len(kline_data)))  #列出全部資料
    kline_data.index = pd.DatetimeIndex(kline_data['Datetime']) #將index改為datetime 以符合backtesting要求
    print("CCX原始資料")
    print(kline_data)
    print("============================") 
    kline_data.drop(columns="Datetime",inplace=True)
    # kline_data.index = pd.to_datetime(kline_data['Datetime'])
    kline_data.to_csv("BTC-USDT1h_Binance_worked.txt")
    print("CCX修改資料")
    print(kline_data) 
    print("============================") 

bt = Backtest(kline_data, SmaCross)
stats = bt.run()
stats.to_csv("overall_worked.txt")
bt.plot()
del kline_data

# if binance_exchange.has['fetchOHLCV']:
#     kline_data = pd.DataFrame(binance_exchange.fetch_ohlcv('BTC/USDT',timeframe='1h',since=start_time2))
#     # kline_data = pd.DataFrame(binance_exchange.fetch_ohlcv('BTC/USDT',timeframe='4h'))
#     kline_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
#     kline_data['Datetime'] = kline_data['Datetime'].apply(binance_exchange.iso8601)
#     # kline_data.to_csv("BTC-USDT_Binance.txt")
#     # print(kline_data.tail()) 
#     # print(kline_data.head(len(kline_data)))  #列出全部資料
#     kline_data.index = pd.DatetimeIndex(kline_data['Datetime']) #將index改為datetime 以符合backtesting要求
#     print("CCX2原始資料")
#     print(kline_data)
#     print("============================") 
#     kline_data.drop(columns="Datetime",inplace=True)
#     # kline_data.index = pd.to_datetime(kline_data['Datetime'])
#     kline_data.to_csv("BTC-USDT1h_Binance_issued.txt")
#     print("CCX2修改資料")
#     print(kline_data) 
#     print("============================") 

# bt1 = Backtest(kline_data, SmaCross)
# stats1 = bt1.run()
# stats1.to_csv("overall_issued.txt")
# bt1.plot()

# df = pd.read_csv("BTCUSDT-4h-data2.csv",index_col='Timestamp',parse_dates=True)
# # df = pd.read_csv("BTC-USDT_Binance_ch.txt",index_col='Datetime',parse_dates=True)
# # # df = pd.read_csv("EURUSD.txt")
# print("colab原始資料")
# print(df.head())
# print("============================") 
# df.drop(columns=['Close_time','Quote_av','Trades','Tb_base_av','Tb_quote_av','Ignore'],inplace=True)
# print("colab修改資料")
# print(df.head())
# print("============================") 
# bt = Backtest(df, SmaCross)
# stats = bt.run()
# # stats.to_csv("strategy overall.txt")
# bt.plot()
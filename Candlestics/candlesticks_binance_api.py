from binance.client import Client
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

api_key = ''
api_secret = ''


client = Client(api_key, api_secret)
status = client.get_system_status()
print(f"Status: {status}\n")

if status['msg'] == 'normal':
    # candles = client.get_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_1MINUTE)
    candles = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_12HOUR,
                                           start_str='1 Dec, 2017')

    dataFrames = pd.DataFrame(candles)
    dataFrames.columns = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote asset volume',
                          'Number of trade', 'Taker buy base asset volume', 'Taker buy quote asset volume',
                          'Can be ignored']
    dataFrames['Open_time'] = pd.to_datetime(dataFrames['Open_time'], unit='ms')

    candlesticks = go.Candlestick(x=dataFrames['Open_time'],
                                  open=dataFrames['Open'],
                                  high=dataFrames['High'],
                                  low=dataFrames['Low'],
                                  close=dataFrames['Close'],
                                  name='BTCUSDT')

    volume_bars = go.Bar(x=dataFrames['Open_time'],
                         y=dataFrames['Volume'],
                         name='Volume', marker={'color': 'grey'}, opacity=0.5)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candlesticks, secondary_y=True)
    fig.add_trace(volume_bars, secondary_y=False)
    fig.update_layout(title="BTC/USDT Binance", autotypenumbers='convert types', height=1000)
    fig.update_yaxes(title="Price $", secondary_y=True, showgrid=True)
    fig.update_yaxes(title="Volume", secondary_y=False)

    fig.show()
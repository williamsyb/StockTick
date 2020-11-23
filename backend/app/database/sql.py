sql_dict = dict(
    depth_raw_sql="select TimeStamp as time, price from depth_raw",
    order_raw_sql="select OrderTime as time, OrderVolume  from order_raw",
    trade_raw_sql="select TradeTime as time, TradeVolume from trade_raw",

    ohlc_10min_sql="select TimeStamp as time, open, high, low, close from ohlc_10min",
    ohlc_1min_sql="select TimeStamp as time, open, high, low, close from ohlc_1min",
    ohlc_5min_sql="select TimeStamp as time, open, high, low, close from ohlc_5min",

    order_10min_sql="select OrderTime as time, OrderVolume from order_10min",
    order_1min_sql="select OrderTime as time, OrderVolume from order_1min",
    order_5min_sql="select OrderTime as time, OrderVolume from order_5min",

    trade_10min_sql="select TradeTime as time, TradeVolume from trade_10min",
    trade_1min_sql="select TradeTime as time, TradeVolume from trade_1min",
    trade_5min_sql="select TradeTime as time, TradeVolume from trade_5min",
)

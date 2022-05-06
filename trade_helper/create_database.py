from sqlalchemy import create_engine, Table, Column, Integer, delete, update
from sqlalchemy import String, Float, Date, MetaData, CHAR
from trade.binance_api import Binance
from sqlalchemy.orm import sessionmaker
from datetime import date
import telebot

token = "2040560954:AAFIkU3ArTg8XZUsYQ5F6EV-Q37eLMz9gqY"
bots = telebot.TeleBot(token)

meta = MetaData()
pair_list = Table('Pair_list', meta,
                  Column('Pair_id', Integer, primary_key=True),
                  Column('Pair_name', String(20), nullable=False),
                  )

engine = create_engine(f'sqlite:///trade.db', echo=True, connect_args={'check_same_thread':False})


pairs = ["BTCUSDT", "BNBUSDT", "ETHUSDT", "XRPUSDT", "LUNAUSDT", "ADAUSDT",
         "SOLUSDT", "AVAXUSDT", "DOTUSDT", "DOGEUSDT", "MATICUSDT",
         "ATOMUSDT", "LTCUSDT", "NEARUSDT", "LINKUSDT", "TRXUSDT",
         "UNIUSDT", "FTTUSDT", "BCHUSDT", "ALGOUSDT", "XLMUSDT",
         "MANAUSDT", "HBARUSDT", "ETCUSDT", "XMRUSDT", "SANDUSDT"]
conn = engine.connect()
Session = sessionmaker(bind=engine)
s = Session()
bot = Binance(
    API_KEY='TH2gATkP9dGER8NIdws4gzJ7xR1hTWCjpWDm4wjGv8BvICmZnELhAjU1AifPsNZK',
    API_SECRET='x9CBXLOR4THuwzp8mXwM5PtQiy5nXhnopLRCGZ4MnPAKgqsrwcBGeboXvsKbByXE'
)


def atr(it, time_frame):
    p_history = Table(it, meta,
                      Column('Id_pair', Integer, primary_key=True),
                      Column('Open_date', Date, unique=True),
                      Column('Pair_name', CHAR),
                      Column('Open_price', Float),
                      Column('High_price', Float),
                      Column('Low_price', Float),
                      Column('Close_price', Float),
                      Column('Volume', Float),
                      extend_existing=True)
    atr_ma = []
    s = Session()
    i = s.query(p_history).order_by(p_history.c.Open_date.desc()).limit(f'{time_frame}')
    t = time_frame
    atr1_l = [x.Low_price for x in i]
    atr1_h = [x.High_price for x in i]
    while t >= 1:
        atr1_ll = atr1_l[t - 1]
        atr1_hh = atr1_h[t - 1]
        atr_ma.append(atr1_hh - atr1_ll)
        t -= 1
        result = sum(atr_ma) / time_frame
    return result
def ma(it, time_frame):
    p_history = Table(it, meta,
                      Column('Id_pair', Integer, primary_key=True),
                      Column('Open_date', Date, unique=True),
                      Column('Pair_name', CHAR),
                      Column('Open_price', Float),
                      Column('High_price', Float),
                      Column('Low_price', Float),
                      Column('Close_price', Float),
                      Column('Volume', Float),
                      extend_existing=True)
    s = Session()
    i = s.query(p_history).order_by(p_history.c.Id_pair.desc()).limit(f'{time_frame}')
    tr = [x.Close_price for x in i]
    result = sum(tr)/time_frame
    res = []
    res.append(result)
    return res
def check_sl(it):
    p_history = Table(it, meta,
                      Column('Id_pair', Integer, primary_key=True),
                      Column('Open_date', Date, unique=True),
                      Column('Pair_name', CHAR),
                      Column('Open_price', Float),
                      Column('High_price', Float),
                      Column('Low_price', Float),
                      Column('Close_price', Float),
                      Column('Volume', Float),
                      extend_existing=True)
    p_trade = Table('Trade_history', meta,
                    Column('Id_trade', Integer, primary_key=True),
                    Column('Open_date', Date),
                    Column('Pair_name', CHAR),
                    Column('Type_of_trade', String(10)),
                    Column('Open_price', Float),
                    Column('Last_price', Float),
                    Column('Close_price', Float),
                    Column('Paper_profit', Float),
                    Column('Profit', Float),
                    Column('Stop_Loss', Float),
                    Column('Status', CHAR),
                    extend_existing=True)
    for x in s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Pair_name == it).order_by(p_trade.c.Id_trade).limit(1):
        for z in s.query(p_history).order_by(p_history.c.Open_date.desc()).limit(1):
            stop = x.Stop_Loss
            l_price = z.Close_price
            type_of_trade = x.Type_of_trade
            if type_of_trade == 'BUY' and l_price > stop:
                return True
            elif type_of_trade == 'SELL' and l_price < stop:
                return True
            else:
                return False


p_trade = Table('Trade_history', meta,
                Column('Id_trade', Integer, primary_key=True),
                Column('Open_date', Date),
                Column('Pair_name', CHAR),
                Column('Type_of_trade', String(10)),
                Column('Open_price', Float),
                Column('Last_price', Float),
                Column('Close_price', Float),
                Column('Paper_profit', Float),
                Column('Profit', Float),
                Column('Stop_Loss', Float),
                Column('Status', CHAR),
                extend_existing=True)

result_sell = 0
result_buy = 0
for sell in s.query(p_trade).filter(p_trade.c.Status == 'Close', p_trade.c.Type_of_trade == 'SELL'):
    o = sell.Open_price
    c = sell.Close_price
    result_sell += ((o * 100 / c) - 100) * 0.02
    print(result_sell)
for buy in s.query(p_trade).filter(p_trade.c.Status == 'Close', p_trade.c.Type_of_trade == 'BUY'):
    ob = buy.Open_price
    cb = buy.Close_price
    result_buy += ((cb * 100 / ob) - 100) * 0.02
    print(result_buy)


result = result_sell + result_buy
print('****')
print(result)
print('****')

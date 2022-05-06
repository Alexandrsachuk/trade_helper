from sqlalchemy import create_engine, Table, Column, Integer, delete, update
from sqlalchemy import String, Float, Date, MetaData, CHAR
from trade.binance_api import Binance
from sqlalchemy.orm import sessionmaker
from datetime import date
import telebot
from telebot import types
token = "..."
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
    API_KEY='...',
    API_SECRET='...'
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
@bots.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('/start')
    itembtn2 = types.KeyboardButton('/update_history')
    itembtn3 = types.KeyboardButton('/update_trade')
    itembtn4 = types.KeyboardButton('/check_trade')
    itembtn5 = types.KeyboardButton('/open_trade')
    itembtn6 = types.KeyboardButton('/paper_profit')
    itembtn7 = types.KeyboardButton('/profit')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
    bots.send_message(message.from_user.id, "Choose one letter:", reply_markup=markup)
# Создание таблицы на каждую торговую пару
# a = 1
# for it in pairs:
#     pair_history = Table(f'{it}', meta,
#                          Column('Id_pair', Integer, primary_key=True),
#                          Column('Open_date', Date, unique=True),
#                          Column(f'ID', Integer, ForeignKey("Pair_list.Pair_id")),
#                          Column('Open_price', Float),
#                          Column('High_price', Float),
#                          Column('Low_price', Float),
#                          Column('Close_price', Float),
#                          Column('Volume', Float)
#                          )
#
#     a += 1
#     meta.create_all(engine)

#Внесение данных в новую таблицу
# for it in pairs:
#     j = 400
#     i = 1
#     while j >= 1:
#         candle = (bot.klines(
#             symbol=it,
#             interval='1d',
#             limit=j
#         ))
#         open_date = candle[0][0]
#         open_date = str(open_date)
#         open_date = open_date[:-3]
#         open_date = int(open_date)
#         open_date = date.fromtimestamp(open_date)
#         open_price = candle[0][1]
#         high_price = candle[0][2]
#         low_price = candle[0][3]
#         close_price = candle[0][4]
#         volume = candle[0][5]
#p_history = Table(it, meta,
#                   Column('Id_pair', Integer, primary_key=True),
#                   Column('Open_date', Date, unique=True),
#                   Column('Pair_name', CHAR),
#                   Column('Open_price', Float),
#                   Column('High_price', Float),
#                   Column('Low_price', Float),
#                   Column('Close_price', Float),
#                   Column('Volume', Float),
#                   extend_existing=True)
#         print(p_history)
#
#         load_date = p_history.insert().values(Id_pair=i,
#             Open_date=open_date, ID=a, Open_price=f'{open_price}',
#             High_price=f'{high_price}', Low_price=f'{low_price}',
#             Close_price=f'{close_price}', Volume=f'{volume}')
#
#         conn.execute(load_date)
#         print('****')
#         j -= 1
#         i += 1
#     a += 1
@bots.message_handler(commands=['update_history'])
def upd(message):
    bots.send_message(message.chat.id, "Обновляем данные")
#Внесение данных в старую таблицу
    for it in pairs:
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
        z = s.query(p_history).order_by(p_history.c.Id_pair.desc()).limit(1)
        lp = [x.Id_pair for x in z]
        ld = [x.Open_date for x in z]
        lp = lp[-1]

        i = lp+1
        j = 1
        while j <= 1:
            candle = (bot.klines(
                symbol=it,
                interval='1d',
                limit=j
            ))
            open_date = candle[0][0]
            open_date = str(open_date)
            open_date = open_date[:-3]
            open_date = int(open_date)
            open_date = date.fromtimestamp(open_date)
            open_price = candle[0][1]
            high_price = candle[0][2]
            low_price = candle[0][3]
            close_price = candle[0][4]
            volume = candle[0][5]
            load_date = p_history.insert().values(Id_pair=i,
                                                Open_date=open_date, Pair_name=it, Open_price=f'{open_price}',
                                                High_price=f'{high_price}', Low_price=f'{low_price}',
                                                Close_price=f'{close_price}', Volume=f'{volume}')

            if ld[0] == open_date:
                pass
            else:
                conn.execute(load_date)
                bots.send_message(message.chat.id, f"Пара {it} от {open_date} добавлена! ")
            print('****')
            j += 1

# Delete modelus:
# for it in pairs:

# p_history = Table(it, meta,
#                   Column('Id_pair', Integer, primary_key=True),
#                   Column('Open_date', Date, unique=True),
#                   Column('Pair_name', CHAR),
#                   Column('Open_price', Float),
#                   Column('High_price', Float),
#                   Column('Low_price', Float),
#                   Column('Close_price', Float),
#                   Column('Volume', Float),
#                   extend_existing=True)
#     last = s.query(p_history).filter(p_history.c.Id_pair).order_by(p_history.c.Id_pair.desc()).limit(1)
#
#     load_date = delete(last)
#     conn.execute(load_date)
#     a += 1

#Расчет входа в сделку
#МА
# def ma(it, time_frame):
# p_history = Table(it, meta,
#                   Column('Id_pair', Integer, primary_key=True),
#                   Column('Open_date', Date, unique=True),
#                   Column('Pair_name', CHAR),
#                   Column('Open_price', Float),
#                   Column('High_price', Float),
#                   Column('Low_price', Float),
#                   Column('Close_price', Float),
#                   Column('Volume', Float),
#                   extend_existing=True)
#     s = Session()
#     i = s.query(p_history).order_by(p_history.c.Id_pair.desc()).limit(f'{time_frame}')
#     tr = [x.Close_price for x in i]
#     result = sum(tr)/time_frame
#     res = []
#     res.append(tr[-1])
#     res.append(result)
#     return res
#
# def atr(it, time_frame):
# p_history = Table(it, meta,
#                   Column('Id_pair', Integer, primary_key=True),
#                   Column('Open_date', Date, unique=True),
#                   Column('Pair_name', CHAR),
#                   Column('Open_price', Float),
#                   Column('High_price', Float),
#                   Column('Low_price', Float),
#                   Column('Close_price', Float),
#                   Column('Volume', Float),
#                   extend_existing=True)
#     atr_ma = []
#     s = Session()
#     i = s.query(p_history).order_by(p_history.c.Open_date.desc()).limit(f'{time_frame}')
#     t = time_frame
#     atr1_l = [x.Low_price for x in i]
#     atr1_h = [x.High_price for x in i]
#     while t >= 1:
#         atr1_ll = atr1_l[t-1]
#         atr1_hh = atr1_h[t-1]
#         atr_ma.append(atr1_hh - atr1_ll)
#         t -= 1
#         result = sum(atr_ma)/time_frame
#     return result
#
#
# res = []
# for it in pairs:
# p_history = Table(it, meta,
#                   Column('Id_pair', Integer, primary_key=True),
#                   Column('Open_date', Date, unique=True),
#                   Column('Pair_name', CHAR),
#                   Column('Open_price', Float),
#                   Column('High_price', Float),
#                   Column('Low_price', Float),
#                   Column('Close_price', Float),
#                   Column('Volume', Float),
#                   extend_existing=True)
#     atr_20 = atr(it, 20)
#     ma_20 = ma(it, 20)
#     res.append(it)
#     res.append(atr_20)
#     res.append(ma_20[0])
#     res.append(ma_20[1])
#     print(res)
@bots.message_handler(commands=['update_trade'])
def update_trade(message):
    bots.send_message(message.from_user.id, 'Проверить на наличие новых сделок')
#Расчет и внесение сделок
    for it in pairs:
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

        ma_200 = ma(it, 200)
        ma_120 = ma(it, 120)
        ma_20 = ma(it, 20)
        atr_20 = atr(it, 20)
        lp = s.query(p_history).order_by(p_history.c.Id_pair.desc()).limit(1)
        last_price = [x.Close_price for x in lp]
        last_price = last_price[0]

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
        ids = s.query(pair_list).filter(pair_list.c.Pair_name == it)
        info = s.query(p_history).order_by(p_history.c.Open_date.desc()).limit(1)
        if ma_120 >= ma_200 and ma_20 >= ma_120 and last_price >= ma_20[0]: #Сравнение результатов функций и вывод решения в тренде пара или нет
            print(f"Pair {it} in uptrend with last price {last_price}")
            print(ma_200)
            print(ma_120)
            print(ma_20)
            for x in ids:
                for zx in info:
                    id = x.Pair_id
                    open_d = zx.Open_date
                    open_p = zx.Close_price
                    load_date = p_trade.insert().values(Open_date=open_d, Pair_name=it, Open_price=open_p,
                                                        Stop_Loss=open_p-atr_20*2, Type_of_trade='BUY', Status='Open')
                    conn.execute(load_date)
        elif ma_120 <= ma_200 and ma_20 <= ma_120 and last_price <= ma_20[0]:
            print(f"Pair {it} in downtrend with last price {last_price}")
            print(ma_200)
            print(ma_120)
            print(ma_20)
            for x in ids:
                for zx in info:
                    id = x.Pair_id
                    open_d = zx.Open_date
                    open_p = zx.Close_price
                    load_date = p_trade.insert().values(Open_date=open_d, Pair_name=it, Open_price=open_p,
                                                        Stop_Loss=open_p+atr_20*2, Type_of_trade='SELL', Status='Open')
                    conn.execute(load_date)
        check_pair = s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Pair_name == it).order_by(
            p_trade.c.Pair_name).limit(2)
        result = []
        for x in check_pair:
            result.append(x)
            print(result)
            a = len(result)
            print(a)
            if a == 2:
                c_pair = s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Pair_name == it).order_by(
                    p_trade.c.Id_trade.desc()).limit(1)
                for z in c_pair:
                    a = z.Id_trade
                    delete_pair = delete(p_trade).where(p_trade.c.Id_trade == a).execution_options(synchronize_session="fetch")
                    s.execute(delete_pair)
                    s.commit()
            else:
                pass
        bots.send_message(message.chat.id, f"Обновляем данные по паре {it}")
#Создание таблицы для сигналов

# p_trade = Table('Trade_history', meta,
#                 Column('Id_trade', Integer, primary_key=True),
#                 Column('Open_date', Date),
#                 Column('Pair_name', CHAR),
#                 Column('Type_of_trade', String(10)),
#                 Column('Open_price', Float),
#                 Column('Last_price', Float),
#                 Column('Close_price', Float),
#                 Column('Paper_profit', Float),
#                 Column('Profit', Float),
#                 Column('Stop_Loss', Float),
#                 Column('Status', CHAR),
#                 extend_existing=True)
#
# meta.create_all(engine)
@bots.message_handler(commands=['check_trade'])
def check_trade(message):
    bots.send_message(message.chat.id, 'Проверка открытых сделок')
#Проверка открытых сделок на закрытие
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

    for x in s.query(p_trade).filter(p_trade.c.Status == 'Open'):
        it = x.Pair_name
        type_of_trade = x.Type_of_trade
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

        ma_200 = ma(it, 200)
        ma_120 = ma(it, 120)
        ma_20 = ma(it, 20)
        info = s.query(p_history).order_by(p_history.c.Open_date.desc()).limit(1)
        if type_of_trade == 'BUY':
            if ma_200[0] >= 0:
                b = check_sl(it)
                for zx in info:
                    last_p = zx.Close_price
                    if b == False:
                        load_date = (update(p_trade).
                                     where(p_trade.c.Pair_name == it).
                                     values(Close_price=last_p, Status='Close')
                                     )
                        bots.send_message(message.chat.id, f'Сделка по паре {it} закрыта по цене {last_p}')
                        conn.execute(load_date)
                    elif ma_20 <= ma_120:
                        for zx in info:
                            last_p = zx.Close_price
                            load_date = (update(p_trade).
                                         where(p_trade.c.Pair_name == it).
                                         values(Close_price=last_p, Status='Close')
                                         )
                            bots.send_message(message.chat.id, f'Сделка по паре {it} закрыта по цене {last_p}')
                            conn.execute(load_date)
                    elif ma_120 >= ma_200 and ma_20 >= ma_120:
                        for zx in info:
                            last_p = zx.Close_price
                            load_date = (update(p_trade).
                                         where(p_trade.c.Pair_name == it).
                                         values(Last_price=last_p)
                                         )
                            bots.send_message(message.chat.id, f'Сделка по паре {it} в работе')
                            conn.execute(load_date)
                    else:
                        pass

        elif type_of_trade == 'SELL':
            if ma_200[0] >= 0:
                b = check_sl(it)
                for zx in info:
                    last_p = zx.Close_price
                    if b == False:
                        load_date = (update(p_trade).
                                     where(p_trade.c.Pair_name == it).
                                     values(Close_price=last_p, Status='Close')
                                     )
                        bots.send_message(message.chat.id, f'Сделка по паре {it} закрыта по цене {last_p}')
                        conn.execute(load_date)
                    elif ma_20 >= ma_120:
                        for zx in info:
                            last_p = zx.Close_price
                            load_date = (update(p_trade).
                                         where(p_trade.c.Pair_name == it).
                                         values(Close_price=last_p, Status='Close')
                                         )
                            bots.send_message(message.chat.id, f'Сделка по паре {it} закрыта по цене {last_p}')
                            conn.execute(load_date)
                    elif ma_120 <= ma_200 and ma_20 <= ma_120:
                        for zx in info:
                            last_p = zx.Close_price
                            load_date = (update(p_trade).
                                         where(p_trade.c.Pair_name == it).
                                         values(Last_price=last_p)
                                         )
                            bots.send_message(message.chat.id, f'Сделка по паре {it} в работе')
                            conn.execute(load_date)
                    else:
                        pass
        else:
            ...

#Удаление дублей
# p_trade = Table('Trade_history', meta,
#                 Column('Id_trade', Integer, primary_key=True),
#                 Column('Open_date', Date),
#                 Column('Pair_name', CHAR),
#                 Column('Type_of_trade', String(10)),
#                 Column('Open_price', Float),
#                 Column('Last_price', Float),
#                 Column('Close_price', Float),
#                 Column('Paper_profit', Float),
#                 Column('Profit', Float),
#                 Column('Stop_Loss', Float),
#                 Column('Status', CHAR),
#                 extend_existing=True)
#
# for it in pairs:
#     check_pair = s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Pair_name == it).order_by(
#         p_trade.c.Pair_name).limit(2)
#     result = []
#     for x in check_pair:
#         result.append(x)
#         print(result)
#         a = len(result)
#         print(a)
#         if a == 2:
#             c_pair = s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Pair_name == it).order_by(
#                 p_trade.c.Id_trade.desc()).limit(1)
#             for z in c_pair:
#                 a = z.Id_trade
#                 delete_pair = delete(p_trade).where(p_trade.c.Id_trade == a).execution_options(synchronize_session="fetch")
#                 s.execute(delete_pair)
#                 s.commit()
#         else:
#             pass

@bots.message_handler(commands=['open_trade'])
def open_trade(message):
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
    for x in s.query(p_trade).filter(p_trade.c.Status == 'Open'):
        name = x.Pair_name
        type_of_trade = x.Type_of_trade
        l_price = x.Last_price
        bots.send_message(message.chat.id, f'{type_of_trade} cделка по паре {name} с последней ценой {l_price}')

@bots.message_handler(commands=['paper_profit'])
def open_trade(message):
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
    for sell in s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Type_of_trade == 'SELL'):
        o = sell.Open_price
        c = sell.Last_price
        result_sell += ((o * 100 / c) - 100) * 0.02
        print(result_sell)
    for buy in s.query(p_trade).filter(p_trade.c.Status == 'Open', p_trade.c.Type_of_trade == 'BUY'):
        ob = buy.Open_price
        cb = buy.Last_price
        result_buy += ((cb * 100 / ob) - 100) * 0.02
        print(result_buy)
    result = float('{:.2f}'.format(result_sell + result_buy))
    bots.send_message(message.chat.id, f'Всего бумажной прибыли {result}% при риске на сделку {2}% от депозита ')

@bots.message_handler(commands=['profit'])
def open_trade(message):
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

    result = float('{:.2f}'.format(result_sell + result_buy))
    bots.send_message(message.chat.id, f'Всего зафиксированой прибыли {result}% при риске на сделку {2}% от депозита ')
bots.polling(none_stop=True)

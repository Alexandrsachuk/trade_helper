from trade.database import Session
from trade.pair_history import Pair_history
session = Session()


def ma(check_pair, time_frame):

    check_pair = check_pair.upper()
    s = Session()
    i = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.desc()).limit(f'{time_frame}')
    tr = [x.close_price for x in i]
    result = sum(tr)/time_frame
    return result


def stochastic(check_pair, time_frame):

    check_pair = check_pair.upper()
    s = Session()
    i = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.desc()).limit(f'{time_frame}')
    lp = [x.close_price for x in i]
    lp = lp[-1]
    low_p = [x.low_price for x in i]
    result_low_p = min(low_p)
    high_p = [x.high_price for x in i]
    result_high_p = max(high_p)
    k = ((lp - result_low_p) / (result_high_p - result_low_p)) * 100
    return k


def atr(check_pair, time_frame):
    choice = []
    check_pair = check_pair.upper()
    s = Session()
    i = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.desc()).limit(1)

    atr1_l = [x.low_price for x in i]
    atr1_l = atr1_l[-1]
    atr1_h = [x.high_price for x in i]
    atr1_h = atr1_h[-1]
    atr1 = atr1_h - atr1_l

    choice.append(atr1)

    atr2_h = [x.high_price for x in i]
    atr2_h = atr2_h[-1]
    atr2_h1_prepare = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.desc()).limit(2)
    atr2_h1 = [x.high_price for x in atr2_h1_prepare]
    atr2_h1 = atr2_h1[-1]
    atr2 = atr2_h - atr2_h1
    atr2 = abs(atr2)
    choice.append(atr2)

    atr3_l = [x.low_price for x in i]
    atr3_l = atr3_l[-1]
    atr3_l1_prepare = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.desc()).limit(2)
    atr3_l1 = [x.low_price for x in atr3_l1_prepare]
    atr3_l1 = atr3_l1[-1]
    atr3 = atr3_l - atr3_l1
    atr3 = abs(atr3)
    choice.append(atr3)
    ch = max(choice)
    return ch

def obv(check_pair, time_frame):

    check_pair = check_pair.upper()
    s = Session()
    i = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.asc()).limit(f'{time_frame}')
    lp = [x.close_price for x in i]
    v = s.query(Pair_history).filter((Pair_history.pair_name == f'{check_pair}')).order_by(
        Pair_history.open_date.asc()).limit(f'{time_frame}')
    lv = [x.volume for x in i]
    obv = 0

    return lp

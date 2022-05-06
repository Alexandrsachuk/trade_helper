import os
from trade.database import DATABASE_NAME, Session
import create_database as db_creator
from trade.indicators import ma, stochastic, atr, obv
# from trade.pair_list import *
from trade.pair_history import Pair_history

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_database()

# a = str(input('Введите торговую пару: '))
# b = int(input('Введите таймфрейм: '))
#
# print("%.2f" % ma(a, b))
# print("%.2f" % stochastic(a, b))
# print("%.2f" % atr(a, b))
# for x in obv(a, b):
#     print(x)




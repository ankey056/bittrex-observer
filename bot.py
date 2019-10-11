#!/usr/bin/env python3

from bittrex import Bittrex
from lib.history import History, Buy_op
from datetime import timedelta, datetime
import re

REPORT_PROGRESS = True
# REPORT_PROGRESS = False

## Operations before t0 are not considered
def get_t0_time():
    # delta = timedelta(minutes=30) # For recent 30 minutes
    # delta = timedelta(hours=1) # For recent 1 hour
    # delta = timedelta(days=1) # For recent day
    delta = timedelta(minutes=10) # For recent 10 minutes
    t0 = datetime.utcnow()
    return t0 - delta


# MARKETS_FILTERS = ['BTC-.+']

MARKETS_FILTERS = [lambda s: s[:4] == 'BTC-']

def filter_market_names(names):
    x = MARKETS_FILTERS
    if len(x) == 0: return names

    def handle_regexp (s):
        if type(s) is str:
            return re.compile(s)
        else:
            return s

    rs = list(map(handle_regexp, x))

    def is_pass (name):
        for r in rs:
            if callable(r):
                if r(name): return True
            elif r.match(name): return True

        return False

    l = []

    for name in names:
        if is_pass(name): l.append(name)

    return l

class Market:
    pass

if __name__ == "__main__":
    bittrex_client = Bittrex(None, None)

    response = bittrex_client.get_market_summaries()

    x = map(lambda m: m['MarketName'],
            response['result'])

    names = filter_market_names(list(x))

    markets = list()
    time0 = get_t0_time()

    n = len(names)
    print("Now is {} by UTC".format(str(datetime.utcnow())))
    print("t0 is {} by UTC".format(str(time0)))
    s = "Downloading of {} markets histories have launched. Please wait."
    print(s.format(n))

    i = 0
    for name in names:
        x = Market()
        x.name = name
        response = bittrex_client.get_market_history(name)
        h = History.load_from_web_list(response['result'])
        x.history = h
        markets.append(x)
        i+=1
        if REPORT_PROGRESS:
            s = "{}: {} of {} request have done [{:.0f}%]"
            print(s.format(str(datetime.now()),
                           i, n, 100*i/n))

    for m in markets:
        q = 0
        for op in m.history.operations:
            if (type(op) is Buy_op) and (time0 <= op.date):
                q+=1

        m.q = q

    markets.sort(key=lambda m: m.q)

    for m in markets:
        print("{}: {}".format(m.name, m.q))

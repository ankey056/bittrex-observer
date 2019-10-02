
from dateutil.parser import parse as parse_timestamp

class Operation:
    def __init__ (self, date):
        self.date = date

    def load_from_web_dict (d):
        s = d["OrderType"]

        if "BUY" == s:
            c = Buy_op
        elif "SELL" == s:
            c = Sell_op
        else:
            raise Exception("'{}' is wrong string for parsing of Operation's type".format(s))
        
        return c(parse_timestamp(d["TimeStamp"]))

class Buy_op(Operation):
    pass

class Sell_op(Operation):
    pass
                         

class History:
    def __init__ (self, operations=None):
        self.operations = operations

    def load_from_web_list (l):
        x = map(Operation.load_from_web_dict,
                l)
        ops = list(x)
        ops.sort(key=lambda op: op.date,
                 reverse=True)

        return History(ops)


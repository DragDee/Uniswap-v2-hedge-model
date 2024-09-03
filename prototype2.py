import time

from main import IL
from binance import BinanceTrading

class Short:
    position_size = 20
    entery_price = 500
    short_entery_money = 10000
    total_closed_short_in_usdt = 0
    total_closed_in_coin = 0
    average_close_price = 0
    sum_money_long = 0
    total_parts = 0
    total_position = 0
    money_supplyed_to_short = 0
    average_entry_short_price = 500
    sum_money_short = 0
    total_parts_short = 0
    position_margin = 10000
    short_pnl = 0
    closed_parts_pnl = 0
    realized_long_pnl = 0
    realized_short_pnl = 0
    last_price = 0


    def __init__(self, il: IL):
        self.il = il

    def show_stats(self):
        s = f"{self.last_price}" + " " * 15 + f"{self.position_size}" + " " * 15 + f"{self.position_margin}" + " " * 15 +\
            f"{self.short_pnl}" +\
            " " * 15 + f"{self.sum_money_long}" + " " * 15 + f"{self.total_closed_in_coin}" +\
            " " * 15 + f"{self.average_close_price}" +\
            " " * 15 + f"{self.total_position}"
        print(s)

    def close_short(self, part, price):
        self.last_price = price

        self.total_closed_in_coin += part
        self.total_parts += part
        self.position_size += part
        delta = self.average_entry_short_price - price
        self.closed_parts_pnl -= delta * part
        self.short_pnl = delta * self.position_size
        self.realized_long_pnl -= delta * part

        pure_closed_usdt = part * price
        self.total_closed_short_in_usdt += pure_closed_usdt
        self.position_margin += -delta * part
        self.short_entery_money = self.position_size * self.average_entry_short_price


        self.sum_money_long += part * price
        self.average_close_price = self.sum_money_long / self.total_parts

        newA = il.get_new_A(price)#eth
        newB = il.get_new_B(price)


        self.total_position = self.position_margin + self.short_pnl + newA * price + newB - self.sum_money_short

    def open_short(self, part, price):
        self.last_price = price

        self.total_parts_short += part

        newA = il.get_new_A(price)
        newB = il.get_new_B(price)

        self.sum_money_short += part * price
        self.position_margin += part * price
        self.average_entry_short_price = (self.position_size * self.average_entry_short_price + part * price) /\
                                         (self.position_size + part)
        self.position_size += part
        delta = self.average_entry_short_price - price
        self.short_pnl = delta * self.position_size



        self.total_position = self.position_margin + self.short_pnl + newA * price + newB - self.sum_money_short

    def show_stats_for_short(self):
        s = f"{self.last_price}" + " " * 15 + f"{self.position_size}" + " " * 15 + f"{self.total_parts_short}" + " " * 15 + f"{self.average_entry_short_price}" + \
     " " * 15 + f"{self.sum_money_short}" + \
            " " * 15 + f"{self.total_position}"
        print(s)






class Trading:
    last_price = 500
    step = 1.5
    symbol = 'BNBUSDT'
    decimals = 2

    def __init__(self, il: IL, short: Short):
        self.il = il
        self.short = short
        self.last_price = il.start_price
        self.last_A = il.A
        self.binance = BinanceTrading()

        self.two_orders()


    def two_orders(self):
        self.binance.cancel_all_orders(self.symbol)

        top = round(self.last_price * (1 + self.step / 100), self.decimals)
        bottom = round(self.last_price * (1 - self.step / 100), self.decimals)
        deltaA = self.find_deltaA(top)

        stop_price = round(top - 10 ** (-self.decimals), self.decimals)
        self.binance.open_stop_order(self.symbol, 'BUY', quantity=deltaA, price=top, stop_price=stop_price)
        deltaA = self.find_deltaA(bottom)
        stop_price = round(bottom + 10 ** (-self.decimals), self.decimals)
        self.binance.open_stop_order(self.symbol, 'SELL', quantity=deltaA, price=bottom, stop_price=stop_price)

    def work_rest_api(self):
        delay = 1
        while True:
            price = self.binance.get_price(self.symbol)
            print(price)
            time.sleep(delay)
            self.main_f(price)

    def main_f(self, price):
        top = self.last_price * (1 + self.step/100)
        bottom = self.last_price * (1 - self.step / 100)

        if price >= top:
            deltaA = self.find_deltaA(price)
            stop_price = round(price - 10**(-self.decimals), self.decimals)
            self.binance.open_stop_order(self.symbol, 'BUY', quantity=deltaA, price=price, stop_price=stop_price)
            self.short.close_short(deltaA, price)
            self.short.show_stats()
            self.last_price = price
            self.two_orders()

        elif price <= bottom:
            deltaA = self.find_deltaA(price)
            stop_price = round(price + 10 ** (-self.decimals), self.decimals)
            self.binance.open_stop_order(self.symbol, 'SELL', quantity=deltaA, price=price, stop_price=stop_price)
            self.short.open_short(deltaA, price)
            self.short.show_stats_for_short()
            self.last_price = price
            self.two_orders()

        else:
            print("Not in diopason")
            print('Borders = ')
            print(top)
            print(bottom)
            print('-'*20)

    def sim_grow(self, peak_price):
        price = self.last_price
        while price < peak_price:
            price = (1 + self.step / 100) * price
            self.main_f(price)

    def sim_fall(self, bottom_price):
        price = self.last_price
        while price > bottom_price:
            price = (1 - self.step / 100) * price
            self.main_f(price)



    def find_deltaA(self, price):
        newA = self.il.get_new_A(price)
        deltaA = round(newA - self.last_A, self.decimals)
        self.last_A = newA
        return abs(deltaA)

    def find_part(self):
        self.last_price = (1 - self.step / 100) * self.last_price
        newA = self.il.get_new_A(self.last_price)
        deltaA = newA - self.last_A
        self.last_A = newA
        return deltaA


    def price_increses(self, peak_price):
        price = self.last_price
        while price < peak_price:
            price = (1 + self.step / 100) * price
            self.last_price = price
            newA = self.il.get_new_A(price)
            deltaA = newA - self.last_A
            #deltaA *= 1.02
            self.last_A = newA
            self.short.close_short(deltaA, price)
            short.show_stats()



    def prise_decreses(self, bottom_price):
        while self.last_price > bottom_price:
            deltaA = self.find_part()
            #deltaA *= 1.02
            self.short.open_short(deltaA, self.last_price)

            short.show_stats_for_short()



il = IL(start_price=530)
short = Short(il)
trading = Trading(il, short)


if __name__ == '__main__':

    il = IL(start_price=517.06)
    short = Short(il)
    trading = Trading(il, short)
    #trading.price_increses(2000)
    #trading.sim_grow(2000)

    trading.work()
    #trading.prise_decreses(250)





'''class Trading:
    def price_increses(self):'''


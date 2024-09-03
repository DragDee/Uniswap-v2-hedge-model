from main import IL

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

    def __init__(self, il: IL, short: Short):
        self.il = il
        self.short = short
        self.last_A = il.A

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
            deltaA *= 1.02
            self.last_A = newA
            self.short.close_short(deltaA, price)
            short.show_stats()



    def prise_decreses(self, bottom_price):
        while self.last_price > bottom_price:
            deltaA = self.find_part()
            deltaA *= 1.02
            self.short.open_short(deltaA, self.last_price)

            short.show_stats_for_short()

il = IL()
short = Short(il)
trading = Trading(il, short)
trading.price_increses(2000)




'''class Trading:
    def price_increses(self):'''


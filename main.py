import math
class IL:
    B = 1000
    A = 2
    h = 2000
    start_price = 500

    def __init__(self, start_price=500):
        self.start_price = start_price

    def get_y(self, x):
        return (x * self.B) / (self.A - x)

    def medial_swap_price(self, x):
        return self.B / (self.A - x)

    def new_price(self, x):
        return self.h / math.sqrt(self.A - x)

    def x_for_selected_price(self, price):
        x = self.A - math.sqrt(self.h / price)
        return x

    def get_new_A(self, price):
        x = self.x_for_selected_price(price)
        newA = self.A - x

        return newA

    def get_new_B(self, price):
        x = self.x_for_selected_price(price)
        y = self.get_y(x)
        newB = self.B + y

        return newB



    def pool_proporsions_for_price(self, price, show_info=True):
        x = self.A - math.sqrt(self.h/price)
        y = self.get_y(x)
        medial_price = self.medial_swap_price(x)
        newA = self.A - x
        newB = self.B + y

        if show_info:
            print("x = " + str(x))
            print("y = " + str(y))
            print("Median Swap price = " + str(medial_price))
            print("New Pool:")
            print("ETH:" + "-"*80 + "USDT:")
            print(str(newA) + " "*60 + str(newB))

        return (newA, newB, medial_price)

    def stata(self):
        i = 0.5
        body = self.A
        sum_money = 0
        step = 0.5
        price = 500

        while i < 300:
            price = round((1 - step/100) * price, 2)
            newA, newB, medial_price = self.pool_proporsions_for_price(price, show_info=False)
            newA = round(newA, 4)
            newB = round(newB, 2)
            medial_price = round(medial_price, 3)
            deltaA = round((newA/self.A - 1) * 100, 2)
            deltaB = round((newB / self.B - 1) * 100, 2)

            part_to_buy = round(newA - body, 4)
            sum_money += part_to_buy * price
            body += part_to_buy
            parts = newA - self.A
            average = round(sum_money / parts, 3)
            average_different_procent = round(((medial_price/average) - 1) * 100, 3)

            total_position = (-1 * (
                        price / self.start_price - 2) * self.B) + newA * price + newB +\
                             -1 * (price/average - 1) * sum_money

            s = f"(-{step}%){price}:" + " "*15 + f"{newA}({deltaA}%)" + " "*15 + f"{newB}({deltaB}%)" + " "*15 + f"{medial_price}" + " "*15 + f"{part_to_buy}" + " "*15 + f"{average}({average_different_procent}%)" + " "*15 + f"{sum_money}" + " "*15 + f"{total_position}"
            print(s)
            i += 1


    def stata_grow(self):
        i = 0.5
        body = self.A
        sum_money = 0
        step = 0.5
        steps = 278
        price = self.start_price
        closed_short_in_pure_usdt = 0
        sum_of_parts = 0

        while i < steps:
            price = (1 + step/100) * price
            newA, newB, medial_price = self.pool_proporsions_for_price(price, show_info=False)


            deltaA = round((newA/self.A - 1) * 100, 2)#отклонение от начальных значений пула в процентах
            deltaB = round((newB / self.B - 1) * 100, 2)#отклонение от начальных значений пула в процентах

            part_to_buy = round(newA - body, 4)
            sum_money += part_to_buy * price

            closed_short_in_pure_usdt += (price/self.start_price - 2) * price * part_to_buy

            body += part_to_buy
            parts = newA - self.A
            average = round(sum_money / parts, 3)
            average_different_procent = round(((medial_price/average) - 1) * 100, 3)

            total_position = (-1 * (price/self.start_price - 2) * newA / self.A * self.B) + newA * price + newB + closed_short_in_pure_usdt

            change = round((price / self.start_price) - 1, 2)

            sum_of_parts += part_to_buy

            price = round(price, 2)
            newA = round(newA, 4)
            newB = round(newB, 2)
            medial_price = round(medial_price, 3)

            s = f"(+{change}%){price}:" + " "*15 + f"{newA}({deltaA}%)" + " "*15 + f"{newB}({deltaB}%)" + " "*15 + f"{medial_price}" + " "*15 + f"{part_to_buy}" +\
                " "*15 + f"{average}({average_different_procent}%)" + " "*15 +\
                f"{closed_short_in_pure_usdt}" + " "*15 + f"{total_position}" + " "*15 + f"{sum_of_parts}"
            print(s)
            i += 1

    def stata_short_v2(self):
        i = 0.5
        body = self.A
        sum_money = 0
        step = 0.5
        price = 500
        short_position = 20
        average_short_price = self.start_price
        steps = 322

        while i < steps:
            price = (1 - step/100) * price
            newA, newB, medial_price = self.pool_proporsions_for_price(price, show_info=False)
            deltaA = (newA/self.A - 1) * 100
            deltaB = (newB / self.B - 1) * 100
            part_to_buy = newA - body

            sum_money += part_to_buy * price
            body += part_to_buy
            parts = newA - self.A
            average = sum_money / parts

            self.average_short_price = (sum_money + self.B) / (parts + self.A)

            average_different_procent = ((medial_price/average) - 1) * 100

            total_position = (-1 * (
                        price / self.average_short_price - 2) * (self.B + sum_money)) + newA * price + newB - sum_money

            total_position = (-1 * (
                    price / self.average_short_price - 2) * (newA * self.average_short_price)) + newA * price + newB - sum_money

            '''price = round(price, 2)
            newA = round(newA, 4)
            newB = round(newB, 2)'''
            part_to_buy = round(part_to_buy, 4)
            deltaA = round(deltaA, 2)
            deltaB = round(deltaB, 2)
            medial_price = round(medial_price, 3)

            average = round(average, 3)
            average_different_procent = round(average_different_procent, 3)


            s = f"(-{step}%){price}:" + " "*15 + f"{newA}({deltaA}%)" + " "*15 + f"{newB}({deltaB}%)" + " "*15 + f"{medial_price}" + " "*15 + f"{part_to_buy}" + " "*15 + f"{average}({average_different_procent}%)" + " "*15 + f"{sum_money}" + " "*15 + f"{total_position}"+ \
                " "*15 + f"{self.average_short_price}"
            print(s)
            i += 1




if __name__ == '__main__':
    il = IL()
    print(il.get_new_A(529))
    #il.pool_proporsions_for_price(497.4875624999999)
    #il.pool_proporsions_for_price(100)
    #il.stata_grow()
    #il.stata_short_v2()
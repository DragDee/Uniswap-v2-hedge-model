import websocket
import threading
from prototype2 import Trading, Short, trading
from main import IL

class SocketConn(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(url=url, on_open=self.on_open)

        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, e: print('Error', e)
        self.on_close = lambda ws: print("Closing")

        self.run_forever()

    def on_open(self, ws):
        print('Websocket was opened')

    def message(self, msg):

        print(msg)
        a = msg.split(',')
        price = a[3].split(':')[1]
        price = float(price[1:-1])
        print(price)


        trading.main_f(price)


il = IL(start_price=536)
short = Short(il)
trading = Trading(il, short)
threading.Thread(target=SocketConn, args=('wss://fstream.binance.com:443/ws/bnbusdt@markPrice', )).start()
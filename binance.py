import base64
import hashlib
import hmac

import requests
import time
from key import API_KEY, PRVT_KEY


class BinanceTrading:
    api_key = API_KEY
    prvt_key = PRVT_KEY
    base_endpoint = 'https://fapi.binance.com/'
    #base_endpoint = 'https://testnet.binancefuture.com/'
    new_order_endpoint = 'fapi/v1/order'
    mark_price = 'fapi/v1/premiumIndex'
    cancel_all_orders_endpoint = 'fapi/v1/allOpenOrders'

    def hashing(self, query_string):
        return hmac.new(self.prvt_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_price(self, symbol):
        params = {
            'symbol': symbol,
        }
        response = requests.get(self.base_endpoint + self.mark_price, data=params)
        print(response.json())
        try:
            res = float(response.json()['markPrice'])
            return res
        except:
            return "Error"

    def transaction(self, params, add_endpoint, request_method='post'):
        params['timestamp'] = int(time.time() * 1000)
        payload = '&'.join([f'{param}={value}' for param, value in params.items()])
        params['signature'] = self.hashing(payload)

        # Send the request
        headers = {
            'X-MBX-APIKEY': API_KEY,
        }
        method = getattr(requests, request_method)
        response = method(
            self.base_endpoint + add_endpoint,
            headers=headers,
            data=params,
        )
        print(response.json())

    def open_order(self, symbol, side, type, quantity, price):
        params = {'symbol': symbol,
                  'side': side,
                  'type': type,
                  'timeInForce': 'GTC',
                  'quantity': quantity,
                  'price': price,
                  }

        self.transaction(params, self.new_order_endpoint)

    def open_market_order(self, symbol, side, quantity, type='MARKET'):
        params = {'symbol': symbol,
                  'side': side,
                  'type': type,
                  'quantity': quantity,
                  }

        self.transaction(params, self.new_order_endpoint)

    def open_stop_order(self, symbol, side, quantity, price, stop_price):
        params = {'symbol': symbol,
                  'side': side,
                  'type': 'STOP',
                  'timeInForce': 'GTC',
                  'quantity': quantity,
                  'price': price,
                  'stopPrice': stop_price,
                  }

        self.transaction(params, self.new_order_endpoint)


    def close_order(self, symbol, orderId):
        params = {'symbol': symbol,
                  'orderId': orderId
                  }

        self.transaction(params, self.new_order_endpoint, request_method='delete')

    def cancel_all_orders(self, symbol):
        params = {'symbol': symbol,
                  }

        self.transaction(params, self.cancel_all_orders_endpoint, request_method='delete')

if __name__ == '__main__':
    binance = BinanceTrading()
    #binance.open_market_order('BNBUSDT', 'BUY', 0.01)
    #binance.close_order('BTCUSDT', 395557978920)
    #binance.open_stop_order('BNBUSDT', 'BUY', 0.01, 600, stop_price=599)
    #print(binance.get_price('BTCUSDT'))
    binance.cancel_all_orders('BNBUSDT')


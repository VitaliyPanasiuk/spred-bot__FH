import hashlib
import hmac
import requests
import time

def sign_data(key: str, data: dict, utc_now: str) -> str:
    if data: sorted_data = sorted(data.items())
    else: sorted_data = {}

    msg = ''.join(
        str(v) for k, v in sorted_data
        if not isinstance(v, (dict, list, type(None)))
    ) + str(utc_now)
    msg = msg.lower()

    return hmac.new(key.encode(), msg.encode(), hashlib.sha512).hexdigest()

data = {
    "method": "invoice.create",
    "params": {"in_curr": "BTC","amount": "11","externalid": "spred-bot","comment": "test payment","lifetime": "15m"},
    "jsonrpc": "2.0",
    "id": "1"
}

MERCHANT = 'spred-bot'
API_KEY = 'OY8ZLrBNqhmN8xnl8zNbeqjHCn3EwoFVL7YPxJVy2Oj87PkCRJ35yWeNAzdRkozz5fmI'
utc_now = str(int(time.time() * 1000))


headers = {
    "x-merchant": MERCHANT,
    "x-signature": sign_data(API_KEY, data.get('params') or {}, utc_now),
    "x-utc-now-ms": utc_now
}

response = requests.post(url='https://api.any.money/', json=data, headers=headers)
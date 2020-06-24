# [LNPAY](https://lnpay.co)

![Image](https://i.imgur.com/tsUtsvx.png)

[Buy me a coffee ☕︎](https://paywall.link/to/donate)

Lnpay is a payment service that uses the Bitcoin Lightning Network as a base, this library written in Python v 3.8 allows you to interact with the platform API in an easy and simple way.

#### Wallet
- [x] Create
- [x] Balance
- [x] Transactions
- [x] New Invoice
- [x] Pay Invoice
- [x] Transfer
- [x] Lnurl Withdraw

#### Lntx

- [x] Transaction Status

#### Paywall
- [x] Create

## Instalation
##### (Lnpay)  requires [ Python ](https://www.python.org) v3.8

```sh
$ pip install Lnpay
```

#### Getting Started

```python
Python 3.8.3 (default, Jun 16 2020, 19:00:28)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import Lnpay
>>> 
>>> Public = Lnpay.Public()
>>> 
>>> Public.importkey('pak_zWl ...')
>>> 
```

#### Wallet

- Create a new wallet and corresponding access keys.

```python
>>> Wallet = Lnpay.Wallet()
>>> Create = Wallet.create('Hello Word')
>>> Create
{'id': 'wal_ ...', 'created_at': 9352251, 'updated_at': 9352251, 'user_label': 'Hello Word!', 'balance': 0, 'statusType': {'type': 'wallet', 'name': 'active', 'display_name': 'Active'}, 'access_keys': {'Wallet Admin': ['waka_ ...'], 'Wallet Invoice': ['waki_ ...'], 'Wallet Read': ['wakr_ ...']}}
```

- Importing the keys from the wallet. You can import an existing wallet just by passing a tuple or a dictionary.

```python
>>> Wallet.importkeys(Create)
('waka_ ...', 'waki_ ...', 'wakr_ ...', 'wal_ ...')
>>>
>>> Wallet.importkeys(('waka_ ...', 'waki_ ...', 'wakr_ ...', 'wal_ ...'))
('waka_ ...', 'waki_ ...', 'wakr_ ...', 'wal_ ...')
>>>
>>> Wallet.importkeys({'blabla1' : 'waka_ ...', 'blabla2' : 'waki_ ...', 'blabla3' : 'wakr_ ...', 'blabla4' , 'wal_ ...'})
('waka_ ...', 'waki_ ...', 'wakr_ ...', 'wal_ ...')
>>>
```

- Returns info about the wallet, including balance

```python
>>> Wallet.balance()
{'id': 'wal_ ...', 'created_at': 999999, 'updated_at': 999999, 'user_label': 'Hello Word!', 'balance': 1, 'statusType': {'type': 'wallet', 'name': 'active', 'display_name': 'Active'}}
```
- Get a list of wallet transactions that have been SETTLED. This includes only transactions that have an impact on wallet balance. These DO NOT include unsettled/unpaid invoices.

```python
>>> Wallet.transactions()
[]
```

- Generate a Lightning payment invoice.

```python
>>> Wallet.newinvoice(1, passthru={'name' : 'alex', 'id' : 1}, memo='Hello Word!', expiry=86400)
{"id": "lntx_ztkK7XxfqCq3ihmhJiUhnR" ...}
```

- Pay an invoice from this wallet.

```python
>>> Wallet.payinvoice('lnbc....', passthru={'message' : 'payment to Aunt Maria.'})
{"id": "wtx_dYeWXmMTrP1VH8XZMOhXdE1", ...}
```

- Transfer satoshis from source wallet to destination wallet.

```python
>>> Wallet.transfer('wal_ ...', 1, memo='Transferring to another account.', passthru={'in' : 'Me', 'to' : 'Maria.'}):
{"wtx_transfer_in": { ... } ...}
```

- Generate an LNURL-withdraw link. 

```python
>>> lnurlwithdraw(50000, passthru={'message' : 'I need to withdraw to buy vegetables.'}, memo='Withdrawing my dear money.'):
{"lnurl":"LNURL ... VGhlcmUncyBub3RoaW5nIGhlcmUgOik=", "ott":"Y241"}
>>> # Do not read what is in base64 :(
```

#### Lntx

- Get Invoice Status.

```python
>>> Node = Lnpay.Lntx()
>>> Node.status('lntx_82yve ...')
{"id" : "lntx_82yveCX2Wn0EkkdyzvyBv", "created_at" : 1577657602, "updated_at" : 1577657602 ...}

```

#### Paywall

- Create Paywall.

```python
>>> Paywall = Lnpay.Paywall()
>>>
>>> Paywall.create('https://lnpay.co', 1, customlink='325415', memo='Hello Word!', linkexpiry='ONE_TIME_USE')
{"id" : "pywl_bI0OuKNxLtMHWs", "created_at" : 1586448191, "updated_at" : 1586448191 ... }
```

##### Link Expiration Rules

These rules control the short link functionality. They work by using a cookie to keep track of the user. 
Example: if a user pays a paywall with 6_HR, whenever they click on the paywall link - they are redirected to the destination automatically until after 6 Hours from original purchase time. At that point they are presented with the paywall again.

| Link Expiry   | Description   |
| ------------- |:-------------:|
| IMMEDIATE     | Payer must pay every time |
| 6_HR          | Payer has access for 6 hours |
| 1_D           | Payer has access for 1 Day |
| 30_D          | Payer has access for 30 Days |
| 90_D          | Payer has access for 90 Days |
| ONE_TIME_USE  | Once the link is paid one time by anyone, it is no longer valid for anyone|


#### Node

```python
>>> Node = Lnpay.Node()
>>> Node.decodeinvoice('lnbc690 ...')
{"destination" : "", "payment_hash" : "", "num_satoshis" : "69" ... }
```

Thanks <3

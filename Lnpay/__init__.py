#!/usr/bin/python3.8

import requests
import json

logged = [{'status' : None}]

def Push(path, method='GET', data=None, auth=None):

    url = 'https://lnpay.co/v1' + path

    if method == 'GET':
        return requests.get(url, data=data, auth=auth)

    if method == 'POST':
        return requests.post(url, data=data, auth=auth)

class Public:

    def importkey(self, public):

        global logged

        if public[:3] != 'pak':
            raise ValueError('Public API Key is invalid.')

        logged[0] = {'status' : True, 'public_api_key' : public}

class Wallet:

    def __init__(self):

        self.walletkeys = {'wallet_id' : None, 'wallet_admin' : None, 'wallet_invoice' : None, 'wallet_read' : None}

        if logged[0]['status'] == None:
            raise ValueError('Public api key not imported.')

        self.auth = (logged[0]['public_api_key'], logged[0]['public_api_key'])

    def importkeys(self, *keys):

        if type(keys[0]) == dict:

            if 'access_keys' in keys[0].keys():

                access = keys[0]['access_keys']
                keys = (keys[0]['id'], access['Wallet Admin'][0], access['Wallet Invoice'][0], access['Wallet Read'][0])

            else:

                keys = tuple(keys[0].values())

        for key in keys:

            if key[:3] == 'wal':
                self.walletkeys.update({'wallet_id' : key})

            elif key[:4] == 'waka':
                self.walletkeys.update({'wallet_admin' : key})

            elif key[:4] == 'waki':
                self.walletkeys.update({'wallet_invoice' : key})

            elif key[:4] == 'wakr':
                self.walletkeys.update({'wallet_read' : key})

        return self.walletkeys

    def create(self, label):

        return Push('/wallet', method='POST', data={'user_label' : label}, auth=self.auth).json()

    def balance(self):

        if self.walletkeys['wallet_read'] == None:
            raise ValueError('Read key not found.')

        return Push('/wallet/' + self.walletkeys['wallet_read'], auth=self.auth).json()

    def transactions(self):

        if self.walletkeys['wallet_read'] == None:
            raise ValueError('Read key not found.')

        return Push('/wallet/{0}/transactions'.format(self.walletkeys['wallet_read']), auth=self.auth).json()

    def newinvoice(self, amount, passthru=None, memo=None, expiry=None):

        if self.walletkeys['wallet_invoice'] == None:
            raise ValueError('Key to generate invoice not found.')

        data = {}

        if passthru != None and type(passthru) == dict:

            passthru = json.dumps(passthru)
            data.update({'passThru' : passthru})

        if memo != None:
            data.update({'memo' : memo})

        if expiry != None and str(expiry).isnumeric() == True:

            data.update({'expiry' : expiry})

        if str(amount).isnumeric() == True:

            data.update({'num_satoshis' : amount})
            return Push('/wallet/{0}/invoice'.format(self.walletkeys['wallet_invoice']), method='POST', data=data, auth=self.auth).json()

        raise ValueError('Amount is not a number.')

    def payinvoice(self, invoice, passthru=None):

        if self.walletkeys['wallet_admin'] == None:
            raise ValueError('Admin key not found.')

        data = {}

        if passthru != None and type(passthru) == dict:

            passthru = json.dumps(passthru)
            data.update({'passThru' : passthru})

        if str(invoice[:4]) == 'lnbc':

            data.update({'payment_request' : invoice})
            return Push('/wallet/{0}/withdraw'.format(self.walletkeys['wallet_admin']), method='POST', data=data, auth=self.auth).json()

        raise ValueError('Invoice not valid.')

    def transfer(self, dest_wallet_id, amount, memo=None, passthru=None):

        if self.walletkeys['wallet_admin'] == None:
            raise ValueError('Admin key not found.')

        data = {}

        if passthru != None and type(passthru) == dict:

            passthru = json.dumps(passthru)
            data.update({'passThru' : passthru})

        if memo != None:
            data.update({'memo' : memo})

        if str(amount).isnumeric() == True:

            if dest_wallet_id[:3] == 'wal':

                data.update({'dest_wallet_id' : dest_wallet_id, 'num_satoshis' : amount})
                return Push('/wallet/{0}/transfer'.format(self.walletkeys['wallet_admin']), method='POST', data=data, auth=self.auth).json()

            raise ValueError('Invalid wallet id.')

        raise ValueError('Amount is not a number.')

    def lnurlwithdraw(self, amount, passthru=None, memo=None):

        if self.walletkeys['wallet_admin'] == None:
            raise ValueError('Admin key not found.')

        if str(amount).isnumeric() == True:

            query = '/wallet/{0}/lnurl/withdraw?num_satoshis={1}'.format(self.walletkeys['wallet_admin'], amount)

            if passthru != None and type(passthru) == dict:
                query += '&passThru=' + json.dumps(passthru)

            if memo != None:
                query += '&passThru=' + str(memo)

            return Push(query, auth=self.auth).json()

class Lntx:

    def __init__(self):

        if logged[0]['status'] == None:
            raise ValueError('Public api key not imported.')

        self.auth = (logged[0]['public_api_key'], logged[0]['public_api_key'])

    def status(self, lntx_id):

        if lntx_id[:4] == 'lntx':
            return Push('/lntx/{0}'.format(lntx_id), auth=self.auth).json()

        raise ValueError('Invalid transaction id.')

class Paywall:

    def __init__(self):

        if logged[0]['status'] == None:
            raise ValueError('Public api key not imported.')

        self.auth = (logged[0]['public_api_key'], logged[0]['public_api_key'])

    def create(self, url, amount, customlink=None, memo=None, linkexpiry=None):

        if not str(linkexpiry).upper() in ['IMMEDIATE', 'NO_EXP', '6_HR', '1_D', '30_D', '90_D', 'ONE_TIME_USE']:
            raise ValueError('The value in linkexpiry does not match any of that list (IMMEDIATE, NO_EXP, 6_HR, 1_D, 30_D, 90_D, ONE_TIME_USE)')

        data = {}

        if customlink != None:
            data.update({'short_url' : customlink})

        if memo != None:
            data.update({'memo' : memo})

        if linkexpiry != None:
            data.update({'link_rule_exp_id' : linkexpiry})

        if str(amount).isnumeric() == True:

            data.update({'num_satoshis' : amount, 'destination_url' : url})
            return Push('/paywall', method='POST', data=data, auth=self.auth).json()

        raise ValueError('Amount is not a number.')

class Node:

    def __init__(self):

        if logged[0]['status'] == None:
            raise ValueError('Public api key not imported.')

        self.auth = (logged[0]['public_api_key'], logged[0]['public_api_key'])

    def decodeinvoice(self, invoice):

        if str(invoice[:4]) == 'lnbc':

            query = '/node/default/payments/decodeinvoice?payment_request={0}'.format(invoice)

            return Push(query, auth=self.auth).json()


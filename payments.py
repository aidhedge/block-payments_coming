import datetime
import json
import os
from ah_requests import AhRequest
from exceptions import NoAPIKeyPresent
from logger import Logger
LOG = Logger()
ah_request = AhRequest()

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY', None)
if not CURRENCY_API_KEY:
    raise NoAPIKeyPresent("Can't find 'CURRENCY_API_KEY' in the env variables", status_code=500) 

def get_risk_by_date(_list,pair,date):
    return [r for r in _list if r['date'] == date and r['pair'] == pair][0]['risk'] 

# How much is the increase/decrease (in %) from one number(start) 
# to another (end)
def percent_diff(start,end):
    result = 100*(end / start)-100
    return round(result, 3)

# Whats is the amount when increased/decreased by X% (pct)
def pct_change(number, pct):
    result = number*(pct/100)
    return round(result, 3)

def today(d=None):
    today = datetime.date.today()
    if d:
        datum = today + datetime.timedelta(days=d)
        return datum.strftime('%Y-%m-%d')
    else:
        return today.strftime('%Y-%m-%d')

def queryCurrencyApi(pair, date):
    url = "http://www.apilayer.net/api/historical?access_key={}&source={}&currencies={}&date={}".format(CURRENCY_API_KEY, pair[:3], pair[3:],date)
    #LOG.console(url)
    res = ah_request.get(url=url)
    res = res.json()
    return float(res['quotes'][pair])
    

def result(data):
    payload = data['project_data']
    risk = data['risk']
    project_start = payload['project_start']
    todays_date = today()
    data = []
    for t in payload["transactions"]:
        obj = {}
        currency_from = t["currency_from"]
        currency_to = t["currency_to"]
        pair = currency_from+currency_to
        obj['direction'] = t['direction']
        obj['pair'] = pair
        obj['uuid'] = t['uuid']
        if 'fixed_rate' in t:
            obj["project_start_rate"] = float(t['fixed_rate'])
            obj["todays_rate"] = float(t['fixed_rate'])
        else:
            if t['start'] >= todays_date:
                obj["project_start_rate"] = queryCurrencyApi(pair=pair, date=today())
                obj["todays_rate"] = queryCurrencyApi(pair=pair, date=today())
            else:
                obj["project_start_rate"] = queryCurrencyApi(pair=pair, date=project_start)
                obj["todays_rate"] = queryCurrencyApi(pair=pair, date=today())
        obj['payments'] = []
        for p in t["payments"]:
            if p['date'] > todays_date: # Har projektet ens startat
                pct_diff = percent_diff(start=obj["project_start_rate"], end=obj["todays_rate"])
                pct_risk = get_risk_by_date(_list=risk, pair=pair, date=p['date'])
                if t['direction'] == 'in':
                    obj["payments"].append(dict(date=p['date'],pct_risk=pct_risk, pct_diff_since_start=pct_diff, amount=p['amount']*obj["project_start_rate"]))
                else:
                    obj["payments"].append(dict(date=p['date'],pct_risk=pct_risk, pct_diff_since_start=pct_diff, amount=p['amount']))

        data.append(obj)
    return data  
       


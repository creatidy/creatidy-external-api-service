import os
import jwt
from datetime import datetime, timezone
import requests
import json
import mysql.connector

EXANTE_ID = os.getenv('EXANTE_ID')
EXANTE_APP = os.getenv('EXANTE_APP')
EXANTE_KEY = os.getenv('EXANTE_KEY')
MODE = "live"

now = int(datetime.now(tz=timezone.utc).timestamp())

payload = {
    'iss': EXANTE_ID,
    "sub": EXANTE_APP,
    "iat": now,
    "exp": now + 3600,
    "aud": ["transactions"]
}
encoded_jwt = jwt.encode(payload, EXANTE_KEY, algorithm="HS256")

api_data_endpoint = f'https://api-{MODE}.exante.eu'

params = {
    'fromDate': '2022-01-01',
    'toDate': '2022-01-03'
}
request = requests.Request('GET', f'{api_data_endpoint}/md/3.0/transactions', data=params)

prepped = request.prepare()
prepped.headers['Accept'] = 'application/json'
prepped.headers['Authorization'] = f"Bearer {encoded_jwt}"

with requests.Session() as session:
    response = session.send(prepped)
    parsed = json.loads(response.text)

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='creatidy')

for r in parsed:
    cursor = cnx.cursor()
    print('INSERT: {data}'.format(data=r))
    query = ("INSERT INTO exante "
             "   (symbolId, orderId, operationType, uuid, orderPos, accountId, id, asset, when_ts, sum_dec) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), %s)")
    cursor.execute(query, (r['symbolId'], r['orderId'], r['operationType'], r['uuid'], r['orderPos'], r['accountId'], r['id'], r['asset'], r['when']/1000, r['sum']))
    cnx.commit()
    cursor.close()

cnx.close()
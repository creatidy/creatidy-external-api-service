import os
import hvac
import jwt
import datetime
import requests
import json
import mysql.connector

TOKEN = os.getenv('VAULT_TOKEN')
MODE = "live"

client = hvac.Client(url='http://localhost:8200', token=TOKEN)
secrets = client.secrets.kv.v1.read_secret(path=MODE, mount_point="hvac-kv")

ct = datetime.datetime.now()
ts = int(ct.timestamp())

payload = {
    'iss': secrets['data']['client-id'],
    "sub": secrets['data']['app-id'],
    "iat": ts,
    "aud": ["transactions"]
}
encoded_jwt = jwt.encode(payload, secrets['data']['secret'], algorithm="HS256")

api_data_endpoint = f'https://api-{MODE}.exante.eu/md/2.0'

params = {
    'version': '2.0'
}
request = requests.Request('GET', f'{api_data_endpoint}/transactions', data=params)

prepped = request.prepare()
prepped.headers['accept'] = 'application/json'
prepped.headers['Authorization'] = "Bearer " + encoded_jwt

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

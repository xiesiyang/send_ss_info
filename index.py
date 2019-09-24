import json
from urllib import request, parse
import base64
import os


ip_url = os.getenv("GET_IP_URL")
ifttt_maker_key = os.getenv("IFTTT_MAKER_KEY")
file_path = os.getenv("FILE_PATH")
ifttt_event_name = os.getenv("IFTTT_EVENT_NAME")

if ip_url is None or ifttt_maker_key is None or file_path is None or ifttt_event_name is None:
    raise BaseException('please check environment  GET_IP_URL , IFTTT_MAKER_KEY ,FILE_PATH,IFTTT_EVENT_NAME')

f = open(file_path, mode='r')
info = json.load(f)
f.close()

method = info['method']

password = info['password']
port = str(info['server_port'])

print('method:'+method)
print('password:'+password)
print('port:'+port)

print('prepare to get out ip')
ip_req = request.urlopen(ip_url)
ip = ip_req.read().decode()
print('ip:'+ip)

origin_info = method + ':' + password + '@' + ip + ':' + port
print('origin ss info:'+origin_info)
_info = 'ss://' + str(base64.b64encode(origin_info.encode('utf-8')), 'utf-8').replace('-', '+').replace("_", '/')
print('ss url '+_info)



data_json = parse.urlencode({
    "value1": _info
})
ifttt_maker_url = "https://maker.ifttt.com/trigger/"+ifttt_event_name+"/with/key/"+ifttt_maker_key
req = request.Request(ifttt_maker_url)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print('prepare to send msg ')
with request.urlopen(req, data=data_json.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))

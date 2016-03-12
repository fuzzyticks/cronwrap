import json
import requests
import salt.client
from flask import Flask, request

app = Flask(__name__, static_folder='', static_url_path='')
es_url = 'http://192.168.56.1:9200/crondb/cronwrap/'
local = salt.client.LocalClient()

@app.route('/')
def hello():
  return "Hello! :)"

@app.route('/esjson/<esquery>')
def getjson(esquery):
  query =  ' { "query" : { "query_string": { "query": "' + esquery + '" } } }'
  app.logger.debug(query)
  res = requests.post(es_url + '_search?&size=50', data = query)
  res = json.loads(res.content)
  d=[]
  for i in res['hits']['hits']:
    d.append(i.get('_source'))

  return(json.dumps(d))

@app.route('/stuckcrons')
def stuckcronlist():
  query = '{ "query" : { "query_string": { "query": "0", "fields": ["end_time"] } } }'
  app.logger.debug(query)
  res = requests.post(es_url + '_search', data = query)
  res = json.loads(res.content)
  d=[]
  for i in res['hits']['hits']:
    d.append(i.get('_source'))

  return(json.dumps(d))

@app.route('/deletecron', methods=['post'])
def deletecron():
  hostname = request.form['hostname']
  userid = request.form['userid']
  cronjobitem = request.form['cronjob']

  crondel = local.cmd(hostname, 'cron.rm_job', [userid, cronjobitem])
  app.logger.debug(crondel)

  if(crondel[hostname] == 'removed'):
    app.logger.debug("msg rem -: " + crondel[hostname])
    return "Removed Sucessfully"
  elif(crondel[hostname] == 'absent'):
    app.logger.debug("msg abs -: " + crondel[hostname])
    return "Error -: Cron Absent!!"
  else:
    app.logger.debug("msg unkon -: " + crondel[hostname])
    return "Known error, please ask admin to check"

@app.route('/cronlist', methods=['post'])
def getcrons():
  app.logger.debug(request.form)

  if len(request.form) == 0:
    return("false")

  hostname = request.form['hostname']
  userid = request.form['userid']
 
  crons = local.cmd(hostname, 'cron.list_tab', [userid])
  app.logger.debug(crons)

  if len(crons) == 0 or len(crons[hostname]['crons']) == 0:
    return("false")  
  else:
    crons_list = crons[hostname]['crons']
    return(json.dumps(crons_list))

@app.route('/addcron', methods=['post'])
def addcron():
  app.logger.debug("Add cron section :")
  app.logger.debug(request.form)

  hostnames = request.form['hostnames']
  userid = request.form['userid']
  cronjob = request.form['cronjob']
  cjmin = request.form['cjmin']
  cjhour = request.form['cjhour']
  cjday = request.form['cjday']
  cjmonth = request.form['cjmonth']
  cjweekday = request.form['cjweekday']
 
  cronjobadd = local.cmd(hostnames, 'cron.set_job', [userid, cjmin, cjhour, cjday, cjmonth, cjweekday, cronjob])

  if len(cronjobadd) == 0:
    return "Hostname : " + hostnames +  "not accessible / reachable"
  elif cronjobadd[hostnames] == 'new' or cronjobadd[hostnames] == 'updated':
    app.logger.debug("Message from salt : " + cronjobadd[hostnames])
    return "!!! Cron Added sucessfully"
  else:
    app.logger.debug("Message from salt : " + cronjobadd[hostnames])
    return(cronjobadd[hostnames])
  
if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.56.101')

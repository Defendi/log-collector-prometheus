from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import time
import subprocess
import datetime
import select

filename='/var/log/odoo/odoo-server.log'
VLTIMER=1

# Create a metric to track time spent and requests made.
# INFO_LOG = Info('nifi_logs_application', 'Envio dos logs do Nifi para o prometheus')
f = subprocess.Popen(['tail','-F',filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

def ConvertStrToDateTime(value):
    milliseconds = int(value[-3:])
    res = datetime.datetime.strptime(value[:-4], "%Y-%m-%d%H:%M:%S")
    res = res.replace(microsecond=milliseconds * 1000)
    return res

def ConvertToDict(linha):
    chavein = linha.find('[')
    chaveout = linha.find(']',chavein)
    levelout = linha.find(' ', 24)
    operin = chaveout + 2
    operout = linha.find(' ', operin)
    
    return {
        'Date': linha[0:10],
        'Time': linha[11:23],
        'Level': linha[24:levelout],
        'type': linha[chavein+1:chaveout],
        'operation': linha[operin:operout],
        'text': linha[operout+1:-2]
    }

def AppendLines():
    res = {
        'Date': "",
        'Time': "",
        'Level': "",
        'type': "",
        'operation': "",
        'text': ""
    }

    with open(filename, 'r') as arquivo:
        for linha in arquivo:
            stline = ConvertToDict(linha)
            if bool(stline.get('Date',False)) and bool(stline.get('Time',False)):
                res = stline
    return res
 
class CustomCollector(object):
    def __init__(self):
        self.last_line = AppendLines()
        self.f = subprocess.Popen(['tail','-F',filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.p = select.poll()
        self.p.register(self.f.stdout)

    def collect(self):
        list_of_metrics = []
        DateTimeLs = ConvertStrToDateTime(self.last_line['Date']+self.last_line['Time']) 
        while p.poll(1):
            linha = f.stdout.readline().decode('utf-8')
            Linha = ConvertToDict(linha)
            try:
                DateTimeLn = ConvertStrToDateTime(Linha['Date']+Linha['Time'])
                if DateTimeLn > DateTimeLs:
                    print(Linha)
                    var = {
                        "appname": linha,
                        "value": "0"
                    }
                    list_of_metrics.append(var)
                    Linha = var
            except:
                pass
        
        for key in list_of_metrics:
            g = GaugeMetricFamily("nifi_logs_application", 'Envio dos logs do Nifi para o prometheus', labels=['logs'])
            g.add_metric([str(key['appname'])], key['value'])
            yield g
        time.sleep(1)
            
if __name__ == '__main__':
    start_http_server(19994)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)

# # Decorate function with metric.
# def process_request(f,last_line):
#     DateTimeLs = ConvertStrToDateTime(last_line['Date']+last_line['Time']) 
#     while True:
#         linha = f.stdout.readline().decode('utf-8')
#         Linha = ConvertToDict(linha)
#         try:
#             DateTimeLn = ConvertStrToDateTime(Linha['Date']+Linha['Time'])
#             if DateTimeLn > DateTimeLs:
#                 print(Linha)
#                 INFO_LOG.info(Linha)
#                 last_line = Linha
#         except:
#             pass
    
# if __name__ == '__main__':
#     # last_line = AppendLines()
#     # # Start log file tail
#     # f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     # # Start up the server to expose the metrics.
#     # start_http_server(19994)
#     # # Generate some requests.
#     # process_request(f,last_line)
#     start_http_server(19994)
#     REGISTRY.register(CustomCollector())
#     while True:
#         time.sleep(1)
#

        
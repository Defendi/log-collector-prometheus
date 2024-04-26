from prometheus_client.core import GaugeMetricFamily, REGISTRY, InfoMetricFamily
from prometheus_client import start_http_server
import time
import subprocess
import datetime
import select
import logging

logging.basicConfig(filename='collector.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# _logger = logging.getLogger('collector')

#filename='/var/log/odoo/odoo-server.log'
filename='/opt/nifi/nifi-current/logs/nifi-app.log'

VLTIMER=1

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
        for idx, line in enumerate(arquivo):
            stline = ConvertToDict(line)
            if idx == 0:
                res = stline
            # if bool(stline.get('Date',False)) and bool(stline.get('Time',False)):
            #     res = stline
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
        while self.p.poll(1):
            linha = self.f.stdout.readline().decode('utf-8')
            if str(linha).find('alexandre') > 0:
                pass
            Linha = ConvertToDict(linha)
            try:
                DateTimeLn = ConvertStrToDateTime(Linha['Date']+Linha['Time'])
                if DateTimeLn > DateTimeLs:
                    logging.info(linha)
                    print(linha)
                    list_of_metrics.append(Linha)
                    self.last_line = Linha
                else:
                    pass
            except:
                pass
        
        for key in list_of_metrics:
            # g = GaugeMetricFamily("nifi_logs_application", 'Envio dos logs do Nifi para o prometheus', labels=['logs'])
            g = InfoMetricFamily("nifi_logs_application", 'Envio dos logs do Nifi para o prometheus', labels=['logs_line'])
            # g.add_metric(labels=[str(key['appname'])], key['value'])
            g.add_metric(['log'],key)
            yield g
        time.sleep(1)
            
if __name__ == '__main__':
    start_http_server(19994)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
        
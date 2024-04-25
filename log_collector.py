from prometheus_client import start_http_server, Info
import time
import subprocess
import datetime

filename='/var/log/odoo/odoo-server.log'
VLTIMER=1

# Create a metric to track time spent and requests made.
INFO_LOG = Info('nifi_logs_application', 'Envio dos logs do Nifi para o prometheus')

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
   

# Decorate function with metric.
def process_request(f,last_line):
    DateTimeLs = ConvertStrToDateTime(last_line['Date']+last_line['Time']) 
    while True:
        linha = f.stdout.readline().decode('utf-8')
        Linha = ConvertToDict(linha)
        try:
            DateTimeLn = ConvertStrToDateTime(Linha['Date']+Linha['Time'])
            if DateTimeLn > DateTimeLs:
                print(Linha)
                INFO_LOG.info(Linha)
                last_line = Linha
        except:
            pass
    
if __name__ == '__main__':
    last_line = AppendLines()
    # Start log file tail
    f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Start up the server to expose the metrics.
    start_http_server(19994)
    # Generate some requests.
    process_request(f,last_line)

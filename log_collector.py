from prometheus_client import start_http_server, Info
import random
import time
import subprocess
import select

FILENAME='/var/log/odoo/odoo-server.log'
VLTIMER=1

# Create a metric to track time spent and requests made.
INFO_LOG = Info('nifi_logs_application', 'Envio dos logs do Nifi para o prometheus')

#
f = subprocess.Popen(['tail','-F',FILENAME], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)


# Decorate function with metric.
def process_request(t):
    if p.poll(1):
        INFO_LOG.Info(f.stdout.readline())
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(19994)
    # Generate some requests.
    while True:
        process_request(VLTIMER)

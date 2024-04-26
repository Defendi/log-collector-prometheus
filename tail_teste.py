import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import requests
import json

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        # response = requests.get('https://api.test.com/v1/data', auth= ('abc@gg.com', 'xxrty'))
        d1 = {
            "app_metric": [
                {
                "appname": "2024-04-25 20:22:53,116 INFO [pool-7-thread-1] o.a.n.c.r.WriteAheadFlowFileRepository Initiating checkpoint of FlowFile Repository",
                "value": "0"
                },
                {
                "appname": "2024-04-25 20:22:53,116 INFO [pool-7-thread-1] o.a.n.c.r.WriteAheadFlowFileRepository Initiating checkpoint of FlowFile Repository",
                "value": "0"
                },
                {
                "appname": "2024-04-25 20:22:53,116 INFO [pool-7-thread-1] o.a.n.c.r.WriteAheadFlowFileRepository Initiating checkpoint of FlowFile Repository",
                "value": "0"
                },
                {
                "appname": "2024-04-25 20:22:53,116 INFO [pool-7-thread-1] o.a.n.c.r.WriteAheadFlowFileRepository Initiating checkpoint of FlowFile Repository",
                "value": "0"
                }
            ]
        }
        list_of_metrics = d1["app_metric"]
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
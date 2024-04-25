import time
import subprocess
import select

filename = '/var/log/odoo/odoo-server.log'

lines = []

with open(filename, 'r') as arquivo:
    for linha in arquivo:
        lines.append(linha)
        print(linha)

f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    line = f.stdout.readline().decode('utf-8')
    if line not in lines:
        print(line)
        lines.append(line)
    else:
        print('x')

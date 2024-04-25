import time
import subprocess
import select

filename = '/var/log/odoo/odoo-server.log'

var = 

lines = []


with open(filename, 'r') as arquivo:
    for linha in arquivo:
        chavein = linha.find('[')
        chaveout = linha.find(']',start=chavein)
        levelout = a.find(' ', 24)
        operin = levelout + 1
        operout = a.find(' ', operin)
        
        line = {
            'Date': linha[0:10],
            'Time': linha[11:23],
            'Level': linha[24:levelout],
            'type': linha[chavein+1:chaveout],
            'operation': linha[operin,operout]
            'text': linha[operout+1:]
        }
        
        lines.append(line)
        print(linha)

f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

while True:
    if p.poll(1):
        line = f.stdout.readline().decode('utf-8')
        if line not in lines:
            print(line)
            lines.append(line)
    else:
        time.sleep(1)

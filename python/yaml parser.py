import subprocess
import yaml
from yaml import Loader
from src.simulation import Simulation

document="""
simtime : 86400
workload : 
    path : '/Users/test/Desktop/Ahmed Nader/bachelor/AMTS/src/dataset/IoT_vehicleCount_7D_1S.csv'

orchestrator :
    min instances : 1
    max util : 1.0
    min util : 0.1
    ConcurrencyValue : 10000
hosts :
    - host :
        pes : 4
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000

    - host : 
        pes : 4
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000
    
    - host :
        pes : 4
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000

    - host : 
        pes : 4
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000

VMs :
    - VM :
        pes : 2
        MIPS : 4000
        RAM : 4000
        BW : 1000
        Storage : 1000
    
    - VM :
        pes : 2
        MIPS : 4000
        RAM : 4000
        BW : 1000
        Storage : 1000
    
    - VM :
        pes : 2
        MIPS : 4000
        RAM : 4000
        BW : 1000
        Storage : 1000
    
    - VM :
        pes : 2
        MIPS : 4000
        RAM : 4000
        BW : 1000
        Storage : 1000
"""
# stream = file('document.yaml', 'r')
y = yaml.load(document,Loader=Loader)

output = subprocess.check_output("java -jar AMTS python package/java/AMTS-1.0-jar-with-dependencies.jar")
print(str(output))

s = Simulation(y['simtime'])
list = s.Create_HostList()
workload = s.Create_Workload(y["workload"]['path'])
o = y["orchestrator"]
Orchestration = s.Create_Orchestrator(o['min instances'],o['max util'],o['min util'],o['ConcurrencyValue'])
Orchestration.setWorkLoad(workload.ParseCSV())
CPUMonitor = s.Create_CPUMonitor(False)

def hosts(y):
    for host in y:
        h=host['host']
        host = s.Create_Host(Pes=h['pes'],MIPS=h['MIPS'],RAM=h['RAM'],BW=h['BW'],Storage=h['Storage'])
        list.add(host)
    return list


datacenter = s.Create_Datacenter(hosts(y['hosts']))



def vms(y):
    for vm in y:
        v = vm['VM']
        vm = s.Create_Vm(MIPS=v['MIPS'],Pes=v['pes'],RAM=v['RAM'],BW=v['BW'],Storage=v['Storage'])
        Orchestration.submitVm(vm)
        CPUMonitor.add(vm)
    return

vms(y['VMs'])


s.start()
s.stop()



# def PrintTime(e):
#     print(e.getTime())

# s.addOnClickTickListener(PrintTime)

from tqdm import tqdm
from time import sleep
import yaml
from yaml import Loader
from src.simulation import Simulation
from subprocess import Popen, PIPE 

def parser():
    

    p =  Popen(['java','-jar','./java/AMTS-1.0-jar-with-dependencies.jar'], stdout=PIPE, bufsize=1, universal_newlines=True) 

    sleep(0.5)

    document="""

simtime : 86400.0
workload : 
    path : '/usr/src/AMTS/AMTS python package/java/ysb.csv'

orchestrator :
    min instances : 1
    max util : 1.0
    min util : 0.1
    ConcurrencyValue : 20000
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

VMs :
    - VM :
        pes : 4
        MIPS : 4000
        RAM : 16250
        BW : 1000
        Storage : 1000
    
    - VM :
        pes : 4
        MIPS : 4000
        RAM : 16250
        BW : 1000
        Storage : 1000
"""
    
    
    # document = file('document.yaml', 'r')
    y = yaml.load(document,Loader=Loader)
    SIM_TIME=y['simtime']


    s = Simulation(SIM_TIME)
    list = s.Create_HostList()
    workload = s.Create_Workload(path=y["workload"]['path'])
    o = y["orchestrator"]
    Orchestration = s.Create_Orchestrator(MinInstances=o['min instances'],maxutil=o['max util'],minutil=o['min util'],ConcurrencyValue=o['ConcurrencyValue'])
    Orchestration.setWorkLoad(workload.ParseCSV())
    CPUMonitor = s.Create_CPUMonitor(WriteToFile=True,path='/usr/src/AMTS/AMTS python package/python',ReportMI=100,ReportBW=100)
    

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
    
    pbar = tqdm(total=SIM_TIME,delay=0.1,unit_scale=True,unit_divisor=1)
    

    def currentstatus(e):
        pbar.update(0.1)
        
    
    s.addOnClickTickListener(currentstatus)
    s.start()
    
    s.stop_with_full_pbar(pbar,SIM_TIME)
    # s.stop(pbar)

    pbar.close()

parser()
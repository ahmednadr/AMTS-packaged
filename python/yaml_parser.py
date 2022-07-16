
from tqdm import tqdm
from time import sleep
import yaml
from yaml import Loader
from src.simulation import Simulation
from subprocess import Popen, PIPE 
import os
from importlib.util import find_spec
import glob

def _contains_jar(path):
    jar_file = path + "/AMTS-1.0-jar-with-dependencies.jar"
    jar_file_matches = glob.glob(jar_file)
    if len(jar_file_matches) > 0:
        return jar_file_matches[0]
    else:
        return None

def _find_java_module():
    try:
        current_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        source_dir = os.path.abspath(current_dir + "/../")
        build_target = glob.glob(source_dir + "/java/")
        if len(build_target) > 0:
            jar_path = _contains_jar(build_target[0])
            if jar_path != None:
              return jar_path

        module_home = os.path.dirname(find_spec("java_integration_lib").origin)

        jar_path = _contains_jar(module_home + "/jars")
        if jar_path != None:
            return jar_path
    except Exception as e:
        pass
    print("Could not find valid jar in current environment.")

def parser(document):
    

    p = Popen(['java','-jar',_find_java_module(),'>','out.txt'], stdout=PIPE, bufsize=1, universal_newlines=True) 

    sleep(0.5)

    
    
    # document = file('document.yaml', 'r')
    y = yaml.load(document,Loader=Loader)
    SIM_TIME=y['simtime']


    s = Simulation(SIM_TIME)
    list = s.Create_HostList()
    workload = s.Create_Workload(path=y["workload"]['path'])
    o = y["orchestrator"]
    Orchestration = s.Create_Orchestrator(maxutil=o['max util'],minutil=o['min util'],ConcurrencyValue=o['ConcurrencyValue'],MessageSize=o['message size'])
    Orchestration.setWorkLoad(workload.ParseCSV())
    CPUMonitor = s.Create_CPUMonitor(WriteToFile=True,path=y["metrics"]['path'],ReportBW=y["metrics"]['reportBW'])
    BWMonitor = s.Create_BWMonitor(WriteToFile=True,path=y["metrics"]['path'],ReportBW=y["metrics"]['reportBW'])


    def hosts(y):
        for host in y:
            h=host['host']
            host = s.Create_Host(Pes=h['pes'],MIPS=h['MIPS'],RAM=h['RAM'],BW=h['BW'],Storage=h['Storage'])
            list.add(host)
        return list


    datacenter = s.Create_Datacenter(hosts(y['hosts']))

    

    def vms(y):
        x = 1
        for vm in y:
            v = vm['VM']
            vm = s.Create_Vm(MIPS=v['MIPS'],Pes=v['pes'],RAM=v['RAM'],BW=v['BW'],Storage=v['Storage'])
            Orchestration.submitVm(vm)
            CPUMonitor.add(vm)
            BWMonitor.add(vm)
            x = vm
        return x

    vm1 = vms(y['VMs'])
    
    pbar = tqdm(total=SIM_TIME,delay=0.1,unit_scale=True,unit_divisor=1)
    

    def currentstatus(e):
        pbar.update(0.1)
    
    def moni(e):
        if(e.getTime()%100 != 0):
            return
        f = CPUMonitor.getVmCurrentpercentage(vm1)
    
    s.addOnClickTickListener(currentstatus)
    s.addOnClickTickListener(moni)
    s.start()
    
    s.stop_with_full_pbar(pbar,SIM_TIME)
    

    pbar.close()


document="""

simtime : 604600.0
workload : 
    path : '/usr/src/AMTS/AMTS python package/java/ysb.csv'
metrics:
    path : '/usr/src/AMTS/AMTS python package/python/metrics 1'
    reportBW: 0.1
orchestrator :
    max util : 1.0
    min util : 0.1
    ConcurrencyValue : 10000
    message size : 0.0032
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
        BW : 40
        Storage : 1000
    
    - VM :
        pes : 4
        MIPS : 4000
        RAM : 16250
        BW : 40
        Storage : 1000
"""

parser(document)
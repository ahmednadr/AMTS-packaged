import subprocess
from py4j.java_gateway import JavaGateway,CallbackServerParameters

class Simulation():
    
    def __init__(self,Termination_time:float):
        self.gateway = JavaGateway(
        callback_server_parameters=CallbackServerParameters())
        self.sim = self.gateway.Create_sim()
        if Termination_time > 0:
            self.sim.terminateAt(Termination_time)
        self.onClockTickListenerList = [] 
        self.gateway.registerListener(self)
        return
    
    def Create_Host(self,Pes:int,MIPS:int,RAM:int,BW:int,Storage:int):
        return self.gateway.Create_Host(Pes,MIPS,RAM,BW,Storage)

    def Create_Vm(self,MIPS:int,Pes:int,RAM:int,BW:int,Storage:int):
        return self.gateway.Create_Vm(MIPS,Pes,RAM,BW,Storage)

    def Create_Workload(self,path:str):
        return self.gateway.Create_Workload(path)
    
    def Create_Orchestrator(self,MinInstances:int):
        return self.gateway.Create_Orchestrator(self.sim,MinInstances)
    
    def Create_Orchestrator(self,MinInstances:int,maxutil:float,minutil:float,ConcurrencyValue:int):
        return self.gateway.Create_Orchestrator(self.sim,MinInstances,maxutil,minutil,ConcurrencyValue)
    
    def Create_CPUMonitor(self,WriteToFile:bool):
        return self.gateway.Create_CPUMonitor(self.sim,WriteToFile)

    def Create_HostList(self):
        return self.gateway.Create_HostList()
    
    def Create_Datacenter(self,HostList):
        return self.gateway.Create_Datacenter(self.sim,HostList)
    
    def Create_PythonBroker(self ,name:str):
        return self.gateway.Create_PythonBroker(self.sim, name)
    
    def Crate_PythonContainer(self,pes:int,minUtilization:float,maxUtilization:float,ConcurrencyValue:int):
        return self.gateway.Create_PythonContainer(pes, minUtilization,  maxUtilization, ConcurrencyValue )
    
    def addOnClickTickListener(self,method): #method must have signature (event)
        self.onClockTickListenerList.append(method)
        return
    
    def ListenerCall (self,method,event):
        method(event)
        return
    
    def onClockTick(self,event):
        for m in self.onClockTickListenerList:
            self.ListenerCall(m,event)
        return

    def start(self): #should start the jar file
        
        return self.sim.start() 
    
    def stop(self): #should stop the jar file then stop the gateway process
        self.gateway.close()
        self.gateway.stop()

    def __getattr__(self, name):
        def method(*args,**kwargs):
            return getattr(self.gateway,name)(*args,**kwargs)
        return method

    
    class Java:
        implements = ["com.company.src.SimController.Interfaces.Listeners.Listener"]
from abc import ABC, abstractmethod
from src.simulation import Simulation

class AbstractBroker(ABC):
    
    class java: #if faced with a problem might try to dynamiclly add this class in __init__
        implements=["com.company.src.SimController.Interfaces.Broker.PythonBrokerInterface"]

    def __init__(self,sim:Simulation,name:str):
        self.Java = sim.Create_PythonBroker(name)
        self.sim = sim
        self.Java.Submit_interface(self)
    
    @abstractmethod
    def defaultVmMapper(self,cloudlet):
        raise NotImplementedError("abstract method defaultVmMapper is not implemented")
    
    @abstractmethod
    def defaultDatacenterMapper(self,lastDatacenter,vm):
        raise NotImplementedError("abstract method defaultDatacenterMapper is not implemented")
    
    def __getattr__(self, name):
        def method(*args,**kwargs):
            return getattr(self.Java,name)(*args,**kwargs)
        return method

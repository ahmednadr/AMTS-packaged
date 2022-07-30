from abc import ABC, abstractmethod
from ..simulation import Simulation

class AbstractBroker(ABC):
    
    class java: #if faced with a problem might try to dynamiclly add this class in __init__
        implements=["com.company.src.SimController.Interfaces.Broker.PythonBrokerInterface"]

    def __init__(self, sim ,Min:float ,  Max:float ,  ConcurrencyValue:int ,  MessageSize:float):
        self.Java = sim.Create_PythonBrokerCreate_PythonBroker(Min ,  Max ,  ConcurrencyValue ,  MessageSize)
        self.sim = sim
        self.Java.Submit_interface(self)
    
    @abstractmethod
    def Run(event):
        pass
    
    def __getattr__(self, name):
        def method(*args,**kwargs):
            return getattr(self.Java,name)(*args,**kwargs)
        return method

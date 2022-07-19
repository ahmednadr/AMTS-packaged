from abc import ABC, abstractmethod
from src.simulation import Simulation as sim

class AbstractContainer(ABC):
    
    class java: #if faced with a problem mighr try to dynamiclly add this class in __init__
        implements=["com.company.src.SimController.Interfaces.Container.PythonContainerInterface"]

    def __init__(self,pes:int,minUtilization:float,maxUtilization:float,ConcurrencyValue:int,s:sim):
        self.pes = pes
        self.minUtilization = minUtilization
        self.maxUtilization = maxUtilization
        self.ConcurrencyValue = ConcurrencyValue
        self.sim = s
        self.Java = s.Create_PythonContainer( pes,  minUtilization,  maxUtilization,  ConcurrencyValue) 
        self.Java.Submit_interface(self)
    
    @abstractmethod
    def CPUUpdateUtilization(self,utilizationModelDynamic):
        return NotImplementedError()
    
    @abstractmethod
    def BWUpdateUtilization(self,utilizationModelDynamic):
        return NotImplementedError()
    
    @abstractmethod
    def Clone(self):
        return NotImplementedError()
    
    def __getattr__(self, name):
        def method(*args,**kwargs):
            return getattr(self.Java,name)(*args,**kwargs)
        return method

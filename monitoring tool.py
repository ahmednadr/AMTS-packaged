from python.yaml_parser import parser
# from darts.models import RNNModel
import pandas as pd
import numpy as np

MODEL_INPUT_LENGTH = 100
MODEL_OUTPUT_LENGTH = 36
STD_THERSHOLD = 0.05
LAST_PREDICTION_TIME = 0.0

document="""

simtime : 600000.0
workload : 
    path : '/usr/src/AMTS/AMTS_python_package/java/ysb.csv'
metrics:
    path : '/usr/src/AMTS/AMTS_python_package/python/metrics 1'
    reportBW: 1.0
orchestrator :
    max util : 1.0
    min util : 0.1
    ConcurrencyValue : 10000
    message size : 0.0032
hosts :
    - host :
        pes : 6
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000

    - host : 
        pes : 6
        MIPS : 4000
        RAM : 32768
        BW : 10000
        Storage : 100000

VMs :
    - VM :
        pes : 6
        MIPS : 4000
        RAM : 16250
        BW : 40
        Storage : 1000
    
    - VM :
        pes : 6
        MIPS : 4000
        RAM : 16250
        BW : 40
        Storage : 1000
"""
test = parser()
test.parse(document)
# model = RNNModel.load_model("./monitor/_model.pth.tar")
# window = pd.Series()
# import csv

# header = ['time in seconds', 'val']



# f = open('countries.csv', 'w', encoding='UTF8', newline='') 
    
# writer = csv.writer(f)

# # write the header
# writer.writerow(header)



# def p (event):
#     vm = test.vms[0]
#     current_time = event.getTime()

#     if window.size < MODEL_INPUT_LENGTH:
#         if int(event.getTime())%10 != 0:
#             return
#         new = [test.CPUMonitor.getVmCurrentpercentage(vm)]
#         ser = pd.Series(new)
#         window.append(ser)
    
#     if current_time < LAST_PREDICTION_TIME + MODEL_OUTPUT_LENGTH*10 :
#         return
    
#     from darts import TimeSeries
#     s = TimeSeries.from_dataframe(window)
#     prediction = model.predict(36,series = s, num_samples=10 , n_jobs = -1)
#     std = prediction[-1].std()

#     if std < STD_THERSHOLD:
#         return
    
#     fetch = test.CPUMonitor.getVmCurrentpercentage(vm)
#     Xs = [0.0,360.0]
#     Ys = [window[-1],fetch]
#     Xs_new = np.arange(0, 360, 10)
#     Ys_new = np.interp(Xs_new,Xs,Ys)
#     window.append(pd.Series(Ys_new))
#     window = window[-100:]
    

# test.addOnClockTickListener(p)

test.Monitor_last_vm()

test.run()

# first create the sliding window
# then prediction and save time of last prediction
# check std of prediction
# if last pridection past the period
# or std violates 
# call test.CPUMonitor.getVmCurrentpercentage(vm)
# interpolate between last fetch and thats your new window

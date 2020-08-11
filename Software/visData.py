import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('officeTest.txt', header = None)
data[0] = pd.to_datetime(data[0], infer_datetime_format=True)
data = data.set_index(0)
data = data.resample('5T').mean()
print(data)

def visData(data):
    plt.plot(data.index, data[1], label = 'Channel 1' )
    plt.plot(data.index, data[2], label = 'Channel 2' )
    plt.plot(data.index, data[3], label = 'Channel 3' )
    plt.plot(data.index, data[4], label = 'Channel 4' )
    plt.plot(data.index, data[5], label = 'Channel 5' )
    plt.legend()
    plt.title('Temperature Monitoring')
    plt.xlabel('Time')
    plt.ylabel('Temperature ($^o$C)')
    plt.show()

print("Plotting data")
visData(data)
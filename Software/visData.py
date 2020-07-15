import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('test1.txt', header = None)
print()


def visData(data):
    plt.plot(data[0], data[1], label = 'Channel 1' )
    plt.plot(data[0], data[2], label = 'Channel 2' )
    plt.plot(data[0], data[3], label = 'Channel 3' )
    plt.plot(data[0], data[4], label = 'Channel 4' )
    plt.plot(data[0], data[5], label = 'Channel 5' )
    plt.legend()
    plt.title('Temperature Monitoring')
    plt.xlabel('Time')
    plt.ylabel('Temperature (^oC)')
    plt.show()


visData(data)
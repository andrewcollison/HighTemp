import matplotlib.pyplot as plt 
import pandas as pd


class DispData():
    def __init__(self, filename, plt_title):
        self.filename = filename
        self.plt_title = plt_title

    def display_data(self):
        try:
            try:
                print("Loading data from: " + self.filename) 
                df = pd.read_csv(self.filename, header = None, parse_dates=True, index_col = [0], engine='python')
                print(df.head())
            except:
                print('Error Loading File \n - Check filename is a string \n - Check file directory')

            print("Plotting Data")
            plt.plot(df)
            plt.legend(["Ch 1", "Ch 2", "Ch 3", "Ch 4", "Ch 5"])
            plt.title(self.plt_title)
            plt.show()

        except:
            print("Error plotting data")        


def main():
    filename = input("Input File: ")
    plt_title = input("Plot title: ")
    df = DispData(filename, plt_title)
    df.display_data()


if __name__ == "__main__":
    # execute only if run as a script
    main()

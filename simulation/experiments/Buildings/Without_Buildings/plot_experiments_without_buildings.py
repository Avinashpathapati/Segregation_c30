import glob
import os
import pandas as pd
from matplotlib import pyplot as plt

# NOTE: If plot_experiments is run it will find all the csv files
# in the simulation directory and compare scores.
# If you want the mean of a subset of experiments, store them
# in a subfolder and change glob.glob('*.csv') to:
# glob.glob('subfolder/*.csv')

def main():
    # Find the correct filenames
    filenames_ext = glob.glob('*.csv')
    filenames = [os.path.splitext(os.path.basename(x))[0] for x in filenames_ext]

    # Iterate through the experiments and concat the dataframes
    df = pd.DataFrame()
    for index, file in enumerate(filenames_ext):
        df_new = pd.read_csv(file)
        df = pd.concat((df, df_new))

    # Use groupby to compute the mean across experiments
    by_row_index = df.groupby(df.index)
    df_means = by_row_index.mean()

    # Plot the resulting mean values
    for column in df_means:
        print("mean "+column, df_means[column].mean())
        plt.title('Mean scores of ' + column + ' over ' + str(len(filenames)) + ' experiments')
        plt.xlabel('Number of Epochs')
        plt.ylabel('Number of Agents')
        plt.plot(df_means[column])
        plt.show()
        # plt.savefig(column+".png", format="png")
    df_means.to_csv('without_buildings.csv')

if __name__ == '__main__':
    main()

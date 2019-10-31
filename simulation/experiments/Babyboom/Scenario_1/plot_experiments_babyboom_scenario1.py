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
    # filenames_ext = glob.glob(path+'*.csv')
    # filenames = [os.path.splitext(os.path.basename(x))[0] for x in filenames_ext]
    # file1 = os.path('with_buildings.csv')
    # file2 = os.path('without_buildings.csv')

    df_1 = pd.read_csv('babyboom_scenario1.csv')
    # df_2 = pd.read_csv('without_buildings.csv')

    # # Iterate through the experiments and concat the dataframes
    # df = pd.DataFrame()
    # for index, file in enumerate(filenames_ext):
    #     df_new = pd.read_csv(file)
    #     df = pd.concat((df, df_new))

    # Use groupby to compute the mean across experiments
    by_row_index = df_1.groupby(df_1.index)
    df_means1 = by_row_index.mean()
    print(df_means1)


    #Print Total agents
    # plt.title('Number of total agents per epoch')
    # plt.xlabel('Number of Epochs')
    # plt.ylabel('Number of Agents')
    # plt.plot(df_means1['total_agents'])
    # plt.show()

    #Print agents per age group
    plt.title('Number of total agents per epoch')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Number of Agents')
    plt.plot(df_means1['young_agents'], label='Young Agents')
    plt.plot(df_means1['adults_agents'], label='Adult Agents')
    plt.plot(df_means1['elderly_agents'], label='Elderly Agents')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

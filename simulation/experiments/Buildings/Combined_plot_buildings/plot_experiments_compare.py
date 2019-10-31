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

    df_1 = pd.read_csv('with_buildings.csv')
    df_2 = pd.read_csv('without_buildings.csv')

    # # Iterate through the experiments and concat the dataframes
    # df = pd.DataFrame()
    # for index, file in enumerate(filenames_ext):
    #     df_new = pd.read_csv(file)
    #     df = pd.concat((df, df_new))

    # Use groupby to compute the mean across experiments
    by_row_index = df_1.groupby(df_1.index)
    df_means1 = by_row_index.mean()
    print(df_means1)

    by_row_index = df_2.groupby(df_2.index)
    df_means2 = by_row_index.mean()

    #Plot Average number of similar agents
    # plt.title('Average number of similar neighbors with and without buildings')
    # plt.xlabel('Number of Epochs')
    # plt.ylabel('Number of Agents')
    # plt.plot(df_means1['similar_neighbors'], label='With buildings')
    # plt.plot(df_means2['similar_neighbors'], label='Without buildings')
    # plt.legend()
    # plt.show()

    #Plot number of moves per step
    plt.title('Number of moves per step with and without buildings')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Number of Agents')
    plt.plot(df_means1['moves'], label='With buildings')
    plt.plot(df_means2['moves'], label='Without buildings')
    plt.legend()
    plt.show()
    # Plot the resulting mean values
    # for column in df_means:
    #     print("mean "+column, df_means[column].mean())
    #     plt.title('Mean scores of ' + column + ' over ' + str(len(filenames)) + ' experiments')
    #     plt.xlabel('Number of Epochs')
    #     plt.ylabel('Number of Agents')
    #     plt.plot(df_means[column])
    #     #plt.show()
    #     # plt.savefig(plots_folder+column+".png", format="png")
    # df_means.to_csv(path+'with_buildings.csv')



if __name__ == '__main__':
    main()

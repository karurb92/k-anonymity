import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_metric(metrics):

    k_array = metrics[3].tolist()
    ncp_result = metrics[4].tolist()
    cav_result = metrics[6].tolist()
    dm_result = metrics[8].tolist()

    fig, axs = plt.subplots(1, 3)
    axs[0].plot(k_array, ncp_result)
    axs[0].set_title('Normalized\nCertainty\n(lower is better)')
    axs[1].plot(k_array, cav_result)
    axs[1].set_title('Average\nEquivalence\n(lower is better)')
    axs[2].plot(k_array, dm_result)
    axs[2].set_title('Discernibility\nMetric\n(lower is better)')
    for ax in axs.flat:
        ax.set(xlabel='K')
        
    figname=f'./plots/datafly_covid'
    plt.savefig(figname)
    plt.show()
    
    
if __name__ == '__main__':
    
    metrics_file = 'metrics_calculated.csv'
    metrics = pd.read_csv(os.path.join(os.path.abspath(os.getcwd()), metrics_file), sep='|', header=None)
    metrics = metrics[metrics[0]=='22/01/2022 16:52:21']
    
    plot_metric(metrics)
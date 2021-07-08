
import os
import numpy as np
import matplotlib.pyplot as plt
from argparse import Namespace
from anonymize import Anonymizer
from models import classifier_evaluation
from datasets import get_dataset_params
from algorithms import read_tree

methods = ['mondrian', 'classic_mondrian', 'topdown'] #, 'cluster', 'datafly']
dataset = ['adult', 'cahousing', 'cmc', 'mgm', 'informs', 'italia'] #, 
k_array = [2, 5, 10, 20, 50, 100]

metrics = ['ncp', 'cav', 'dm']
ml_metrics = ['knn', 'svm', 'rf']
lcolors = ['orange', 'deepskyblue', 'limegreen', 'magenta']

metric_names = [
    'Normalized\nCertainty\n(lower is better)', 
    'Average\nEquivalence\n(lower is better)', 
    'Discernibility\nMetric\n(lower is better)']

ml_metric_names = [
    'KNN',
    'SVMs',
    'RFs'
]

def sub_plot(result, dataset, methods, metrics, label_x, label_y, figname):

    fig, axis = plt.subplots(nrows = len(metrics), ncols = len(dataset), figsize = (30, 20))
    
    for row, metric in enumerate(metrics):
        for col, data in enumerate(dataset):
            sub_data = result[ (data == result['data']) ]
            for i, method in enumerate(methods):
                sub = sub_data[ (method == sub_data['method'])]
                axis[row, col].plot(sub['k'], sub[metric], color = lcolors[i], label=sub['method'][0])

    labels_handles = {
        label: handle for ax in fig.axes for handle, label in zip(*ax.get_legend_handles_labels())
    }

    fig.legend(
        labels_handles.values(),
        labels_handles.keys(),
        loc="upper center",
        ncol=len(labels_handles.values()),
        size=30)

    for ax, col in zip(axis[0], label_x):
        ax.set_title(col.upper())
    
    for ax in axis[-1]:
        ax.set_xlabel('k', size=20)

    for ax, row in zip(axis[:,0], label_y):
        ax.set_ylabel(row, size = 24)
        ax.get_yaxis().set_label_coords(-0.4, 0.5)
    
    plt.subplots_adjust(0.075, 0.05, 0.97, 0.95, 0.2, 0.25)
    plt.savefig(figname)
    plt.show()


def plot_metric(col, metrics, label_x, label_y, figname):
    result = np.genfromtxt("metric_result", names = col, dtype = None)
    dataset = np.unique(result['data'])
    methods = np.unique(result['method'])
    sub_plot(result, dataset, methods, metrics, label_x, label_y, figname)

def run_anon_data():

    output = open("metric_result", "w")

    for data in dataset:
        for method in methods:
            for k in k_array:
                args = Namespace()
                args.method = method
                args.dataset = data
                args.k = k
                anonymizer = Anonymizer(args)
                ncp, cav_b, cav_a, dm_b, dm_a = anonymizer.anonymize()
                result = f'{data} {method} {k} {ncp:.3f} {cav_a:.3f} {dm_a:.3f}'
                output.write(result + '\n')
    
    output.close()

def run_anon_data_ml():
    import pandas as pd
    data_path = './data'
    result_path = './results'
    output = open("ml_metric_result", "w")

    for data in dataset:
        gen_path = f'./data/{data}/hierarchies'
        data_params = get_dataset_params(data)
        QI_INDEX = data_params['qi_index']
        IS_CAT = data_params['is_category']
        HAS_HIERARCHIES = [True] * len(IS_CAT)
        ori_csv = os.path.join(data_path, data, f'{data}.csv')
        tmp_df = pd.read_csv(ori_csv, delimiter=';')
        ATT_NAMES = list(tmp_df.columns)
        ATT_TREES = read_tree(
                gen_path, 
                data, 
                ATT_NAMES, 
                QI_INDEX, 
                HAS_HIERARCHIES)
        train_index = os.path.join(data_path, data, f'{data}_train.txt')
        val_index = os.path.join(data_path, data, f'{data}_val.txt')
        for classifier_name in ml_metrics:
            ori_f1 = classifier_evaluation(classifier_name, ori_csv, train_index, val_index)
            for method in methods:
                for k in k_array:
                    anon_csv = os.path.join(result_path, data, method, f'{data}_anonymized_{k}.csv')
                    tmp_att_trees = ATT_TREES
                    if method == 'classic_mondrian':
                        tmp_att_trees = None
                    anon_f1 = classifier_evaluation(
                        classifier_name, 
                        ori_csv, 
                        train_index, 
                        val_index, 
                        anon_csv=anon_csv,
                        qi_index=QI_INDEX, 
                        is_cat=IS_CAT,
                        att_trees=tmp_att_trees)

                    result = f'{data} {method} {k} {classifier_name} {ori_f1:.3f} {anon_f1:.3f}'
                    output.write(result + '\n')
    output.close()


if __name__ == '__main__':

    # Metric evaluation
    run_anon_data()
    plot_metric(
        col = ["data", "method", "k", "ncp", "cav", "dm"],
        metrics = metrics,
        label_x= dataset,
        label_y = metric_names,
        figname='./demo/metrics2'
    )

    # run_anon_data_ml()
    # plot_metric(
    #     col = ["data", "method", "k", "ori_f1", "anon_f1"],
    #     metrics = metrics,
    #     label_x= dataset,
    #     label_y = metric_names,
    #     figname='./demo/metrics'
    # )
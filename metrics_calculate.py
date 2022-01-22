import os
import numpy as np
from argparse import Namespace
from datetime import datetime
import csv

from anonymize import Anonymizer
#from models import classifier_evaluation
#from datasets import get_dataset_params
#from algorithms import read_tree

methods = ['datafly'] #['cluster', 'datafly']
dataset = ['covid']  # italia
k_array = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]#[i for i in range(10, 110, 50)]  
metrics = ['ncp', 'cav', 'dm']


def run_anon_data():

    result_file = 'metrics_calculated.csv'
    result_path = os.path.join(os.path.abspath(os.getcwd()), result_file)
    
    results = []
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    for data in dataset:
        for method in methods:
            for k in k_array:
                args = Namespace()
                args.method = method
                args.dataset = data
                args.k = k
                anonymizer = Anonymizer(args)
                ncp, cav_b, cav_a, dm_b, dm_a = anonymizer.anonymize()
                results.append([date, data, method, k, ncp, cav_b, cav_a, dm_b, dm_a])

    with open(result_path, 'a+', errors='ignore', encoding='utf-8', newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter='|')
        csv_output.writerows(results)
               
            
if __name__ == '__main__':
    run_anon_data()
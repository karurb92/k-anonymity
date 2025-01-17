# Data anonymization using k-Anonymity
## ✔️ Team's contribution (Amir, Nikita, Karol)

Repository was forked from here: https://github.com/kaylode/k-anonymity

Our contribution:
1. We prepared our own dataset to be anonymized, together with quasi-identifiers' hierarchies definition. All can be found in ```/data/covid```
2. We anonymized the dataset using the ```datafly``` algorithm for different k values. Results can be found in ```/results/covid```
3. We calculated ```CAVG```, ```DM``` and ```NCP``` metrics for different k-values. Results are stored in ```metrics_calculated.csv```
4. We generated plots with above-mentioned metrics, which can be found in ```/plots```

- Anonymization of the data, together with metrics calculation and saving them into csv can be called this way:
```
python metrics_calculate.py
```
Variables ```methods```, ```dataset```, ```k_array``` inside ```metrics_calculate.py``` are responsible, respectively, for the choice of the algorithm, data and k values. By default ```covid``` dataset and ```datafly``` algorithm are being used. The script might take a while to run.

- Plots can then be generated by calling:
```
python metrics_plot.py
```


# Explanations below come directly from the forked repository and have not been changed
## ✔️ Experiments
- Provides 5 k-anonymization method: 
  - Datafly
  - Incognito 
  - Topdown Greedy
  - Classic Mondrian
  - Basic Mondrian
- Implements 3 anonymization metrics: 
  - Equivalent Class size metric (CAVG)
  - Discernibility Metric (DM)
  - Normalized Certainty Penalty (NCP)
- Implements 3 classification models: 
  - Random Forests 
  - Support Vector Machines 
  - K-Nearest Neighbors


## 📖 Reports
- Report edit link: [link](./demo/report.pdf)
- Slide link: [link](./demo/slides.pdf)

## Folder Structure
- A dataset must comes with a .csv file contains features information and a hierarchy folder which contains predefined generalization hierarchies for its QID attributes. 
```
this repo
│   anonymize.py
|
└───data  
│   │
│   └───adult
│       │   adult.csv
│       └───hierarchies
│       │     adult_hierarchy_workclass.csv
│       │     ....
```

- Here is an example for a generalization hierarchy of the 'workclass' attribute from ADULT dataset, described in ```adult_hierarchy_workclass.csv```, which is a csv file using **";" as delimiter**
```
Private;Non-Government;*
Self-emp-not-inc;Non-Government;*
Self-emp-inc;Non-Government;*
Federal-gov;Government;*
Local-gov;Government;*
State-gov;Government;*
Without-pay;Unemployed;*
Never-worked;Unemployed;*
```

which describes this tree:

<div align="center"><img width="450" alt="screen" src="demo/adult_workclass.PNG"></div>

-------------------------------------------------------------

## 🌟 Executing
To anonymize dataset, run:
```
python anonymize.py --method=<model_type> --k=<k-anonymity> --dataset=<dataset_name>
```
- **model_type**: [mondrian | classic_mondrian | mondrian_ldiv | topdown | cluster | datafly]
- **dataset_name**: [adult | cahousing | cmc | mgm | informs | italia]

Results will be in ```results/{dataset}/{method}``` folder

To run evaluation metrics on every combination of algorithms, datasets and value k, run:
```
python visualize.py
```

Results will be in ```demo/{metrics.png, metrics_ml.png}``` 

## K-Anonymity examples

| Before anonymization | After anonymization with k = 2 |
|:-------------------------:|:-------------------------:|
|<img width="450" alt="screen" src="demo/italia_before.png"> | <img width="450" alt="screen" src="demo/italia_after.png"> |

## Evaluation Metrics
  
| Evaluate anonymization using information loss metrics |
|:-------------------------:|
|<img width="1000" height="600" alt="screen" src="demo/metrics.png"> |
|<img width="1000" height="600" alt="screen" src="demo/metrics2.png"> |
  

| Evaluate anonymization using classification models |
|:-------------------------:|
|<img width="1000" height="600" alt="screen" src="demo/metrics_ml.png"> |
|<img width="1000" height="600" alt="screen" src="demo/metrics_ml2.png"> |



## References:
- Basic Mondrian, Top-Down Greedy, Cluster-based (https://github.com/fhstp/k-AnonML)
- L-Diversity (https://github.com/Nuclearstar/K-Anonymity, https://github.com/qiyuangong/Mondrian_L_Diversity)
- Classic Mondrian (https://github.com/qiyuangong/Mondrian)
- Datafly Algorithm (https://github.com/nazilkbahar/python-datafly)
- Normalized Certainty Penalty from [Utility-Based Anonymization for Privacy Preservation with
Less Information Loss](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.450.6140&rep=rep1&type=pdf)
- Discernibility, Average Equivalent Class Size from [A Systematic Comparison and Evaluation
of k-Anonymization Algorithms
for Practitioners](http://www.tdp.cat/issues11/tdp.a169a14.pdf)
- [Privacy in a Mobile-Social World](https://courses.cs.duke.edu//fall12/compsci590.3/slides/lec3.pdf)
- Code and idea based on [k-Anonymity in Practice: How Generalisation and Suppression Affect Machine Learning Classifiers](https://arxiv.org/abs/2102.04763)

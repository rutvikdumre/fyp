import pandas as pd
import numpy as np
from ast import literal_eval

my_output = pd.read_csv("naive_test_output.csv")
#get precision
combine_list = zip(my_output.actual_hashtags, my_output.predicted_hashtags)
my_output['precision'] = [len(list(set(a).intersection(set(b))))/len(set(b)) if len(set(b)) != 0 else 0 for a, b in combine_list]
precision_score = my_output['precision'].sum()/len(my_output)
print(f'Precision: {precision_score}')

#get_recall
combine_list = zip(my_output.actual_hashtags, my_output.predicted_hashtags)
my_output['recall'] = [len(list(set(a).intersection(set(b))))/len(set(a)) if len(set(b)) != 0 else 0 for a, b in combine_list]
recall_score = my_output['recall'].sum()/len(my_output)
print(f'Recall: {recall_score}')

# get_f1score
my_output['f1 score'] = 2* my_output['precision'] * my_output['recall'] / (my_output['precision'] + my_output['recall'])
my_output['f1 score'] = my_output['f1 score'].replace(np.nan, int(0))
f1_score = my_output['f1 score'].sum()/len(my_output)
print(f'F1 Score: {f1_score}')

#get hit_rate
combine_list = zip(my_output.actual_hashtags, my_output.predicted_hashtags)
my_output['hit rate'] = [1 if len(list(set(a).intersection(set(b))))!=np.nan else 0 for a, b in combine_list]
hit_rate_score = my_output['hit rate'].sum()/len(my_output)
print(f'Hit Rate: {hit_rate_score}')


#get_hit_ratio
combine_list = zip(my_output.actual_hashtags, my_output.predicted_hashtags)
my_output['hit ratio'] = [len(list(set(a).intersection(set(b))))/min(len(set(a)),len(set(b))) if len(set(b)) != 0 else 0 for a, b in combine_list]
hit_ratio_score = my_output['hit ratio'].sum()/len(my_output)
print(f'Hit Ratio: {hit_ratio_score}')

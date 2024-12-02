import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# input a well-organized excel file containing real_categories and pred_categories
# output a heatmap with details of text classification
def make_heatmap(excel_file): 
    df = pd.read_excel(excel_file)
    real_categories_list = set(df['real_categories'])
    for i in range(len(df)):
        pred_categories = df.loc[i,'pred_categories']
        if pred_categories not in real_categories_list:
            df.loc[i,'pred_categories'] = 'other outputs' # categorizing all non-listed data under the umbrella term 'other data'
    
    plt.rcParams['font.family'] = 'Times New Roman'
    df['real_categories'] = df['real_categories'].astype('category')
    df['pred_categories'] = df['pred_categories'].astype('category')
    
    confusion_matrix = pd.crosstab(df['real_categories'], df['pred_categories'])
    row_sums = np.sum(confusion_matrix, axis=1)
    normalized_confusion_matrix = confusion_matrix*100 / np.array(row_sums)[:,np.newaxis]
    normalized_confusion_matrix = normalized_confusion_matrix.iloc[:, [0,1,2,3,4,5,7,8,9,6]]
    plt.figure(figsize=(10, 8))
    sns.heatmap(normalized_confusion_matrix, annot=True, fmt='.2f', cmap='coolwarm',vmin=0, vmax=50,\
                xticklabels=normalized_confusion_matrix.columns, yticklabels=normalized_confusion_matrix.index)
    plt.title('Text Classification (%)')
    plt.xlabel('pred_categories')
    plt.ylabel('real_categories')
    plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

make_heatmap('Text_Fragments_labels.xlsx')
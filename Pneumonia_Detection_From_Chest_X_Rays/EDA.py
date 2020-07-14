## EDA for image dataset

import numpy as np
import pandas as pd
import os
from glob import glob
%matplotlib inline
import matplotlib.pyplot as plt
from skimage import io


## Visualize the image here
def visualize_img(vars = True):

    if vars:
        fig, m_axs = plt.subplots(5, 4, figsize=(16, 16))
        m_axs = m_axs.flatten()
        imgs = all_xray_df.path[:20]
        ind = 0
        
        for img, ax in zip(imgs, m_axs):
            img = io.imread(img)
            ax.imshow(img)
            ax.set_title(all_xray_df.iloc[ind]['Finding Labels'])
            ind = ind + 1
        
        plt.tight_layout()
        
if __name__ == "__main__":
    ## load the dataset here
    all_xray_df = pd.read_csv('/data/Data_Entry_2017.csv')
    all_image_paths = { os.path.basename(x): x for x in glob(os.path.join('/data', 'images*', '*', '*.png'))}
    print('Scans found:', len(all_image_paths), ', Total Headers', all_xray_df.shape[0])
    all_xray_df['path'] = all_xray_df['Image Index'].map(all_image_paths.get)
    
    visualize_img()
    
    ## extract all the disease, and change to pivot table
    all_disease = np.unique(list(chain(*all_xray_df['Finding Labels'].map(lambda x: x.split('|'))tolist())))
    ## label the image dataset here, add a new label into the dataframe
    all_xray_df['pneumonia_class'] = all_xray_df['Finding Labels'].map(lambda x: 1 if 'Pneumonia' in x else 0)
    all_xray_df.drop(columns=['Unnamed: 11'], axis = 0, inplace=True)
    
    all_xray_df["pneumonia_class"].value_counts().plot(kind='bar')
    pneumonia_num = all_xray_df["pneumonia_class"].value_counts()[0]
    non_pneumonia_num = all_xray_df["pneumonia_class"].value_counts()[1]
    ratio = pneumonia_num / (non_pneumonia_num + pneumonia_num)
    print('The number of non-pneumonia data: {}'.format(pneumonia_num))
    print('The number of non-pneumonia data: {}'.format(non_pneumonia_num))
    print('The number of non-pneumonia data: {}'.format(ratio))
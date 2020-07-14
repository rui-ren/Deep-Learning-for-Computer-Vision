## Create your dataset

from random import sample
from sklearn.model_selection import train_test_split


'''
1. Have equal amount of positive and negative cases of Pneumonia using stratify & undersampling sampling in Train
2. Have 20% Pneumonia in the test size
'''

def create_splits(train_df):
    
    train_data, val_data = train_test_split(train_df,
                                            test_size = 0.2,
                                            stratify = train_df["pneumonia_class"])
                                            
    # undersampling here for the imbalanced dataset
    p_inds = train_df[train_df.pneumonia_class == 1].index.tolist()
    np_inds = train_df[train_df.pneumonia_class == 0].index.tolist()
    np_sample = sample(np_inds, len(p_inds))
    train_df = train_df.loc[p_inds + np_sample]
    assert 'Training data is not balance', len(train_data.pneumonia_class == 1) == len(train_data.pneumonia_class == 0)
    
    # make sure that the validation set contains 80% positive and 20% negative
    
    val_p_inds = val_data[val_data.pneumonia_class == 1].index.tolist()
    val_np_inds = val_data[val_data.pneumonia_class == 0].index.tolist()
    val_neg_sample = sample(val_np_inds, 4*len(val_p_inds))
    val_df = valid_df.loc[val_p_inds + val_np_sample]
    
    assert "Test dataset positive and negative ratio", len(valid_df[valid_df['pneumonia_class'] == 1])/len(valid_df) == 0.8
    return train_df, val_df
    

if __name__ == "__main__":
    # Test here
    all_xray_df = pd.read_csv('/data/Data_Entry_2017.csv')
    all_image_paths = { os.path.basename(x): x for x in glob(os.path.join('/data', 'images*', '*', '*.png'))}
    print('Scans found:', len(all_image_paths), ', Total Headers', all_xray_df.shape[0])
    all_xray_df['path'] = all_xray_df['Image Index'].map(all_image_paths.get)
    
    ## extract all the disease, and change to pivot table
    all_disease = np.unique(list(chain(*all_xray_df['Finding Labels'].map(lambda x: x.split('|'))tolist())))
    ## label the image dataset here, add a new label into the dataframe
    all_xray_df['pneumonia_class'] = all_xray_df['Finding Labels'].map(lambda x: 1 if 'Pneumonia' in x else 0)
    all_xray_df.drop(columns=['Unnamed: 11'], axis = 0, inplace=True)
    
    train_df, test_df = create_splits(train_df)
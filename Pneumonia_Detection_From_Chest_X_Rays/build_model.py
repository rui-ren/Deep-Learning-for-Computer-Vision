## Build model for the training dataset
## Here we use the transfer learning method for the model training dataset

'''
Steps for the model training part:
1. Data augumentation using ImageDataGenerator for training dataset and validation dataset separately.
2. VGG16 transfer learning for and add the new fully connected layer and dropout to avoid overfitting
3. checkpoint, EarlyStopping and Learning rate decay method.
4. Combine the model and start training


'''


# Load package
from keras.preprocessing import ImageDataGenerator
from random import sample
from sklearn.model_selection import train_test_split
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential, Model
from keras.application.vgg16 import VGG16
from keras.application.resnet import ResNet50
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau


def my_image_augumentation(data_type):
    """
    @data_type: define the training data or validation data:
        - training data need to do data augumentation and normalization.
        - test dataset ONLY need to normalize the data.
    """
    
    if data_type == "training":
        my_img = ImageDataGenerator(rescale = 1./255,
                                    horizontal_flip = True,
                                    vertical_flip = False,
                                    height_shift_range = 0.1,
                                    width_shift_range = 0.1,
                                    rotation_range = 20,
                                    shear_range = 0.1,
                                    zoom_range = 0.1
                                 )
    else:
        my_img = ImageDataGenerator(rescale = 1./255)
    
    return my_img


def make_train_gen(my_img, train_df, IMG_SIZE, batch_size):
    '''
    @ my_img: the image augmentation object
    @ train_df: training dataset
    @ IMG_SIZE
    @ batch_size
    '''
    train_gen = my_img.flow_from_dataframe(dataframe = train_df,
                                             directory = None,
                                             x_col = 'path',
                                             y_col = 'pneumonia_class',
                                             class_mode = 'raw',
                                             target_size = IMG_SIZE,
                                             batch_size = batch_size
                                        )

    return train_gen
    
    
def make_val_gen(my_idg, val_data, IMG_SIZE, batch_size):
    '''
    @ my_img: the image augmentation object
    @ train_df: training dataset
    @ IMG_SIZE
    @ batch_size
    '''
    val_gen = my_idg.flow_from_dataframe(dataframe = val_data, 
                                             directory=None, 
                                             x_col = 'path',
                                             y_col = 'pneumonia_class',
                                             class_mode = 'raw',
                                             target_size = IMG_SIZE, 
                                             batch_size = batch_size
                                        ) 
    return val_gen


def load_pretrained_model(lay_of_interest):
'''
Here we use the pretrained model for the calculation

'''
    model = VGG16(include_top = True, weights = 'imagenet')
    transfer_layer = model.get_layer(lay_of_interest)
    vgg_model = Model(inputs = model.input, outputs = transfer_layer.output)
    
    for layer in vgg_model.layers[0:17]:
        layer.trainable = False
    
    for layer in vgg_model.layers:
        print(layer.name, layer.trainable)
    
    return vgg_model


def build_my_model(vgg_model, dropout=0.2):
    new_model = Sequential()
    new_model.add(vgg_model)
    
    # add the output of the VGG16
    new_model.add(Dropout(dropout_rate))
    
    # add dense layer
    new_model.add(Dense(1024, activation='relu'))
    
    # add dropout layer
    new_model.add(Dropout(dropout_rate))
    
    # add fully connected layers
    new_model.add(Dense(512, activation='relu'))
    
    # add dropout layers
    new_model.add(Dropout(dropout_rate))
    
    # add another dropout layers
    new_model.add(Dense(256, activation='relu'))
    
    # add fully connected layer
    new_model.add(Dense(1, activation='sigmoid'))
    
    optimizer = Adam(lr=1e-4)
    loss = 'binary_crossentropy'
    metrics = ['binary_accuracy']
    
    new_model.compile(optimizer = optimizer, loss = loss, metrics = metrics)
    
    return new_model
    

if __name__ == "__main__":
    
    vgg_model = load_pretrained_model("block5_pool")
    model = build_my_model(vgg_model)
    model.summary()
    
    weight_path = "{}_my_model.best.hdf5".format('xray_class')
    
    checkpoint = ModelCheckpoint(weight_path,
                                 monitor = 'val_loss',
                                 verbose = 1,
                                 save_best_only = True,
                                 mode = 'min',
                                 save_weights_only = True)

    lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience = 4, verbose = 2, mode = 'min')

    early = EarlyStopping(monitor = 'val_loss',
                            mode = 'min',
                            patience = 10)
                            
    callbacks_list = [checkpoint, lr_reduce, early]

    history = model.fit_generator(train_gen,
                                    validation_data = val_gen,
                                    epochs = 100,
                                    callbacks = callbacks_list)




























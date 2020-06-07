import os
import numpy as np
import keras.backend as K
from keras.models import Model
from keras.layers import Input, Lambda
# import yolo3 file mode.py, utils.py
from yolo3.model import preprocessing_true_boxes, yolo_body, yolo_loss
from yolo3.utils import get_random_data

def get_categoryList(txtFilePath):
    with open(txtFilePath, 'r', encoding='utf8') as file:
        fileContent = file.read()

    line_list = [k.strip() for k in fileContent.split('\n') if k.strip() != '']
    category_list = sorted(line_list, reverse=False)
    return category_list

# anchor_ndarray
def get_anchorNdarray(anchor_txtFilePath):
    with open(anchor_txtFilePath) as file:
        anchor_ndarray = [float(k) for k in file.read().split(',')]
    return np.array(anchor_ndarray).reshape(-1, 2)

def create_model(input_shape, anchor_ndarray, num_classes, load_pretrained=True, freeze_body=False, weights_h5FilePath='./trained_weights.h5'):
    K.clear_session()
    image_input = Input(shape=(None, None, 3))
    height, width = input_shape
    num_anchors = len(anchor_ndarray)
    y_true = [Input(shape=(height // k,
                           width //k,
                           num_anchors //3,
                           num_classes + 5)) for k in [32, 16, 8]]
    model_body = yolo_body(image_input, num_anchors//3, num_classes)
    print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

    if load_pretrained and os.path.exists(weights_h5FilePath):
        model_body.load_weights(weights_h5FilePath, by_name=True, skip_mismatch=True)
        print('Load weights from this path: {}.'.format(weights_h5FilePath))
        if freeze_body:
            num = len(model_body.layers) - 7
            for i in range(num):
                model_body.layers[i].trainable = False
                print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

        model_loss = Lambda(yolo_loss,
                            output_shape=(1, ),
                            name='yolo_loss',
                            arguments={
                                'anchors': anchor_ndarray,
                                'num_classes': num_classes,
                                'ignore_thresh': 0.5
                            })(
            [*model_body.output, *y_true])
        model = Model([model_body.input, *y_true], model_loss)

        return model

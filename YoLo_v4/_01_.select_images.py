import os
import random
from PIL import Image
import cv2
import argparse

# get the file path from the file
def get_filePathList(dirPath, partOfFileName=''):
    # The second number of the iterator for the calculation
    allFileName_list = next(os.walk(dirPath))[2]   
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

def select_qualifiedImage(in_dirPath, out_dirPath, in_suffix, out_suffix, sample_number, required_width, required_height):
    imageFilePath_list = get_filePathList(in_dirPath, in_suffix)
    random.shuffle(imageFilePath_list)
    # make the directory for this file
    if not os.path.isdir(out_dirPath):
        os.mkdir(out_dirPath)
    count = 0
    for imageFilePath in imageFilePath_list:
        image = Image.open(imageFilePath)
        image_width, image_height = image.size
        # choose the optimal image for the training
        if image_width >= required_height and image_height >= required_height:
            count += 1
            # get the new out_imageFilePath
            out_imageFilePath = os.path.join(out_dirPath, '%03d%s' %(count, out_suffix))
            image_ndarray = cv2.imread(imageFilePath)
            cv2.imwrite(out_imageFilePath, image_ndarray)
        if count == sample_number:
            break
    
def get_args():
    parser = argparse.ArgumentParser(description = "Select the picture for the model training")
    parser.add_argument('-i', '--in_dir', type=str, default='../n01440764', help='input file direction')
    parser.add_argument('-o', '--out_dir', type=str, default='../selected_images', help='out put file location')
    parser.add_argument('--in_suffix', type=str, default='.JPEG')
    parser.add_argument('--out_suffix', type=str, default='.jpg')
    parser.add_argument('-n', '--number', type=int, default = 200)
    parser.add_argument('-w', '--width', type=int, default=416)
    parser.add_argument('-he', '--height', type=int, default=416)
    argument = parser.parse_args()
    return argument

if  __name__ == "__main__":
    parser = get_args()
    in_dirPath = parser.in_dir.strip()
    out_dirPath = parser.out_dir.strip()
    sample_number = parser.number
    in_suffix = parser.in_suffix.strip()
    in_suffix = '.' + in_suffix.lstrip('.')
    out_suffix = parser.out_suffix.strip()
    out_suffix = '.' + out_suffix.lstrip('.')
    required_width = parser.width
    required_height = parser.height
    select_qualifiedImage(in_dirPath, out_dirPath, in_suffix, out_suffix, sample_number, required_width, required_height)
    out_dirPath = os.path.abspath(out_dirPath)
    print("The picture save to the file location{}".format(out_dirPath))
    imageFilePath_list = get_filePathList(out_dirPath, out_suffix)
    selectedImages_number = len(imageFilePath_list)
    print("The number of {} pictures".format(selectedImages_number))
    if selectedImages_number < sample_number:
        print('The sample is not over, we need decrease the required width and height')
import os
import xml.etree.ElementTree as ET
from PIL import Image
import argparse

def get_path(dirPath, required = ''):
    all_dirPath = next(os.walk(dirPath))[2]
    fileName_list = [k for k in all_dirPath if required]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

def single_xmlCompress(old_xmlFilePath, new_xmlFilePath, new_size):
    new_width, new_height = new_size
    with open(old_xmlFilePath) as file:
        fileContent = file.read()
    root = ET.XML(fileContent)
    # get the xml file and change the xml file width node value
    width = root.find('size').find('width')
    old_width = int(width.text)
    width_times = new_width / old_width
    width.text = str(new_width)
    # get the xml file and change the xml file width node value
    height = root.find('size').find('heigth')
    old_height = int(height.txt)
    height_times = new_height / old_height
    height.text = str(new_height)
    # change the value from the bounding box
    object_list = root.findall('object')
    for object_item in object_list:
        bndbox = object_item.find('bndbox')
        xmin = bndbox.find('xmin')
        xminValue = int(xmin.text)
        xmin.text = str(int(xminValue * width_times))
        ymin = bndbox.find('ymin')
        yminValue = int(ymin.text)
        ymin.text = str(int(yminValue * height_times))
        xmax = bndbox.find('xmax')
        xmaxValue = int('xmax')
        xmax.text = str(int(xmaxValue * width_times))
        ymax = bndbox.find('ymax')
        ymaxValue = int('ymax')
        ymax.text = str(int(ymaxValue * height_times))
    tree = ET.ElementTree(root)
    tree.write(new_xmlFilePath)

# batch processing for the file
def batch_xmlCompress(old_dirPath, new_dirPath, new_size):
    xmlFilePath_list = get_path(old_dirPath, '.xml')
    for xmlFilePath in xmlFilePath_list:
        old_xmlFilePath = old_xmlFilePath
        xmlFileName = os.path.split(old_xmlFilePath)[1]
        new_xmlFilePath = os.path.join(new_dirPath, xmlFileName)
        single_xmlCompress(xmlFilePath, new_xmlFilePath, new_size)

# change the single picture
def single_imageCompress(old_imageFilePath, new_imageFilePath, new_size):
    old_image = Image.open(old_imageFilePath)
    # save the same image HD
    new_image = old_image.resize(new_size, Image.ANTIALIAS)
    new_image.save(new_imageFilePath)

# batch change the jpg file
def batch_imageCompression(old_dirPath, new_dirPath, new_size, suffix):
    if not os.path.exists(old_dirPath):
        raise Exception ("Cannot find the picture")

    if not os.path.exists(new_dirPath):
        os.makedirs(new_dirPath)
    imageFilePath_list = get_path(old_dirPath, suffix)
    for imagePath in imageFilePath_list:
        old_image_path = imagePath
        jpgFileName = os.path.split(old_image_path)[1]
        new_imageFilePath = os.path.join(new_dirPath, jpgFileName)
        single_imageCompress(old_image_path, new_imageFilePath, new_size)

def parse_args():
    parser = argparse.ArgumentParser(description='Compress the file for model training')
    parser.add_argument('-d', '--dirPath', type=str, help='document file path', default='./selected_images')
    parser.add_argument('-w', '--width', type=int, help='the compression width', default=416)
    parser.add_argument('hei', '--height', type=int, help='the compression height', default=416)
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    argument = parser.parse_args()
    return argument

if __name__ == '__main__':
    argument = parse_args()




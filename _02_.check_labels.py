import os
import xml.etree.ElementTree as ET
from PIL import Image
import argparse
"""
Check label of this file
"""

def get_filePathList(dirPath, pathOfFileName=''):
    all_fillName_list = next(os.walk(dirPath))[2]
    fileName_list = [k for k in all_fillName_list if pathOfFileName in k]
    filePath_List = [os.path.join(dirPath, k) for k in fileName_list]
    # return all the file path list for the calculation
    return filePath_List

def delete_file(filePath):
    if not os.path.exists(filePath):
        print('%s This file is not here, please check' %filePath)
    else:
        print('%s This file will be deleted' %filePath)

def check1(dirPath, suffix):
    # check if image got the mark
    # every jpg file, I marked then there exists a '.xml' file
    imageFilePath_list = get_filePathList(dirPath, suffix)
    allFileMarked = True
    for imageFilePath in imageFilePath_list:
        xmlFilePath = imageFilePath[:-4] + '.xml'
        if not os.path.exists(xmlFilePath):
            delete_file(imageFilePath)
            allFileMarked = False
    if allFileMarked:
        print("All the image already got marked")

    # when we have some unmarked figures in the file
    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    xmlFilePathPrefix_list = [k[:-4] for k in xmlFilePath_list]
    # the set of marked xml
    xmlFilePathPrefix_set = set(xmlFilePathPrefix_list)
    imageFilePath_list = get_filePathList(dirPath, suffix)
    imageFilePathPrefix_list = [k[:-4] for k in imageFilePath_list]
    # the set of image
    imageFilePathPrefix_set = set(imageFilePathPrefix_list)
    #  we get the set difference for the image and the xml marked file
    redundant_xmlFilePathPrefix_list = list(xmlFilePathPrefix_set - imageFilePathPrefix_set)
    redundant_xmlFilePath_list = [k +'.xml' for k in redundant_xmlFilePathPrefix_list]
    for xmlFilePath in redundant_xmlFilePath_list:
        delete_file(xmlFilePath)

def check2(dirPath, className_list):
    className_set = set(className_list)
    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        with open(xmlFilePath) as file:
            fileContent = file.read()
        # use the tries tree here
        root = ET.XML(fileContent)
        object_list = root.findall('object')
        for object_item in object_list:
            name = object_item.find('name')
            className = name.text
            if className not in className_set:
                print('%s This xml file has the typo here' % (xmlFilePath, className))
                allFileCorrect = False
    if allFileCorrect:
        print('Congratulations. You pass all the xml file')

def check3(dirPath, suffix):
    xmlFilePath_list = get_filePathList(dirPath, '.xml')
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        # the image file path
        imageFilePath = xmlFilePath[:-4] + '.' + suffix.strip('.')
        image = Image.open(imageFilePath)
        width, height = image.size
        with open(xmlFilePath) as file:
            fileContent = file.read()
        root = ET.XML(fileContent)
        object_list = root.findall('object')
        for object_item in object_list:
            bndbox = object_item.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            if xmin >= 1 and ymin >= 1 and xmax <= width and ymax <= height:
                continue
            else:
                delete_file(xmlFilePath)
                delete_file(imageFilePath)
                allFileCorrect = False
                break
    if allFileCorrect:
        print("congrats all file is in the boundary")

# get the txt File here
def get_classNameList(txtFilePath):
    with open(txtFilePath, 'r', encoding='utf8') as file:
        fileContent = file.read()
        line_list = [k.strip() for k in fileContent.split('\n') if k.strip() != '']
        className_list = sorted(line_list, reverse=False)
    return className_list

def parse_args():
    parser = argparse.ArgumentParser(description= 'check the label picture for the calculaton')
    parser.add_argument('-d', '--dirPath', type=str, help='file path check please', default='./selected_images')
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    parser.add_argument('-c', '--class_textFilePath', type=str, default='./category_list.txt')
    name_space = parser.parse_args()
    return name_space

# check the file soon
if __name__ == '__main__':
    argument = parse_args()
    dirPath = argument.dirPath
    class_txtFilePath = argument.class_textFilePath
    className_list = get_classNameList(class_txtFilePath)
    suffix = argument.suffix
    check1(dirPath, suffix)
    check2(dirPath, className_list)
    check3(dirPath, suffix)

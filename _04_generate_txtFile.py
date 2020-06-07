import xml.etree.ElementTree as ET
import os
import argparse
from sklearn.model_selection import train_test_split


def get_classname_list(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf8') as file:
        fileContent = file.read()
        # here we get the marked name in the txt file
        line_list = [k.strip() for k in fileContent.split('\n') if k.strip() != '']
        className_list = sorted(line_list, reverse=False)
    return className_list

def get_path(dirPath, require=''):
    pathNameList = next(os.walk(dirPath))[2]
    fileName_list = [k for k in pathNameList if require in k]
    # we can switch to get jpg or xml file here
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

def get_args():
    parser = argparse.ArgumentParser(description='get the class of object ')
    parser.add_argument('-d', '--dirPath', type=str, help='document path direction', default='./image_416x416')
    parser.add_argument('-s', '--suffix', type=str, default='.jpg')
    parser.add_argument('-c', '--class_txtFilePath', type=str, default='./category_list.txt')
    argument_compile = parser.parse_args()
    return argument_compile

if __name__ == '__main__':
    argument = get_args()
    dataset_dirPath = argument.dirPath
    suffix = argument.suffix
    class_txtFilePath = argument.class_txtFilePath
    xmlFilePath_list = get_path(dataset_dirPath, '.xml')
    className_list = get_classname_list(class_txtFilePath)
    train_xmlFilePath_list, test_xmlFilePath_list = train_test_split(xmlFilePath_list, test_size=0.1)
    dataset_list = [('dataset_train', train_xmlFilePath_list), ('dataset_test', test_xmlFilePath_list)]
    # use xml file parser
    for dataset in dataset_list:
        txtFile_Path = '%s.txt' % dataset[0]
        txtFile = open(txtFile_Path, 'w')
        # change xml file to label training set and test set
        for xmlFilePath in dataset[1]:
            jpgFilePath = xmlFilePath.replace('.xml', '.jpg')
            txtFile.write(jpgFilePath)
            # check the xml file here
            with open(xmlFilePath) as xmlFile:
                xmlFileContent = xmlFile.read()
            root = ET.XML(xmlFileContent)
            for obj in root.iter('object'):
                className = obj.find('name').text
                if className not in className_list:
                    print('Error, make sure the className_list')
                    continue
                classId = className_list.index(className)
                bndbox = obj.find('bndbox')
                bound = [int(bndbox.find('xmin').text), int(bndbox.find('ymin').text),
                         int(bndbox.find('xmax').text), int(bndbox.find('ymax').text)]
                txtFile.write("" + ",".join([str(k) for k in bound]) + ',' + str(classId))
            txtFile.write('\n')
        txtFile.close()
    print('well done')


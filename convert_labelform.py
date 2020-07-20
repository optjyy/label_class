# written by JYY in 2020.07.20 

# this code is converting csv file into json file we want to use in training
# if there is dirty column in csv file, it makes clean label, dirty label files
# else, if makes a label file.
# file name is inherited the base_path's last directory name.
# ex) if base_path = 'C:\Users\vsoso\Desktop\ai_challenge\Garbage classification\cardboard',
#       label name = cardboard_label.json
# label starts from 1
# label file would be json file. Its key is file name. value is list type labels. label starts from 1
# 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food'
# etc : 1
# paper : 2
# metal : 3
# glass : 4
# plastic : 5
# vinyl : 6
# styrofom : 7
# food : 8

import os
import csv
import json
# base path is where image files are at. you must edit base path
# if you are window user, use path like below example, the 'r' is not mistyped. it is needed.
# base_path = r'C:\Users\vsoso\Desktop\ai_challenge\Garbage classification\cardboard'

base_path = r'plz input image directory path'

# outpath is path that labeled csv file exists
output_path = os.path.join(base_path, 'output', 'assigned_classes.csv')
save_path = os.path.join(base_path, 'output')
dir_name = os.path.split(base_path)

dir_name = dir_name[-1]

temps = os.listdir(base_path)
images = []
for temp in temps:
    if temp.endswith(".jpg"):
        images.append(temp)

# dictionary for saving label into json form
img_label = {}
dirty_img_label = {}

with open(output_path, newline='') as f:
    labelreader = csv.reader(f, delimiter=' ', quotechar='|')
    
    for row in labelreader:
        data = row[0].split(",")
        # first row in csv file has column name
        # confirm first row is form we want. and whether dirty class is included or not
        # and skip it
        if data[0] == 'img':
            assert data == ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food'] or ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food', 'dirty']
            if data == ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food']:
                dirty = False
            elif data == ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food', 'dirty']:
                dirty = True
            continue

        # confirm filename in label file is not wrong
        assert data[0] in images, f'{data[0]} is not in original images! labeled file may be corrupted by something!'
        
        # after first row, there are labels like [0, 1, 0, 0, 1, 0, 0, 0]. convert it to like [2, 5].
        # and save it to dictionary.
        img_label[data[0]] = []
        label_exist = False
        for i in range(1, 9):
            if data[i] == '1':
                label_exist = True
                if dirty:
                    if data[9] == '1':
                        dirty_img_label[data[0]].append(i)
                    else:
                        img_label[data[0]].append(i)
                        dirty_img_label[data[0]].append(i)
                else:
                    img_label[data[0]].append(i)

        if label_exist == 'False':
            print(f"{data[0]} is not labeled")

    # for dirty file, json label file generated
    if dirty:
        assert len(dirty_img_label) == len(images), "# of labeled image is not matched with # of original images"
        clean_path = os.path.join(save_path, f'{dir_name}_label_clean.json')
        dirty_path = os.path.join(save_path, f'{dir_name}_label_dirty.json')
        with open(clean_path, 'w', encoding='utf-8') as f:
            json.dump(img_label, f, indent='\t')
        with open(dirty_path, 'w', encoding='utf-8') as f:
            json.dump(dirty_img_label, f, indent='\t')
        assert os.path.exists(clean_path), 'clean label not generated'
        assert os.path.exists(dirty_path), 'dirty label not generarted'
        print('clean, dirty label generated well')
    
    # for not dirty included file, json label file generated
    else:
        assert len(img_label) == len(images), "# of labeled image is not matched with # of original images"
        label_path = os.path.join(save_path, f'{dir_name}_label.json')
        with open(label_path, 'w', encoding='utf-8') as f:
            json.dump(img_label, f, indent='\t')
        assert os.path.exists(label_path), 'label not generated'
        print('label generated well')

print(len(img_label))
print(type(img_label))
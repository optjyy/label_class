# written by JYY in 2020.07.20 

# this code is confirming that every image files in base path are labeled.
# if # of image files in original file is not matched with labeled image, it makes error.

import os
import csv

# base path is where image files are at. you must edit base path
# if you are window user, use path like below example, the 'r' is not mistyped. it is needed.
# base_path = r'C:\Users\vsoso\Desktop\ai_challenge\Garbage classification\cardboard'

base_path = r'C:\Users\vsoso\Desktop\ai_challenge\Garbage classification\cardboard'

# outpath is path that labeled csv file exists
output_path = os.path.join(base_path, 'output', 'assigned_classes.csv')

temps = os.listdir(base_path)
images = []
for temp in temps:
    if temp.endswith(".jpg"):
        images.append(temp)

img_label = {}

with open(output_path, newline='') as f:
    labelreader = csv.reader(f, delimiter=' ', quotechar='|')
    for row in labelreader:
        data = row[0].split(",")
        # print(data)
        # a = input()
        if data[0] == 'img':
            assert data == ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food'] or ['img', 'etc', 'paper', 'metal', 'glass', 'plastic', 'vinyl', 'styrofoam', 'food', 'dirty']
            label_length = len(data)
            continue
        assert data[0] in images, f'{data[0]} is not in original images! labeled file may be corrupted by something!'
        img_label[data[0]] = []
        label_exist = False
        for i in range(1, 9):
            if data[i] == '1':
                label_exist = True
                img_label[data[0]].append(i)
        
        if label_exist == 'False':
            print(f"{data[0]} is not labeled")
    
    
    assert len(img_label) == len(images), "# of labeled image is not matched with # of original images"
    
    print(f"# of images in base_path : {len(images)}")
    print(f"# of labeled image : {len(img_label)}")
    print("labeled well!")







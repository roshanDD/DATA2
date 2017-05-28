'''
    This program packages the labels and images 
from the underwater dataset and converts them 
to an hdf5 database file.

    Thanks, Thomas, for labeling all of those images.
        -shadySource
'''
import os
import sys
import json
import PIL.Image
import numpy as np
import time
import csv

debug = False #only load 10 images

label_dict = {"car":0, "truck":1, "pedestrian":2}
f = csv.reader(open("labels.csv", "rb"), delimiter=" ")
'''
CSV Format

xmin
ymin
xmax
ymax
frame
label
'''

# ['1478732250414454214.jpg', '898', '562', '988', '630', '0', 'car']

# label, x_min, y_min, x_max, y_max
# [['underwater_1', '2013_AUVSI_Robosub_Competition_Recap_085.jpg'], [2, 163, 111, 200, 151], [0, 305, 125, 335, 154], [1, 433, 66, 460, 91], [3, 223, 254, 308, 297]]
i = 0
prev = " "
image_labels = []
tmp = []
for row in f:
    if i >14:
        break
    print row
    #tmp = []
    if (row[0] == prev):
        #tmp.append(['object-detection', row[0]])
        xmin = row[1]
        ymin = row[2]
        xmax = row[3]
        ymax = row[4]
        LABEL = row[6]
        if (LABEL in label_dict):
            tmp.append([label_dict[LABEL], xmin, ymin, xmax, ymax])


    else :
        #print image_labels[i]
        if (i != 0):
            image_labels.append(tmp)
            print image_labels
            print type(tmp)
            #time.sleep(1)

        i = i +1
        tmp = []
        tmp.append(['object-detection', row[0]])
        xmin = row[1]
        ymin = row[2]
        xmax = row[3]
        ymax = row[4]
        LABEL = row[6]
        if (LABEL in label_dict):
            tmp.append([label_dict[LABEL], xmin, ymin, xmax, ymax])
    i = i + 1
    #prev = row[0]
    #print len(image_labels)
#print type(image_labels)
#time.sleep(20)



# load images
images = []
for i, label in enumerate(image_labels):
    img = np.array(PIL.Image.open(os.path.join('data', label[0][0], label[0][1])))
    images.append(img)
    if debug and i == 9:
        break

#shuffle dataset
np.random.seed(13)
shuffle = [(images[i], image_labels[i]) for i in range(len(images))]
np.random.shuffle(shuffle)
images = [pair[0] for pair in shuffle]
image_labels = [pair[1] for pair in shuffle]



#convert to numpy for saving
images = np.asarray(images, dtype=np.uint8)
image_labels = [np.array(i[1:]) for i in image_labels]# remove the file names
image_labels = np.array(image_labels)

#save dataset
np.savez("underwater_data", images=images, boxes=image_labels)
print('Data saved: underwater_data.npz')



# 1. ) download data
# 2. ) for the label, group them onto a same image. 
# 3. ) then, bound a box across the image. 
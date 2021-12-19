# Data Parser for the *Anti-UAV dataset*

The [Anti-UAV dataset](https://github.com/ZhaoJ9014/Anti-UAV) is a collection 160 high quality, full HD video sequence of UAV videos in various situations and conditions.  All data are annotated with bounding boxes and flags indicating whether the target exists or not in each frame. Each video has a corresponding JSON file that contain these frame-wise annotations. 

<hr>


### Motivation:

To train any object detection model, we have to extract frames from all the videos in the training as well as the validation set. The images are accompanied with TXT/XML annotations that provide the exact coordinates of the bounding boxes that shall enclose the object in the frame. 

<hr>


### Contents:

This repository contains of two python files:

* *extract_frames.py* to extract every frame from the videos and map each frame with it's respective coordinates from the json file. These coordinates are normalized and formatted to fit the YOLOv5 annotation convections.

* *pqrs.py* to randomly split the resulting dataset into training and validation set in ratio r.

<hr>


### How to use:

For extracting the frames and creating the corresponding txt file:

`python extract_frames.py --r [path to the root directory]`

For randomly splitting the dataset based on the desired ratio:

`python split_dataset.py --pf [path of frames] --pl [path of labels] --r [ratio of train-to-test set] --pfinal [path to final]`

<hr>






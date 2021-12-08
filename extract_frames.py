# extracts the frames from the video and saves them in the frames folder
# each frame is annoted individually in a txt file as per the yolo format
# by going through the json file provided with each video
# eg: py extract_frames.py -r ./Anti_UAV_test_dev/

import cv2
import time
import os
import json
from PIL import Image
import argparse

def video_to_frames(input_loc, output_loc):
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds forconversion." % (time_end-time_start))
            return video_length

def parse_json(dir):
    with open(dir) as data_file:
        data = json.load(data_file)
        exists = data['exist']
        coord = data['gt_rect']
    return exists, coord

def parse_txt(dir):
    coords = []
    with open(dir) as f:
        data = f.readline()
        # read through the file and extract coordinates
        data = list(map(int,data.split()))
        coords.extend([data[1],data[2]])
    return coords

def make_files(base,n,exists,coord):
    for i in range(0,n):
        # rename in 00000 format
        file = open(f'{base}/{str(i+1).zfill(5)}.txt','w+')
        file.write(f'{exists[i]} {coord[i][0]} {coord[i][1]} {coord[i][2]} {coord[i][3]}')
        file.close()

def normalise(base_txt,base_img):
    with open(base_txt) as f:
        lists = f.read()
    lists = lists.split()
    lists = [int(i) for i in lists]
    exists,xmin,ymin,w,h=map(int,lists)
    # read the image
    image= Image.open(base_img)
    w_img,h_img = image.size
    # normalise the coordinates to the yolo format
    xcenter = (xmin + w/2) / w_img
    ycenter = (ymin + h/2) / h_img
    w = w / w_img
    h = h / h_img
    return exists,xcenter,ycenter,w,h

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rootdir', action='store', dest='rootdir', default='./Anti_UAV_test_dev' ,
                    help='Path for root directory')
    values = parser.parse_args()
    rootdir = values.rootdir

    # get the list of files
    # rootdir = './Anti_UAV_test_dev'
    for subdir, dirs, files in os.walk(rootdir):
        for file in dirs:
            print(os.path.join(subdir,file))
            input = os.path.join(subdir,file)
            input_loc = os.path.join(input,'IR.mp4')
            output_loc = os.path.join(input,'frames')
            output_labels = os.path.join(input,'labels')
            try:
                os.mkdir(output_labels)
            except OSError:
                pass
            for files in os.walk(output_loc):
                input_json = os.path.join(input,'IR_label.json')
            n = video_to_frames(input_loc,output_loc)
            exists,coord = parse_json(input_json)
            coord = normalise(input,coord)
            n = len(exists)
            make_files(output_labels,n,exists,coord)
            print(f'{file} done')
        



    
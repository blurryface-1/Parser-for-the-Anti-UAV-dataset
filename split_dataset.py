# splits the extracted frames and labels randomly into train and validation sets and moves them to the respective folders 
# as per the user input 
# eg: py split_dataset.py -pf ./Anti_UAV_test_dev/20190925_131530_1_5/frames/ -pl ./Anti_UAV_test_dev/20190925_131530_1_5/labels/ -r 0.7 -pfinal ./done/

import glob
import random
import os
import shutil
import tqdm
import argparse

def get_train_size(data_size,r):
    train_size = int(data_size * r)
    return train_size

def get_all_paths(PATHF,PATHL):
    img_paths = glob.glob(PATHF + '*.jpg')
    txt_paths = glob.glob(PATHL + '*.txt')
    return img_paths,txt_paths

def shuffle_paths(img_paths,txt_paths):
    img_txt = list(zip(img_paths, txt_paths))
    random.seed(43)
    random.shuffle(img_txt)
    img_paths, txt_paths = zip(*img_txt)
    return img_paths,txt_paths

def split_paths(img_paths,txt_paths,train_size):
    train_img_paths = img_paths[:train_size]
    train_txt_paths = txt_paths[:train_size]
    valid_img_paths = img_paths[train_size:]
    valid_txt_paths = txt_paths[train_size:]
    return train_img_paths,train_txt_paths,valid_img_paths,valid_txt_paths

def move(paths, folder):
    for p in paths:
        shutil.move(p, folder)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-pf','--path_frames', default="./Anti_UAV_test_dev/20190925_131530_1_5/frames/", dest='path_frames',help='path_frames')
    parser.add_argument('-pl','--path_labels', default="./Anti_UAV_test_dev/20190925_131530_1_5/labels/", dest='path_labels',help='path_labels')
    parser.add_argument('-r','--ratio', default=0.7, dest='ratio',help='ratio')
    parser.add_argument('-pfinal','--path_final', default="./DRONE/done/", dest='path_final',help='path_final')
    args = parser.parse_args()

    # enter path to frames folder
    PATHF = args.path_frames
    # enter path to labels folder
    PATHL = args.path_labels
    # Get all paths to your images files and text files
    img_paths,txt_paths = get_all_paths(PATHF,PATHL)
    # Calculate number of files for training, validation
    data_size = len(img_paths)
    # enter training to testing ratio
    r = args.r
    # get train size
    train_size = get_train_size(data_size,r)
    # Shuffle two list
    img_paths,txt_paths = shuffle_paths(img_paths,txt_paths)
    # split them
    train_img_paths,train_txt_paths,valid_img_paths,valid_txt_paths = split_paths(img_paths,txt_paths,train_size)

    # Move them to train, valid folders
    PATH2 = args.path_final
    train_folder = PATH2 +'train/' 
    valid_folder = PATH2 +'valid/'

    # uncomment to create folders
    # s.mkdir(train_folder)
    # os.mkdir(valid_folder)

    move(train_img_paths, train_folder)
    move(train_txt_paths, train_folder)
    move(valid_img_paths, valid_folder)
    move(valid_txt_paths, valid_folder)





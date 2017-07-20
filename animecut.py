import os
import cv2
from PIL import Image, ImageFilter, ImageChops, ImageStat
import csv
from datetime import datetime
import tkinter as tk
import tkinter.filedialog

class Logger:
    def __init__(self, save_dir):
        self.filename = save_dir + '/log.csv'
        self.diffs = []
        self.diffs.append((1,0,0))
    def append(self, diff):
        self.diffs.append(diff)
    def end(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f, lineterminator = '\n')
            writer.writerows(self.diffs)

def filter_extension(img_dir, extensions):
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if file.split('.')[-1] in extensions:
                yield os.path.join(root, file), root, file

def resize_img(img_dir, extensions, size):
    for file_path, _, _ in filter_extension(img_dir, extensions):
        img = Image.open(file_path)
        new_img = img.resize(size)
        new_img.save(file_path)

def is_different_cut(image1, image2, cutoff, log, frame_number, fps_video):
    cmp = cv2.absdiff(image1, image2)
    difference = cmp.mean()
    log.append((frame_number, frame_number/fps_video, difference))
    print(difference)
    if difference > cutoff:
        return 1
    else:
        return 0

def collect_img(cap, log, fps, extension, save_dir, cutoff, fps_video, start_frame, end_frame):
    frame_number = start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    img_number = 1
    ret, image1 = cap.read()
    file_name = '{0}.{1}'.format(img_number, extension)
    path = os.path.join(save_dir, file_name)
    cv2.imwrite(path, image1)
    img_number += 1
    #while内で1フレームごとの処理
    while(cap.isOpened() and frame_number <= end_frame):
        frame_number += 1
        ret, image2 = cap.read()
        if not ret:
            break

        if frame_number % fps == 0:
            if is_different_cut(image1, image2, cutoff, log, frame_number, fps_video):
                file_name = '{0}.{1}'.format(img_number, extension)
                path = os.path.join(save_dir, file_name)
                cv2.imwrite(path, image2)
                img_number += 1
        image1 = image2

    return img_number

def start(video_path, save_dir, start_frame, end_frame, extension = 'png', resize_size = (320, 180), fps = 1, resize = True, cutoff = 40):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    s_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    log = Logger(save_dir)
    cap = cv2.VideoCapture(video_path)
    fps_video = cap.get(5)
    img_numbers = collect_img(cap, log, fps, extension, save_dir, cutoff, fps_video, start_frame, end_frame)
    cap.release()
    log.end()
    print('capture finished', img_numbers)

    if resize:
        resize_img(save_dir, (extension,), resize_size)
        print('resize finished')
    print(s_time)
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

if __name__ == "__main__":
    movie_filename = tk.filedialog.askopenfilename()
    print(movie_filename)
    cutoff = input('cutoff difference(30~40 recommended) : ')
    save_dir = input('save folder name : ')
    start_frame = input('from which frame? :')
    end_frame = input('to which frame? :')
    start(movie_filename, save_dir, int(start_frame), int(end_frame), cutoff = int(cutoff))

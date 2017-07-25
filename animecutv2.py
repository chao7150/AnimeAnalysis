import os
import cv2
import start
import csv
import datetime
import time

class Logger:
    def __init__(self, save_dir, datestr, header):
        self.filename = save_dir + '/' + datestr + '.csv'
        self.diffs = []
        self.diffs.append((1,0,0))
        self.header = header
    def append(self, diff):
        self.diffs.append(diff)
    def end(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f, lineterminator = '\n')
            writer.writerows(self.header)
            writer.writerows(self.diffs)

def output(cap, cutpoints, save_dir):
    img_num = 1
    for p in cutpoints:
        cap.set(cv2.CAP_PROP_POS_FRAMES, p)
        ret, image = cap.read()
        image = cv2.resize(image, (800, 450))
        num_pud = '{0:04d}'.format(img_num)
        file_name = num_pud + '.png'
        path = os.path.join(save_dir, file_name)
        cv2.imwrite(path, image)
        img_num += 1
    return 0



def detect(movie_filename, save_dir, start_frame, end_frame, resolution, datestr, cutoff = 40):
    #保存先フォルダが無ければ作る
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    header = [[str(movie_filename)],
    [str(start_frame), str(end_frame)],
    ['resolution', str(resolution), 'cutoff', str(cutoff)]]
    cutpoints = [start_frame]
    logger = Logger(save_dir, datestr, header)
    #動画の読み込み
    cap = cv2.VideoCapture(movie_filename)
    #アニメは24fpsなので60fpsでエンコードされていた場合2フレームに1つしか読まなくていい
    fps = cap.get(5)
    skip = int(fps / (24 / resolution))
    if skip == 0:
        skip = 1
    print(skip)
    #処理開始位置までジャンプ
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    #フレーム数カウンタを作る
    frame_norm = start_frame
    frame_relative = 0
    #1フレーム目は最初に読んでおく
    ret, image1 = cap.read()
    #1フレームずつ回していく
    while(cap.isOpened() and frame_norm + frame_relative < end_frame):
        #次のフレームを読む
        if frame_relative % skip != 0:
            cap.grab()
            frame_relative += 1
            continue
        ret, image2 = cap.read()
        frame_relative += 1
        print(frame_norm + frame_relative)
        #比較してカット点と判定されたらフレーム番号をリストに入れる
        cmp = cv2.absdiff(image1, image2)
        diff = cmp.mean()
        logger.append((frame_norm + frame_relative, int((frame_norm + frame_relative) / fps), int((frame_norm + frame_relative) % fps), diff))
        if diff >= cutoff:
            cutpoints.append((frame_norm + frame_relative))
        image1 = image2

    print(cutpoints)
    logger.end()
    return cutpoints, cap

if __name__ == "__main__":
    movie_filename, start_frame, end_frame = start.start()
    save_dir = input('save folder name :')
    now = datetime.datetime.now()
    datestr = now.strftime("%Y%m%d-%H%M%S")
    save_dir = save_dir+'/'+datestr
    cutoff = input('cutoff difference :')
    resolution = input('resolution:')
    stime = time.time()
    cutpoints, cap = detect(movie_filename, save_dir, start_frame, end_frame, int(resolution), datestr, cutoff = int(cutoff))
    output(cap, cutpoints, save_dir)
    etime = time.time() - stime
    print("etime:{0}".format(etime)+"[sec]")

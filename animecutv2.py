import os
import cv2
import start

def output(cap, cutpoints, save_dir):
    #保存先フォルダが無ければ作る
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

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



def detect(movie_filename, start_frame, end_frame, cutoff = 40):
    cutpoints = [start_frame]


    #動画の読み込み
    cap = cv2.VideoCapture(movie_filename)
    #処理開始位置までジャンプ
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    #フレーム数カウンタを作る
    frame_number = start_frame
    #1フレーム目は最初に読んでおく
    ret, image1 = cap.read()
    #1フレームずつ回していく
    while(cap.isOpened() and frame_number <= end_frame):
        #次のフレームを読む
        ret, image2 = cap.read()
        frame_number += 1
        #比較してカット点と判定されたらフレーム番号をリストに入れる
        cmp = cv2.absdiff(image1, image2)
        diff = cmp.mean()
        if diff >= cutoff:
            cutpoints.append(frame_number)
        image1 = image2

    print(cutpoints)
    return cutpoints, cap

if __name__ == "__main__":
    movie_filename, start_frame, end_frame = start.start()
    save_dir = input('save folder name :')
    cutoff = input('cutoff difference :')
    cutpoints, cap = detect(movie_filename, start_frame, end_frame, cutoff = int(cutoff))
    output(cap, cutpoints, save_dir)

#http://qiita.com/k_sui_14/items/92fd84f35245ad0be464　の　export_movie.py　をアレンジしたものです
#coding=utf-8

import cv2

def export_movie():

    # 入力する動画と出力パスを指定。
    target1 = "XXXX.mp4"
    #動画1の何フレーム目からを参照するか
    delay1 = 2082
    target2 = "XXXX.mp4"
    #動画2の何フレームメカラを参照するか
    delay2 = 3498
    result =  "XXXX.m4v"

    # 動画の読み込みと動画情報の取得
    movie1 = cv2.VideoCapture(target1)
    movie2 = cv2.VideoCapture(target2)
    #現段階では2つの動画のfpsとサイズは一致していることを前提としています
    fps    = movie1.get(cv2.CAP_PROP_FPS)
    height = movie1.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width  = movie1.get(cv2.CAP_PROP_FRAME_WIDTH)

    # 形式はMP4Vを指定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # 出力先のファイルを開く
    out = cv2.VideoWriter(result, int(fourcc), fps, (int(width), int(height)))

    # 最初の1フレームを読み込む
    if movie1.isOpened() == True:
        ret1,frame1 = movie1.read()
    else:
        ret1 = False

    if movie2.isOpened() == True:
        ret2,frame2 = movie2.read()
    else:
        ret2 = False

    #指定したフレームまでスキップ
    movie1.set(cv2.CAP_PROP_POS_FRAMES, delay1)
    movie2.set(cv2.CAP_PROP_POS_FRAMES, delay2)

    # フレームの読み込みに成功している間フレームを書き出し続ける
    frame_number = 1
    #2200フレームだけキャプチャし動画化する
    while ret1 and frame_number < 100:

        # 読み込んだフレームの差分をとり、書き込み
        out.write(cv2.absdiff(frame1, frame2))

        # 次のフレームを読み込み
        ret1,frame1 = movie1.read()
        ret2,frame2 = movie2.read()
        frame_number += 1
    print('finished')

if __name__ == '__main__':
    export_movie()

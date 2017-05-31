#基本的なアイデアは　http://kivantium.hateblo.jp/entry/2015/02/02/203209　からお借りしました

import numpy as np
import cv2
import sys

#ビデオの何フレーム目からを対象にするか
START = 511
#ビデオの最初の何フレーム間を対象にするか
FRAME = 100

#ビデオ読み込み
cap = cv2.VideoCapture("XXXX")
if cap.isOpened() != True:
    print("load failed")
    sys.exit()

images = []
frame_number = 1
cap.set(cv2.CAP_PROP_POS_FRAMES, START)

#動画の最初からFRAME番目のフレームまでをキャプチャしimages配列に入れる
while cap.isOpened() and frame_number <= FRAME:
    ret, image = cap.read()
    images.append(image)
    frame_number += 1

#キャプチャした画像のサイズとカラーチャンネル数を取得
shape = images[0].shape
print(shape)

#取り出した画像のリストをnumpy.arrayに変換
images_a = np.asarray(images)

#計算した最頻値を格納していく3次元リストを初期化しておく
imgmed = [[[0 for i in range(shape[2])]for i in range(shape[1])]for i in range(shape[0])]

#最頻値を計算
imgmed = np.median(images_a, axis=0)

#出来上がった画像を保存
cv2.imwrite("XXXX", np.asarray(imgmed))

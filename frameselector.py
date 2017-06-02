import numpy as np
import cv2

#グローバル
updatelock = False
WINDOW_NAME = "frame"
TRACKBAR_NAME = "Position"

#ウィンドウ生成
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)



#動画の読み込みとチェック
cap = cv2.VideoCapture("XXXX")
if cap.isOpened() != True:
    print("file not found")

#トラックバーが動かされた時に呼び出され、動画の再生位置を変更する
def onTrackbarSlide(pos):
    updatelock = True
    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    updatelock = False

#動画は全部で何フレームあるか
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#トラックバーを生成し、動かされたときにはonTrackbarSlideにトラックバーの位置を渡す
if frames > 0:
    cv2.createTrackbar(TRACKBAR_NAME, WINDOW_NAME, 0, frames, onTrackbarSlide)

#再生用ループ
while(cap.isOpened()):
    if updatelock:
        continue

    #1フレーム読み込む
    ret, frame = cap.read()
    #読み込み失敗（最終フレーム）したら最初に戻る
    if ret == False:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    #リサイズ
    h_frame = cv2.resize(frame, (480, 270))
    #画面に表示
    cv2.imshow("frame", h_frame)

    #現在の再生位置を取得
    curpos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    #トラックバーの位置を現在の再生位置に合わせる
    cv2.setTrackbarPos(TRACKBAR_NAME, WINDOW_NAME, curpos)

    #押されたキーがqならばループを終える
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

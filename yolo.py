import pyyolo
import os
import pdb
import glob
import cv2
import numpy as np

#pdb.set_trace() 

THRESH = 0.24
HIER_THRESH = 0.5

def overlay(img): 
    proc_img = img.transpose(2, 0, 1)
    c, h, w = proc_img.shape
    data = proc_img.ravel()/255.0
    data = np.ascontiguousarray(data, dtype=np.float32)
    outputs = pyyolo.detect(w, h, c, data, THRESH, HIER_THRESH)
    for output in outputs:
        topleft = (output['left'], output['top'])
        bottomright = (output['right'], output['bottom'])
        color = (int(255 * (1 - output['prob'])), 0, int(255 * output['prob']))
        img = cv2.rectangle(img, topleft, bottomright, color, 10)
        img = cv2.putText(img, output['class'], (output['left']+10, output['bottom']-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2, cv2.LINE_AA)
        print(output)
    return img
        

if __name__ == '__main__':
    pyyolo_path = ''
    darknet_path = os.path.join(pyyolo_path, 'darknet')
    datacfg = os.path.join(darknet_path, 'cfg', 'coco.data')
    cfgfile = os.path.join(darknet_path, 'cfg', 'yolo.cfg')
    weightfile = os.path.join(pyyolo_path, 'yolo.weights')
    #filename = os.path.join(darknet_path, 'data', 'person.jpg')
    pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

    cap = cv2.VideoCapture('')
    FOURCC = int(cap.get(cv2.CAP_PROP_FOURCC))
    FPS = cap.get(cv2.CAP_PROP_FPS)
    SIZE = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    out = cv2.VideoWriter('', FOURCC, FPS, SIZE)

    while cap.isOpened():
        ret, img = cap.read()
        if ret != True:
            break
        img = overlay(img)
        out.write(img) 
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

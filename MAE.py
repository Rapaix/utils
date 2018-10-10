import numpy as np
import cv2 as cv
import glob
import shutil
import json


dst = 'D:/Documentos/Lego/repetidas'
src = "D:/Documentos/Lego/imagens/*.jpg"
data ={}

def calculateMAE(imgA, imgB):

    mae = np.sum(np.absolute(imgB.astype("float")-imgA.astype("float")))
    mae /= float(imgA.shape[0] * imgA.shape[1])

    return abs(mae)


tree = glob.glob(src)
print(tree)

for filename in tree:
    imgA = cv.imread(filename)
    imgA = cv.resize(imgA, (300, 300))
    for i,fl in enumerate(glob.glob(src)):
        imgB = cv.imread(fl)
        imgB = cv.resize(imgB, (300, 300))
        if filename != fl:
            mae = calculateMAE(imgA, imgB)
            if (mae >= 0.0 and mae <=0.5):
                shutil.move(fl, dst)
                data.setdefault(filename, []).append(fl)
                tree.remove(fl)



log = json.dumps(data)
print(log)
with open('log.json', 'w') as outfile:
    json.dump(log, outfile)


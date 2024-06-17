import cv2
import os

count=0
path = os.path.join('deskpet','right','sleep')
filelist=os.listdir(path)
for files in filelist:
    Olddir=os.path.join(path,files)
    if os.path.isdir(Olddir):
        continue
    Newdir=os.path.join(path,str(count)+'.png')
    os.rename(Olddir,Newdir)
    path_left = os.path.join('deskpet', 'left', 'sleep', str(count) + '.png')
    image_right = cv2.imread(Newdir, -1)
    image_left = cv2.flip(image_right, 1)
    cv2.imwrite(path_left, image_left)
    count+=1






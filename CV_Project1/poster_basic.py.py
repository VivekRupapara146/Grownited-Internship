# We are gonna make a small project using the functions we learned in basic1.py and basic2.py
''' 
The project is a simple image processing project that will takes number of images as input and make a collage of them images are resized, cropped, rotated, flipped, etc. and showed in a single window

'''
import cv2
import numpy as np

org_w = 1920
org_h = 1080

options = {
    1: ['Porche_4.jpg', 'Porche_2.jpg', 'Porche_3.jpg', 'Porche_1.jpg'],
    2: ['Jungle_1.jpg', 'Jungle_2.jpg', 'Jungle_3.jpg', 'Jungle_4.jpg'],
    3: ['Aurora_Lights_1.jpg','Aurora_Lights_2.jpg','Aurora_Lights_3.jpg','Aurora_Lights_4.jpg']
}

print('''
1. Porche collage
2. Forest collage
3. Aurora Lights collage
      ''')
choice = int(input("Enter the choice: "))

files = options.get(choice)
if files is None:
    raise ValueError("Invalid choice")

img1, img2, img3, img4 = [cv2.imread(f) for f in files]
    
h,w,c = img1.shape
# print(img1_resize.shape,img2_resize.shape)
print(h,w,c)

center = (w//2,h//2)
matrix1 = cv2.getRotationMatrix2D(center, 20,1.6)
matrix2 = cv2.getRotationMatrix2D(center, -20,1.6)
matrix3 = cv2.getRotationMatrix2D(center, 0,1.6)

pic1 = cv2.resize(img3, (org_w//2,org_h//2))
pic2 = cv2.resize(cv2.warpAffine(img4,matrix3,(w,h)), (org_w//2,org_h//2))

row1 = np.hstack((pic1,pic2)) 

pic3 = cv2.resize(cv2.flip(cv2.warpAffine(img2,matrix1,(w,h)),1),(org_w//2,org_h//2))
pic4 = cv2.resize(cv2.flip(cv2.warpAffine(img1,matrix2,(w,h)),1),(org_w//2,org_h//2))

row2 = np.hstack((pic3, pic4))

final = np.vstack((row1,row2))

cv2.imshow('Image Collage', final)

cv2.waitKey(0)
cv2.destroyAllWindows()
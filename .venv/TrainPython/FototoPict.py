import cv2

image = cv2.imread(r'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle\000001.jpg')
cv2.imshow('AVATAR', image)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

invert_image = 255 - gray_image

blurred = cv2.GaussianBlur(invert_image, (21, 21), 0)

invert_blurred = 255 - blurred

pencil_sketch = cv2.divide(gray_image, invert_blurred, scale=256.0)
cv2.imwrite(
    r'D:\MyPythonFolder\MyPython\.venv\Dif_files\ImagesGoogle\000001_sketch'
    r'.jpg', pencil_sketch)

import torch
import requests
import imutils
import numpy as np
import cv2
# Model

## 0.13125
#0.1

# url1 = 'http://192.168.245.88:8080/shot.jpg'
# url2 = 'http://192.168.245.191:8080/shot.jpg'


# # While loop to continuously fetching data from the Url
# # while True:
# img_resp = requests.get(url1)
# img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
# img1 = cv2.imdecode(img_arr, -1)

# img_resp = requests.get(url2)
# img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
# img2 = cv2.imdecode(img_arr, -1)

# cv2.imwrite('calib.jpg', img)

def calc(img1, img2):

# cv2.imshow("Android_cam", img2)
    img1 = imutils.resize(img1, width=640, height=640)
    img2 = imutils.resize(img2, width=640, height=640)
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
    
#     if cv2.waitKey(1) == 27:
#         break
# cv2.destroyAllWindows()
# Inference
# exit()


    model = torch.hub.load('ultralytics/yolov5', 'custom','./latest.pt', device='cpu')

    results = model(img1)
    results.save()

    r1 = results.pandas().xyxy[0].sort_values('confidence').iloc[-1]
    # print(r1)

    l = (r1['xmax'] - r1['xmin']) * 0.13125
    b = (r1['ymax'] - r1['ymin']) * 0.13125

    print(l,b)


    results = model(img2)
    r2 = results.pandas().xyxy[0].sort_values('confidence').iloc[-1]
    # print(r2)

    h = (r2['ymax'] - r2['ymin']) * 0.1
    # results.save()
    # print(h)
    # print(results.pandas().xyxy[0])

    print(h)

    return l*b*h

    # print(results)

    # image = cv2.rectangle(im, )

    #      xmin    ymin    xmax   ymax  confidence  class    name
    # 0  749.50   43.50  1148.0  704.5    0.874023      0  person
    # 1  433.50  433.50   517.5  714.5    0.687988     27     tie
    # 2  114.75  195.75  1095.0  708.0    0.624512      0  person
    # 3  986.00  304.00  1028.0  420.0    0.286865     27     tie
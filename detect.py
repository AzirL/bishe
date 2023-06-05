import cv2
import numpy as np
error_points = []


def skeleton(img):  # 返回骨架图像

    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    ret, thresh = cv2.threshold(img, 150, 255, 0)
    # find the contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours detected:",  len(contours))

    # # select the first contour
    # cnt0 = contours[0]
    # # find the shortest distance from point[250, 250]
    # cnt1 = contours[1]

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while (not done):
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
    cv2.imshow('skel', skel)
    return skel


# 沿法线方向检测
def lines_detect(i, j, y, x, s):
    x1 = int(4*x/s)
    y1 = int(4*y/s)
    print(i+x1, j+y1)
    print(i-x1, j-y1)
    # print(img_otsu[i, j])
    # print(img_otsu[i+x1, j+y1], img_otsu[i-x1, j-y1])
    # 像素白色返回1， 黑色返回0
    if i+x1 > 449 or i-x1 < 0 or j+y1 > 399 or j-y1 < 0:
        print(1)
        return 1
    elif img_otsu[i+x1, j+y1] > 100 & img_otsu[i-x1, j-y1] > 100:
        return 1
    else:
        return 0


# 判断中心点两侧满足是否要求
def point_detect(img, i, j):
    rbeg = max(0, i-20)
    rend = min(rbeg+41, 450)
    rbeg = rend - 41
    cbeg = max(0, j-20)
    cend = min(cbeg+41, 400)
    cbeg = cend - 41
    print(cend, cbeg)
    img_ori = img[rbeg:rend, cbeg:cend]
    # cv2.imshow('im', img_ori)
    edges = cv2.Canny(img_ori, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 1, minLineLength=18, maxLineGap=10)
    if lines is not None:  # 判断非空，排除骨架中的孤立点
        L_judge = 0
        # 遍历每条直线
        for line in lines:
            # 获取直线上两点
            x1, y1, x2, y2 = line[0]
            # 计算直线斜率
            y0 = y2 - y1
            x0 = x2 - x1
            s0 = np.sqrt(x0*x0+y0*y0)
            L_judge += lines_detect(i, j, y0, x0, s0)
            # print('L:', L_judge)
        # 黑色返回1， 白色返回0
        if L_judge == 0:
            return 0
        else:
            return 1
    else:
        return 0


# 读取图像

img = cv2.imread('D:/bishe/picture/roi/(0, 3).jpg', 0)

# 阈值化
k = np.ones((10, 10), np.uint8)
bi = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k)
t2, img_otsu = cv2.threshold(bi, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# 骨架提取
img_skel = skeleton(img_otsu)
width, height = img_skel.shape
print(width, height)

# 宽度计算
i, j = 0, 0
u = 0
# u = u*point_detect(img_skel, 141, 399)
for i in range(width):
    for j in range(height):
        if img_skel[i, j] >= 200:
            print(i, j)
            u = u*point_detect(img_skel, i, j)  # u为0代表合格点，1代表不合格点
        if u == 5:
            print('error')
            error_points.append((i, j))


cv2.imshow('2', img_skel)
cv2.waitKey()

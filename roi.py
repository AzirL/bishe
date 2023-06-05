def roi(img):
    import cv2
    i = 0
    j = 0
    while i < 4:
        while j < 4:
            imgC = img[400 * i:400 * (i + 1), 400 * j:400 * (j + 1)]
            cv2.namedWindow(str(i) + ", " + str(j), cv2.WINDOW_FREERATIO)
            cv2.imshow(str(i) + ", " + str(j), imgC)
            # cv2.imwrite(f"D:/bishe/picture/roi/{i, j}.jpg", imgC)
            j = j + 1
        i = i + 1
        j = 0

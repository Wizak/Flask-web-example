import random
import numpy as np
import cv2

from PIL import Image, ImageDraw


def efect_photo(mode, into='static/other/ni_photo.jpg', out='static/other/ni_photo_after.jpg'):
    image = Image.open(into)  
    draw = ImageDraw.Draw(image)
    width = image.size[0]  
    height = image.size[1]  	
    pix = image.load() 

    if (mode == 'gray'):
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                draw.point((i, j), (S, S, S))
    elif (mode == 'sepia'):
        depth = 50
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                a = S + depth * 2
                b = S + depth
                c = S
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
    elif (mode == 'negative'):
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255 - a, 255 - b, 255 - c))
    elif (mode == 'noise'):
        factor = 70
        for i in range(width):
            for j in range(height):
                rand = random.randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
    elif (mode == 'blackwhite'):
        factor = 80
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))

    image.save(out, "JPEG")
    del draw


def efect_video(mode, frame):
    def distort(image):
        def convert(image, alpha=1, beta=0):
            tmp = image.astype(float) * alpha + beta
            tmp[tmp < 0] = 0
            tmp[tmp > 255] = 255
            image[:] = tmp

        image = image.copy()

        if random.randrange(2):
            convert(image, beta=random.uniform(-32, 32))

        if random.randrange(2):
            convert(image, alpha=random.uniform(0.5, 1.5))

        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if random.randrange(2):
            tmp = image[:, :, 0].astype(int) + random.randint(-18, 18)
            tmp %= 180
            image[:, :, 0] = tmp

        if random.randrange(2):
            convert(image[:, :, 1], alpha=random.uniform(0.5, 1.5))

        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

        return image 

    def filter_color(img, color):
        frame = cv2.GaussianBlur(img, (3,3), 0) 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if color == 'red':
            lower_color= np.array([0, 50, 70])
            upper_color = np.array([9, 255, 255])
        elif color == 'green':
            lower_color= np.array([36, 50, 70])
            upper_color = np.array([89, 255, 255])
        elif color == 'blue':
            lower_color= np.array([90, 50, 70])
            upper_color = np.array([128, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(frame,frame, mask=mask)

        return res

    def choose(mode, frame):
        if mode == 0:
            return distort(frame)
        elif mode == 1:
            return filter_color(frame, 'red')
        elif mode == 2:
            return filter_color(frame, 'green')
        elif mode == 3:
            return filter_color(frame, 'blue')

    res = choose(mode, frame)
    return res
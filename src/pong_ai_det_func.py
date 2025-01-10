from PIL import ImageGrab
import numpy as np
import pyautogui
import cv2
import time

'''
TOP, LEFT, BOTTOM, RIGHT = 362, 236, 822, 887
ENEMY_X = 275 - LEFT
FRIENDLY_X = 850 - LEFT
Y_RANGE = [TOP + 5 - TOP, BOTTOM - 5 - TOP]
BALL_TOP, BALL_LEFT, BALL_BOTTOM, BALL_RIGHT = 454 - TOP, 284 - LEFT, 821 - TOP, 839 - LEFT
'''


TOP, LEFT, BOTTOM, RIGHT = 379, 245, 816, 890
ENEMY_X = 280 - LEFT
FRIENDLY_X = 855 - LEFT
Y_RANGE = [TOP + 5 - TOP, BOTTOM - 5 - TOP]
BALL_TOP, BALL_LEFT, BALL_BOTTOM, BALL_RIGHT = 453 - TOP, 295 - LEFT, 815 - TOP, 840 - LEFT

def draw_rect(img_arr, r, c, width):

    for i in range(r, r+10, 3):
        for j in range(c, c+10, 3):
            if i > 0 and j > 0 and i < BOTTOM - TOP and j < RIGHT - LEFT:
                img_arr[i, j] = 255 
    
    return img_arr

def draw_line(img_arr, r1, c1, r2, c2):
    global slope, b
    
    x1 = c1
    x2 = c2
    y1 = r1
    y2 = r2

    max_x = len(img_arr[0])
    max_y = len(img_arr)

    if x2 - x1 == 0: 
        print("UNDEFINED TRIGGERED")
        # TODO 
        # MARK THE SLOPE AS UNDEFINED
        slope = None
        b = None

        temp_y = [y1, y2]
        
        y1 = min(temp_y[0], temp_y[1])
        y2 = max(temp_y[0], temp_y[1])
        
        for i in range(y1, y2, 1):
            # SINCE X2 == X1, EITHER X1 OR X2 WORK FOR THE Y-COORDINATE
            img_arr[i, x1] = 100
        return img_arr
    
    # GUARRANTEED TO NEVER BE UNDEFINED BECAUSE OF THE CONDITION ON TOP
    slope = (y2 - y1) / (x2 - x1)
    b = y1 - (slope * x1)

    temp_x = [x1, x2]

    x1 = min(temp_x[0], temp_x[1])
    x2 = max(temp_x[0], temp_x[1])

    x1 = max(0, x1)
    x2 = min(max_x-1, x2)

    for i in range(x1, x2, 1):
        y_result = round((slope * i) + b)
        
        if y_result >= 0 and y_result < max_y:
            img_arr[y_result][i] = 100

    return img_arr

def bounds(img_arr, r1, c1, r2, c2):
    global slope, b

    x1 = c1
    x2 = c2
    y1 = r1
    y2 = r2

    predicted_pos = []

    if x2 > x1:
        y_result = round((slope * BALL_RIGHT) + b)
        
        if y_result > BALL_TOP and y_result < BALL_BOTTOM:
            predicted_pos = [y_result, BALL_RIGHT]
            #print("right")

        elif y_result < BALL_TOP:
            intercept = round((BALL_TOP - b) / slope)
            predicted_pos = [BALL_TOP, intercept]
            #print("top")

        elif y_result > BALL_BOTTOM:
            intercept = round((BALL_BOTTOM - b) / slope)
            predicted_pos = [BALL_BOTTOM, intercept]
            #print("bottom")
    
    elif x1 > x2: 
        y_result = round((slope * BALL_LEFT) + b)
        
        if y_result >= BALL_TOP and y_result <= BALL_BOTTOM:
            predicted_pos = [y_result, BALL_LEFT]
            #print("left")
        
        elif y_result < BALL_TOP:
            intercept = round((BALL_TOP - b) / slope)
            predicted_pos = [BALL_TOP, intercept]
            #print("top")

        elif y_result > BALL_BOTTOM:
            intercept = round((BALL_BOTTOM - b) / slope)
            predicted_pos = [BALL_BOTTOM, intercept]
            #print("bottom")
    
    return predicted_pos

def find_ball(img_arr):

    ball_pos = None
    found_ball = 0

    for i in range(BALL_TOP, BALL_BOTTOM, 10):
        for j in range(BALL_LEFT, BALL_RIGHT, 10):
            ball_pixels = img_arr[i][j]

            if j < 558 - LEFT or j > 580 - LEFT:

                if ball_pixels > 10:
                    ball_pos = [i, j]
                    found_ball = 1
                    break

        if found_ball:
            break

    return ball_pos

def screen_shot():
    gray_image = np.array(ImageGrab.grab(bbox=(LEFT, TOP, RIGHT, BOTTOM)))
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    return gray_image

def refraction(direction, predicted_pos):        
    global slope, b
    
    x = predicted_pos[1]
    y = predicted_pos[0]

    #print(f"SLOPE BEFORE: m: {slope}, b: {b}")

    slope *= -1
    b = y - (slope * x)

    #print(f"SLOPE AFTER: m: {slope}, b: {b}")

    refracted_pos = []

    if direction == "right":
        # right
        y_result = round((slope * BALL_RIGHT) + b)
        refracted_pos = [y_result, BALL_RIGHT]

    elif direction == "left": 
        # left
        y_result = round((slope * BALL_LEFT) + b)
        refracted_pos = [y_result, BALL_LEFT]
        
    return refracted_pos

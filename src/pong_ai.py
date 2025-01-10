import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui

from pong_ai_det_func import *

curr_ball_pos, prev_ball_pos = None, None
b, slope = None, None
last_direction = "None"

def find_pongs(img_arr):

    enemy_y = []
    enemy_pos = 0

    friendly_y = []
    friendly_pos = 0

    for y_pos in range(Y_RANGE[0], Y_RANGE[1], 10):
        friendly_pixels = img_arr[y_pos, FRIENDLY_X]

        if friendly_pixels > 10:
            friendly_y.append(y_pos)

        friendly_pos = 0 if len(friendly_y) == 0 else sum(friendly_y) // len(friendly_y)

    return friendly_pos
    
def det_algo():
    global curr_ball_pos, prev_ball_pos, last_direction

    gray_image = None
    gray_image_2 = None

    while not prev_ball_pos or not curr_ball_pos:
        gray_image = screen_shot()
        time.sleep(.002)
        gray_image_2 = screen_shot()

        prev_ball_pos = find_ball(gray_image)
        curr_ball_pos = find_ball(gray_image_2)

    '''
    cv2.imshow('window', gray_image)
    cv2.imshow('window', gray_image_2)
    
    cv2.waitKey(0)
    '''

    friendly_position = find_pongs(gray_image_2)

    gray_image_2 = draw_line(gray_image_2, prev_ball_pos[0], prev_ball_pos[1], curr_ball_pos[0], curr_ball_pos[1])
    gray_image_2 = draw_rect(gray_image_2, curr_ball_pos[0], curr_ball_pos[1], 15)

    predicted_pos = bounds(gray_image_2, prev_ball_pos[0], prev_ball_pos[1], curr_ball_pos[0], curr_ball_pos[1])
    #print(predicted_pos)

    if predicted_pos == []:
        if  friendly_position - (Y_RANGE[0] + Y_RANGE[1]) // 2 > 0:
            if last_direction != "up":
                pyautogui.keyDown('up')
                last_direction = "up"
            
            elif last_direction != "down":
                pyautogui.keyDown('down')
                last_direction = "down"

        return gray_image_2

    direction = ""
    if prev_ball_pos[1] >= curr_ball_pos[1]: 
        direction = "left"
    elif prev_ball_pos[1] < curr_ball_pos[1]:
        direction = "right"

    gray_image_2 = draw_rect(gray_image_2, predicted_pos[0], predicted_pos[1], 15)

    while(predicted_pos[0] == BALL_BOTTOM or predicted_pos[0] == BALL_TOP):
        prev_predicted_pos = predicted_pos
        predicted_pos = refraction(direction, predicted_pos)
        predicted_pos = bounds(gray_image_2, prev_predicted_pos[0], prev_predicted_pos[1], predicted_pos[0], predicted_pos[1])
        gray_image_2 = draw_rect(gray_image_2, predicted_pos[0], predicted_pos[1], 15)
        gray_image_2 = draw_line(gray_image_2, prev_predicted_pos[0], prev_predicted_pos[1], predicted_pos[0], predicted_pos[1])

    if friendly_position - predicted_pos[0] > 10:
        if last_direction != "up":
            #pyautogui.keyUp('down')
            pyautogui.keyDown('up')
            last_direction = "up"
    
    elif predicted_pos[0] - friendly_position > 10:
        if last_direction != "down":
            #pyautogui.keyUp('up')
            pyautogui.keyDown('down')
            last_direction = "down"

    else:
        if last_direction != "None":
            #pyautogui.keyUp('up')
            #pyautogui.keyUp('down')
            last_direction = "None"

    return gray_image_2

time.sleep(1)

def screen_record(): 
    global curr_ball_pos, prev_ball_pos
    global delta_time

    while(True):
        gray_image = det_algo()
        curr_ball_pos, prev_ball_ps = None, None
        
        cv2.imshow('window', gray_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
screen_record()

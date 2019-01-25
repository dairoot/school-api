# -*- coding: utf-8 -*-
"""
    school_api.check_code.predict
    ~~~~~~~~~~~~~~~~
    This module provides functions for Identification verification code

    :copyright: (c) 2018 by dairoot.
    :license: MIT, see LICENSE for more details.
"""
import os
from io import BytesIO
import numpy as np
from PIL import Image


class CheckCode(object):
    """ 正方系统验证码识别 """
    data_file = os.path.dirname(os.path.realpath(__file__)) + '/theta.dat'
    real_all_theta = np.matrix(np.loadtxt(data_file)).transpose()

    def __init__(self):
        self.img = None

    def photo_to_text(self):
        '''
        图片转数据
        '''
        x_size, y_size = self.img.size
        y_size -= 5
        piece = (x_size - 22) // 8
        centers = [4 + piece * (2 * i + 1) for i in range(4)]
        photo_data = []
        for center in centers:
            single_img = self.img.crop((center - (piece + 2), 1, center + (piece + 2), y_size))
            width, height = single_img.size
            photo_data_x = []
            for h_index in range(0, height):
                for w_index in range(0, width):
                    pixel = single_img.getpixel((w_index, h_index))
                    photo_data_x.append(int(pixel == 255))
            photo_data.append(photo_data_x)
        return photo_data

    def verify(self, img_stream):
        '''
        将图片转成numpy数组数据 与 训练好的模型 进行匹配
        '''
        obj = BytesIO(img_stream)
        img = Image.open(obj).convert("L")
        self.img = self.denoise_img(img)
        data = np.matrix(self.photo_to_text())
        data = np.hstack((np.ones((data.shape[0], 1)), data))
        all_predict = 1.0 / (1.0 + np.exp(-(np.dot(data, self.real_all_theta))))
        pred = np.argmax(all_predict, axis=1)
        answers = map(chr, map(lambda x: x + 48 if x <= 9 else x + 87, pred))
        return ''.join(answers)

    @staticmethod
    def denoise_img(img):
        '''图片降噪处理'''
        img2 = Image.new("L", img.size, 255)
        for x in range(img.size[1]):
            for y in range(img.size[0]):
                pix = img.getpixel((y, x))
                if pix == 17:  # these are the numbers to get
                    img2.putpixel((y, x), 0)
        return img2

import cv2
import airtest.core.api as air_api
from airtest.core.helper import G
import numpy as np

air_api.auto_setup(__file__, logdir=True, devices=["Android:///", ])


def get_resolution():
    height = G.DEVICE.display_info['height']
    width = G.DEVICE.display_info['width']
    return width, height


def img_scale(image, scale=2):
    # 输入你想要resize的图像高。
    height, width = image.shape[0], image.shape[1]
    # 获得相应等比例的图像宽度。
    width_size = int(width / scale)
    height_size = int(height / scale)
    # resize
    image_resize = cv2.resize(image, (width_size, height_size))
    return image_resize


def get_screenshot(scale=1):
    img = G.DEVICE.snapshot()
    img = np.array(img)
    return img_scale(img, scale)

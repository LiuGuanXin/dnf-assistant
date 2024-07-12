from paddleocr import PaddleOCR
from tools.image_deal import get_default_img, get_default_region


# https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/quickstart.md

class pd_ocr:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    def detect_rechallenge(self, text='再次挑战地下城') -> []:
        img = get_default_img()
        result = self.ocr.ocr(img, cls=True)
        for line in result[0]:
            center_x = (line[0][0][0] + line[0][1][0] + line[0][2][0] + line[0][3][0]) / 4
            center_y = (line[0][0][1] + line[0][1][1] + line[0][2][1] + line[0][3][1]) / 4
            if line[1][1] > 0.8 and text == line[1][0]:
                return [center_x, center_y]
        return []

    def confirm_challenge(self, text='本次登录期间不再显示') -> []:
        img = get_default_img()
        _, _, w, _ = get_default_region()
        result = self.ocr.ocr(img, cls=True)
        select = []
        confirm = []
        for line in result[0]:
            if line[1][1] > 0.8 and text == line[1][0]:
                left_x = line[0][0][0] - w / 35
                center_y = (line[0][0][1] + line[0][2][1]) / 2
                select = [left_x, center_y]
            elif line[1][1] > 0.8 and "确认" == line[1][0]:
                center_x = (line[0][0][0] + line[0][2][0]) / 2
                center_y = (line[0][0][1] + line[0][2][1]) / 2
                confirm = [center_x, center_y]
        return select, confirm

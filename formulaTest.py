# -*- coding: UTF-8 -*-
import os

from pix2text import Pix2Text
import Enhancement_Test
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
def OCRAndFormulaProcess(cropsPath):
    img_fp = cropsPath
    try:
        p2t = Pix2Text(analyzer_config=dict(model_name='mfd'))
        outs = p2t(img_fp, resized_shape=600)  # 也可以使用 `p2t.recognize(img_fp)` 获得相同的结果
        # print("outs:{}".format(outs))
        # for out in outs:
            # print("position:{},{},{},{}".format(x1, y1, x2, y2))
        # 如果只需要识别出的文字和Latex表示，可以使用下面行的代码合并所有结果
        only_text = '\n'.join([out['text'] for out in outs])
        if "m°" in only_text or "m/" in only_text or "m'" in only_text:
            only_text = only_text.replace("m°", "^3")
            only_text = only_text.replace("m/", "m^3/")
            only_text = only_text.replace("m'", "m^3")

        return only_text
    except:
        print("这有个错误")
        return ''

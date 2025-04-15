import time
import cv2

from hand_recognition import hand_detector as hd, hand_recognition_config as hrc
from image_capture import capture, image_capture_config as icc
from color_recognition import color_detector as cd, color_recognition_config as crc


# config 的路径可自定义，如果不存在，将自动创建，并生成默认的配置文件
# hand_detector_config = hrc.Config('config/hand_recognition_config.yaml')
# hand_detector = hd.HandDetector(hand_detector_config)

capture_config = icc.Config('config/image_capture_config.yaml')
image_capture = capture.ImageCapture(capture_config)

color_detector_config = crc.Config('config/color_recognition_config.yaml')
color_detector = cd.ColorDetector(color_detector_config)

# # hand_detector.debug() 用于可视化修改roi，鼠标左键设置两个点用于划定roi区域，按q退出并自动将roi保存到配置文件中
# hand_detector.debug(get_frame_callback = image_capture.get_frame)

# # hand_detector.detect() 返回单帧识别的结果
# while True:
#     print(hand_detector.detect(image_capture.get_frame()))

time.sleep(3)
# color_detector.debug_roi(get_frame_callback = image_capture.get_frame)
# color_detector.debug_color(get_frame_callback = image_capture.get_frame)

while True:
    image = image_capture.get_frame()
    print(color_detector.detect(image))

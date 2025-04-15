import cv2
import pyrealsense2 as rs
import numpy as np

from .image_capture_config import Config, CameraType
from .exceptions import *


class ImageCapture:
    _config: Config
    _cap: cv2.VideoCapture
    
    _rs_pipeline = None
    _rs_config = None
    _rs_profile = None
    _rs_sensor = None

    def __init__(self, config: Config):
        self._config = config

        # 初始化realsense
        if self._config.camera_config.camera_type == CameraType.REALSENSE:
            # 获取图像长宽
            frame_width = self._config.camera_config.realsense_width
            frame_height = self._config.camera_config.realsense_height
            # 配置彩色流
            self._rs_pipeline = rs.pipeline() 
            self._rs_config = rs.config() 
            self._rs_config.enable_stream(rs.stream.color, 
                                            frame_width, 
                                            frame_height, 
                                            rs.format.bgr8, 
                                            self._config.camera_config.realsense_fps)
            # 启动RealSense摄像头 
            self._rs_profile = self._rs_pipeline.start(self._rs_config) 
            # self._rs_sensor = self._rs_profile.get_device().query_sensors()[1]
            # self._rs_sensor.set_option(rs.option.enable_auto_exposure, False) 
            
            return

        # 使用索引初始化摄像头
        if self._config.camera_config.camera_type == CameraType.INDEX:
            self._cap = cv2.VideoCapture(0)
            return

    def get_frame(self):
        cv_frame = None
        # 根据摄像头类型获取一帧图像
        if self._config.camera_config.camera_type == CameraType.REALSENSE:
            # 从realsense中获取一帧图像
            frames = self._rs_pipeline.wait_for_frames()
            color_frame = frames.get_color_frame() 
            # 转换为OpenCV格式 
            cv_frame = np.asanyarray(color_frame.get_data())
            return cv_frame
        
        elif self._config.camera_config.camera_type == CameraType.INDEX:
            # 从摄像头中获取一帧图像
            ret, cv_frame = self._cap.read()
            if not ret:
                raise VideoCaptureReadException('VideoCaptureReadException: read frame failed!')
            return cv_frame
        
        elif self._config.camera_config.camera_type == CameraType.WEBCAMERA:
            raise CameraTypeErrorException('CameraTypeErrorException: camera type is not supported, this feature has not been developed yet!')


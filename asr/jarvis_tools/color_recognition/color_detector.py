from collections import deque
from ruamel.yaml import YAML, CommentedMap
import numpy as np
import cv2

from .color_recognition_config import Config
from .exceptions import *

class ColorDetector:
    _config: Config
    _frame_width: int
    _frame_height: int
    _mp_hands: None

    def __init__(self, config: Config):
        self._config = config
        self.roi_dict = config.detect_config.color_recognition_list.roi
        self.color_dict = config.detect_config.color_recognition_list.color

    def _visulize_roi(self, cv_frame, debug_roi, track_points):
        # 边框颜色
        green = (0,255,0)
        red = (0,0,255)

        frame = cv_frame.copy()
        roi_overlay = cv_frame.copy()
        
        # 处理鼠标轨迹点
        if track_points:
            for point in track_points:
                cv2.circle(frame, point, 5, (0,100,250), -1)

        # 绘制roi边框
        roi_num = 0
        for roi in debug_roi:
            roi_x1, roi_y1, roi_x2, roi_y2 = roi
            
            cv2.rectangle(frame,  (roi_x1, roi_y1), (roi_x2, roi_y2), red, 2)
            cv2.putText(frame, str(roi_num), (roi_x1, roi_y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, red, 2)

            roi_num += 1
        
        imshow_frame = frame.copy()
        # 绘制roi区域
        for roi in debug_roi:
            roi_x1, roi_y1, roi_x2, roi_y2 = roi
            
            cv2.rectangle(roi_overlay, (roi_x1, roi_y1), (roi_x2, roi_y2), green, -1)
            
            # 透明度控制
            alpha = 0.15  
            imshow_frame = cv2.addWeighted(roi_overlay, alpha, frame, 1 - alpha, 0)
                    

        cv2.imshow('Color Recognition Visulize Debug', imshow_frame)

    def detect(self, image):
        # 判断输入的参数是否合法
        if image is None:
            raise ImageEmptyException('ImageEmptyException: image is empty!')
        
        # 获取识别的颜色
        color_dict = self.color_dict
        
        # 将BGR图像转换为HSV图像
        hsv_image = cv2.cvtColor(image,  cv2.COLOR_BGR2HSV)
        
        result = {}
        for roi_name, roi in self.roi_dict.items():
            # 当前roi内是否检测到颜色
            hit = False
            # 获取roi坐标
            roi_x1 = roi[0]
            roi_y1 = roi[1]
            roi_x2 = roi[2]
            roi_y2 = roi[3]

            # 获取roi区域
            roi_image = hsv_image[roi_y1:roi_y2, roi_x1:roi_x2]
            
            # 识别每一种颜色
            # color的格式 {str ： ColorData, ...}
            for color_name, color_data in color_dict.items():
                # 获取颜色阈值
                lower = np.array(color_data.hsv_min)
                upper = np.array(color_data.hsv_max)
                mask = cv2.inRange(roi_image, lower, upper)

                # 腐蚀膨胀
                kernel = np.ones((5,5),  np.uint8)
                morphology_result = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

                # 计算颜色占比
                confidence = color_data.confidence
                
                white_pixels = cv2.countNonZero(mask)
                total_pixels = morphology_result.shape[0] * morphology_result.shape[1]
                ratio = white_pixels / total_pixels 
                if ratio > confidence:
                    if hit:
                        raise ColorAlreadyFoundException('ColorAlreadyFoundException: This area has been detected as another color!')
                    result[roi_name] = color_name
                    hit = True

        return result
    
    def debug_roi(self, image = None, get_frame_callback = None):
        if image is None and get_frame_callback is None:
            raise DebugParameterErrorException('DebugParameterErrorException: image and get_frame_callback cannot be empty at the same time!')
        if image is not None and get_frame_callback is not None:
            raise DebugParameterErrorException('DebugParameterErrorException: Only one of image and get_frame_callback can exist at the same time!')
        
        # 鼠标点击的记录点
        track_points = deque(maxlen=2)
        # roi坐标
        debug_roi = []

        # cv窗口鼠标回调           
        def mouse_callback(event, x, y, flags, param):       
            if event == cv2.EVENT_LBUTTONDOWN:
                track_points.append((x, y))
                
                # 点击第一次记录起点，第二次记录终点
                if len(track_points) >= 2:
                    x1 = min(track_points[0][0], track_points[1][0])
                    y1 = min(track_points[0][1], track_points[1][1])
                    x2 = max(track_points[0][0], track_points[1][0])
                    y2 = max(track_points[0][1], track_points[1][1])
                
                    debug_roi.append([x1, y1, x2, y2])
                    
                    print(f'add roi [x1, y1, x2, y2]: [{x1}, {y1}, {x2}, {y2}]')

                    track_points.clear()

        # 设置cv窗口和鼠标事件回调
        cv2.namedWindow('Color Recognition Visulize Debug')
        cv2.setMouseCallback('Color Recognition Visulize Debug', mouse_callback)

        while cv2.waitKey(1) != ord('q'):
            cv_frame = None
            # 获取调试的图像
            if get_frame_callback is not None:
                cv_frame = get_frame_callback()
            else:
                cv_frame = image

            # 显示debug信息
            self._visulize_roi(cv_frame, debug_roi, track_points)
            
            if cv2.waitKey(1) == ord('c') and len(debug_roi) != 0:
                debug_roi.pop()


        if len(debug_roi) == 0:
            return
        
        # 输入roi名称
        print(f'请输入{len(debug_roi)}个roi的名称，以空格分隔：')
        roi_names = list(dict.fromkeys(input().split(' ')))

        while len(debug_roi) != len(roi_names):
            print('roi数量和名称数量不匹配或roi名称重复，请重新输入：')
            roi_names = list(dict.fromkeys(input().split(' ')))
        
        roi_dict = {}
        for i in range(len(debug_roi)):
            roi_dict[roi_names[i]] = debug_roi[i]

        # 保存roi到配置文件
        yaml = YAML()
        yaml.indent(mapping=2,  sequence=4, offset=2)
        
        with open(self._config.config_file, 'r') as f:
            data = yaml.load(f)

        data['detect_config']['color_recognition_list']['roi'] = roi_dict

        with open(self._config.config_file, 'w') as f:
            yaml.dump(data, f)
            
        cv2.destroyAllWindows() 
        print('roi信息已写入配置文件！')
        
    def debug_color(self, image = None, get_frame_callback = None, custom_pick = False):
        if image is None and get_frame_callback is None:
            raise DebugParameterErrorException('DebugParameterErrorException: image and get_frame_callback cannot be empty at the same time!')
        if image is not None and get_frame_callback is not None:
            raise DebugParameterErrorException('DebugParameterErrorException: Only one of image and get_frame_callback can exist at the same time!')

        # 鼠标点击的记录点
        track_points = deque()

        # cv窗口鼠标回调
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                track_points.append((x, y))
                
        # 设置cv窗口和鼠标事件回调
        cv2.namedWindow('Color Recognition Visulize Debug')
        cv2.setMouseCallback('Color Recognition Visulize Debug', mouse_callback)
        
        # 颜色
        color = {}
        color_data = {}
        color_name = ''
        hsv_min = None
        hsv_max = None
        hsv_list = []

        while cv2.waitKey(1) != ord('q'):
            cv_frame = None
            # 获取调试的图像
            if get_frame_callback is not None:
                cv_frame = get_frame_callback()
            else:
                cv_frame = image
               
            # 自动获取区域的颜色范围
            if not custom_pick:
                hsv_image = cv2.cvtColor(cv_frame,  cv2.COLOR_BGR2HSV)
                
                # 先预显示十帧防止摄像头启动后的色差
                for i in range(10):
                    self._visulize_roi(cv_frame, self.roi_dict.values(), track_points)
                    cv2.waitKey(1)
                
                for roi_name, roi in self.roi_dict.items():
                    self._visulize_roi(cv_frame, self.roi_dict.values(), track_points)
                    
                    # 获取roi坐标
                    roi_x1 = roi[0]
                    roi_y1 = roi[1]
                    roi_x2 = roi[2]
                    roi_y2 = roi[3]

                    # 获取roi区域
                    roi_image = hsv_image[roi_y1:roi_y2, roi_x1:roi_x2]
                
                    height = roi_image.shape[0]
                    width = roi_image.shape[1]
                    # 遍历roi区域，获取最值
                    hsv_list = []
                    for y in range(height):
                        for x in range(width):
                            hsv_list.append(roi_image[y, x])
                    hsv_min = np.min(hsv_list, axis=0)
                    hsv_max = np.max(hsv_list, axis=0)
                    
                    # 保存为ColorData
                    color = {'hsv_min': hsv_min.tolist(), 'hsv_max': hsv_max.tolist(), 'confidence': 0.7}
                    color_name = input(f'输入区域"{roi_name}"颜色名: ')
                    color_data[color_name] = color
                    
                break
                
            # 手动选择颜色点
            if custom_pick:
                self._visulize_roi(cv_frame, self.roi_dict.values(), track_points)
                
                # 添加当前颜色
                if cv2.waitKey(1) == ord('a') and len(track_points) != 0:
                    # 计算鼠标点击点的hsv_min和hsv_max
                    hsv_image = cv2.cvtColor(cv_frame,  cv2.COLOR_BGR2HSV)
                    for point in track_points:
                        hsv_list.append(hsv_image[point[1], point[0]])
                    print(hsv_list)
                    hsv_min = np.min(hsv_list, axis=0)
                    hsv_max = np.max(hsv_list, axis=0)
                    
                    # 保存为ColorData
                    color = {'hsv_min': hsv_min.tolist(), 'hsv_max': hsv_max.tolist(), 'confidence': 0.7}
                    color_name = input('输入颜色名: ')
                    color_data[color_name] = color
                    
                    track_points.clear()
                    
                if cv2.waitKey(1) == ord('c'):
                    track_points.clear()

        if len(color_data) == 0:
            return
        
        # 保存颜色字典到配置文件
        yaml = YAML()
        yaml.indent(mapping=2,  sequence=4, offset=2)
        
        with open(self._config.config_file, 'r') as f:
            data = yaml.load(f)

        data['detect_config']['color_recognition_list']['color'] = CommentedMap(color_data)

        with open(self._config.config_file, 'w') as f:
            yaml.dump(data, f)
            
        cv2.destroyAllWindows() 
        print('roi信息已写入配置文件！')
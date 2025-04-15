from collections import deque
from ruamel.yaml import YAML
import mediapipe as mp 
import cv2

from .hand_recognition_config import Config
from .exceptions import *

class HandDetector:
    _config: Config
    _frame_width: int
    _frame_height: int
    _mp_hands: None

    def __init__(self, config: Config):
        self._config = config

        # 初始化MediaPipe手部检测 
        self._mp_hands = mp.solutions.hands.Hands( 
            static_image_mode = self._config.detect_config.static_image_mode,
            max_num_hands = self._config.detect_config.max_num_hands,
            model_complexity = self._config.detect_config.model_complexity,
            min_detection_confidence = self._config.detect_config.min_detection_confidence,
            min_tracking_confidence = self._config.detect_config.min_tracking_confidence)
        self._mp_drawing = mp.solutions.drawing_utils

    def _get_roi(self):
        roi_x_list = [self._config.detect_config.roi_x1, self._config.detect_config.roi_x2]
        roi_y_list = [self._config.detect_config.roi_y1, self._config.detect_config.roi_y2]
        roi_x1 = min(roi_x_list)
        roi_y1 = min(roi_y_list)
        roi_x2 = max(roi_x_list)
        roi_y2 = max(roi_y_list)

        return deque([roi_x1, roi_y1, roi_x2, roi_y2])

    def _visulize(self, cv_frame, inbox_hand_landmarks, 
                  track_points, roi_x1, roi_y1, roi_x2, roi_y2):
        # 边框颜色
        green = (0,255,0)
        red = (0,0,255)
        # 绘制roi区域
        frame = cv_frame.copy()
        overlay = cv_frame.copy()
        cv2.rectangle(overlay, (roi_x1, roi_y1), (roi_x2, roi_y2), green, -1)
        
        # 透明度控制
        alpha = 0.15  
        frame = cv2.addWeighted(overlay, alpha, cv_frame, 1 - alpha, 0)

        # 处理鼠标轨迹点
        if track_points:
            for point in track_points:
                cv2.circle(frame, point, 5, (0,100,250), -1)

        # 绘制roi边框
        cv2.rectangle(frame,  (roi_x1, roi_y1), (roi_x2, roi_y2), red, 2)

        if len(inbox_hand_landmarks) > 0:
            # 绘制检测成功信息
            cv2.putText(frame, "HAND DETECTED", (roi_x1, roi_y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, green, 2)
            cv2.rectangle(frame,  (roi_x1, roi_y1), (roi_x2, roi_y2), green, 2)
            
            # 绘制手部关键点
            point_num = 0
            for hand_landmarks in inbox_hand_landmarks:
                for hand_landmark in hand_landmarks.landmark:
                    landmark_x = int(hand_landmark.x * self._frame_width)
                    landmark_y = int(hand_landmark.y * self._frame_height)
                    cv2.putText(frame,  str(point_num), (landmark_x, landmark_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2)
                    point_num += 1
                    
                mp.solutions.drawing_utils.draw_landmarks( 
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS) 
                    
        cv2.imshow('Hand Recognition Debug', frame)

    def detect(self, image, roi = None, roi_debug = False):
        if image is None:
            raise ImageEmptyException('ImageEmptyException: image is None!')
        
        # 获取识别的图像长宽
        cv_frame = image
        self._frame_width = image.shape[1]
        self._frame_height = image.shape[0]

        # 手部检测
        results = self._mp_hands.process(cv2.cvtColor(cv_frame,  cv2.COLOR_BGR2RGB))

        # 处理识别结果
        in_box_hand_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 获取识别的判定点
                decision_point = self._config.detect_config.decision_point
                if (decision_point > 20 or decision_point < 0):
                    raise DecisionPointOutOfRangeException(
                        'DecisionPointOutOfRangeException: decison_point out of range!')
                
                # 获取手掌根部坐标 
                hand_x = int(hand_landmarks.landmark[decision_point].x  * self._frame_width)
                hand_y = int(hand_landmarks.landmark[decision_point].y  * self._frame_height)
                
                # 获取roi坐标
                if roi is None:
                    roi_x1, roi_y1, roi_x2, roi_y2 = self._get_roi()
                else:
                    roi_x1, roi_y1, roi_x2, roi_y2 = roi

                # 判断是否在框内 
                in_box = ((roi_x1 < hand_x < roi_x2 ) and (roi_y1 < hand_y < roi_y2))             

                if in_box:
                    in_box_hand_landmarks.append(hand_landmarks)

        if roi_debug:
            return in_box_hand_landmarks
        
        return len(in_box_hand_landmarks)
    
    def debug(self, image = None, get_frame_callback = None):
        if image is None and get_frame_callback is None:
            raise DebugParameterErrorException('DebugParameterErrorException: image and get_frame_callback cannot be empty at the same time!')
        if image is not None and get_frame_callback is not None:
            raise DebugParameterErrorException('DebugParameterErrorException: Only one of image and get_frame_callback can exist at the same time!')
        
        # 鼠标点击的记录点
        track_points = deque(maxlen=2)
        # 获取roi坐标
        debug_roi = self._get_roi()

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
                
                    debug_roi.clear()
                    debug_roi.append(x1)
                    debug_roi.append(y1)
                    debug_roi.append(x2)
                    debug_roi.append(y2)
                    
                    print(f'change roi[x1, y1, x2, y2] to: [{debug_roi[0]}, {debug_roi[1]}, {debug_roi[2]}, {debug_roi[3]}]')

                    track_points.clear()

        # 设置cv窗口和鼠标事件回调
        cv2.namedWindow('Hand Recognition Debug')
        cv2.setMouseCallback('Hand Recognition Debug', mouse_callback)

        while cv2.waitKey(1) != ord('q'):
            # 获取调试的图像
            if get_frame_callback is not None:
                cv_frame = get_frame_callback()
            else:
                cv_frame = image

            # 获取roi坐标
            roi_x1, roi_y1, roi_x2, roi_y2 = debug_roi

            # 手部检测 
            hand_landmarks = self.detect(cv_frame, debug_roi, True)

            # 显示debug信息
            self._visulize(cv_frame, hand_landmarks, 
                           track_points, roi_x1, roi_y1, roi_x2, roi_y2)

        cv2.destroyAllWindows() 

        # 保存roi到配置文件
        yaml = YAML()
        yaml.indent(mapping=2,  sequence=4, offset=2)
        
        with open(self._config.config_file, 'r') as f:
            data = yaml.load(f)

        data['detect_config']['roi_x1'] = debug_roi[0]
        data['detect_config']['roi_y1'] = debug_roi[1]
        data['detect_config']['roi_x2'] = debug_roi[2]
        data['detect_config']['roi_y2'] = debug_roi[3]

        with open(self._config.config_file, 'w') as f:
            yaml.dump(data, f)
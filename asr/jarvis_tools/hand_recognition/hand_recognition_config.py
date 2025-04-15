import os
from dataclasses import dataclass, field
from ruamel.yaml  import YAML 
from ruamel.yaml.comments  import CommentedMap 

from exceptions import *


@dataclass   
class DetectConfigData:
    static_image_mode: bool = False
    max_num_hands: int = 1
    model_complexity: int = 0
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    decision_point: int = 0
    roi_enable: bool = True
    roi_x1: int = 170
    roi_y1: int = 90
    roi_x2: int = 470
    roi_y2: int = 390
    
    def get_map(self):
        return {'static_image_mode': self.static_image_mode,
                'max_num_hands': self.max_num_hands,
                'model_complexity': self.model_complexity,
                'min_detection_confidence': self.min_detection_confidence,
                'min_tracking_confidence': self.min_tracking_confidence,
                'decision_point': self.decision_point,
                'roi_enable': self.roi_enable,
                'roi_x1': self.roi_x1,
                'roi_y1': self.roi_y1,
                'roi_x2': self.roi_x2,
                'roi_y2': self.roi_y2}
        
    def get_comment_map(self):
        return {
            'static_image_mode' : '是否使用静态图像模式，默认为False',
            'max_num_hands' : '最多检测的手的数量，默认为1',
            'model_complexity' : '模型复杂度，0为低精度模型(使用CPU运算)，1为高精度模型(使用GPU运算，需要安装CUDA)，默认为0',
            'min_detection_confidence' : '最小检测置信度，默认为0.7',
            'min_tracking_confidence' : '最小跟踪置信度，默认为0.5',
            'decision_point': '手掌的哪个节点用于判定，范围为0到20，默认为0',
            'roi_enable' : '是否启用ROI，默认为False',
            'roi_x1' : 'ROI左上角x坐标，默认为170',
            'roi_y1' : 'ROI左上角y坐标，默认为90',
            'roi_x2' : 'ROI右下角x坐标，默认为470',
            'roi_y2' : 'ROI右下角y坐标，默认为390',
        }

@dataclass
class Config:
    config_file: str = './config/hand_recognition_config.yaml'
    detect_config: DetectConfigData = field(default_factory = DetectConfigData) 
    
    def __init__(self, config_file):
        self._init_config(config_file)
       
    def _init_config(self, config_file):
        # 初始化config并从配置文件中读取配置
        self.config_file = config_file
        self.detect_config = DetectConfigData()
        yaml = YAML()
        yaml.indent(mapping=2,  sequence=4, offset=2)

        # 文件不存在则自动创建并生成默认配置
        if not os.path.exists(config_file):
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w') as f:
                yaml.dump(self._get_config_map(), f)

        with open(config_file, 'r') as f:
            config = yaml.load(f)
            self.detect_config = DetectConfigData(**config['detect_config'])

    
    def _get_config_map(self):
        # 序列化的默认config信息
        config_map = CommentedMap()
        config_map['detect_config'] = CommentedMap(self.detect_config.get_map())
        detect_comment_map = self.detect_config.get_comment_map()

        for key, value in detect_comment_map.items():
            config_map['detect_config'].yaml_add_eol_comment(comment = value, key = key)
        
        return config_map
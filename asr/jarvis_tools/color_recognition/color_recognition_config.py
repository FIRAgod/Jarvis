import os
from dataclasses import dataclass, field
from ruamel.yaml  import YAML 
from ruamel.yaml.comments  import CommentedMap 

from .exceptions import *
from .data import ColorRecognitionList


@dataclass   
class DetectConfigData:
    color_recognition_list: ColorRecognitionList = field(default_factory = ColorRecognitionList)
    
    def __init__(self, color_recognition_list = None):
        if color_recognition_list is not None:
            self.color_recognition_list = ColorRecognitionList(color_recognition_list)
        else:
            self.color_recognition_list = ColorRecognitionList()
    
    def get_map(self):
        return {'color_recognition_list' : self.color_recognition_list.get_map()}
    
    def get_comment_map(self):
        return {
            'color_recognition_list': {
                'roi' : '检测区域的列表',
                'color' : '颜色列表'
            } 
        }

@dataclass
class Config:
    config_file: str = './config/color_recognition_config.yaml'
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
        config_map['detect_config'] = CommentedMap()
        config_map['detect_config']['color_recognition_list'] = \
            CommentedMap(self.detect_config.get_map()['color_recognition_list'])
        comment_map = self.detect_config.get_comment_map()  

        for key, value in comment_map['color_recognition_list'].items():
            config_map['detect_config']['color_recognition_list'].\
                yaml_add_eol_comment(comment = value, key = key)
        
        return config_map
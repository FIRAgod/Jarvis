import os
from enum import Enum
from dataclasses import dataclass, field
from ruamel.yaml  import YAML 
from ruamel.yaml.comments  import CommentedMap 

from exceptions import *

class CameraType(Enum):
    REALSENSE = 0
    INDEX = 1
    WEBCAMERA = 2

@dataclass
class CamaraConfigData:
    camera_type: CameraType = CameraType.REALSENSE
    index: int = 0
    realsense_width: int = 640
    realsense_height: int = 480
    realsense_fps: int = 60
    image_server_ip: str = '127.0.0.1'
    image_server_port: int = 14514
    
    def get_map(self):
        return {'camera_type' : self.camera_type.name, 
                'index' : self.index, 
                'realsense_width' : self.realsense_width, 
                'realsense_height' : self.realsense_height, 
                'realsense_fps' : self.realsense_fps, 
                'image_server_ip' : self.image_server_ip, 
                'image_server_port' : self.image_server_port
        }
        
    def get_comment_map(self):
        return {
            'camera_type' : '相机类型: REALSENSE(默认, 使用Intel RealSense相机)，INDEX(使用其他摄像头)，WEBCAMERA(使用网络摄像头，该功能暂未开发，无法使用)',
            'index' : '摄像头索引号, 仅在camera_type为INDEX时有效，默认为0',
            'realsense_width' : 'realsense分辨率宽度，默认为640',
            'realsense_height' : 'realsense分辨率高度，默认为480',
            'realsense_fps' : 'realsense帧率，默认为60',
            'image_server_ip' : '图像服务器IP，默认为127.0.0.1',
            'image_server_port' : '图像服务器端口，默认为14514',
            
        }

@dataclass
class Config:
    config_file: str = './config/camera_config.yaml'
    camera_config: CamaraConfigData = field(default_factory = CamaraConfigData) 

    def __init__(self,  config_file ):
        self._init_config(config_file)
        self._parse_config()

    def _init_config(self, config_file):
        # 初始化config并从配置文件中读取配置
        self.config_file = config_file
        self.camera_config = CamaraConfigData()
        yaml = YAML()
        yaml.indent(mapping=2,  sequence=4, offset=2)

        # 文件不存在则自动创建并生成默认配置
        if not os.path.exists(config_file):
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w') as f:
                yaml.dump(self._get_config_map(), f)

        with open(config_file, 'r') as f:
            config = yaml.load(f)
            self.camera_config = CamaraConfigData(**config['camera_config'])

    

    def _parse_config(self):
        # 根据配置文件中的相机类型解析参数
        if self.camera_config.camera_type == 'INDEX':
            self.camera_config.camera_type = CameraType.INDEX
            return
        
        if self.camera_config.camera_type == 'REALSENSE':
            self.camera_config.camera_type = CameraType.REALSENSE
            return
        
        if self.camera_config.camera_type == 'WEBCAMERA':
            self.camera_config.camera_type = CameraType.WEBCAMERA
            return

        raise CameraTypeErrorException('CameraTypeErrorException: Invalid camera type!')
    
    def _get_config_map(self):
        # 序列化的默认config信息
        config_map = CommentedMap()
        config_map['camera_config'] = CommentedMap(self.camera_config.get_map())

        camera_comment_map = self.camera_config.get_comment_map()

        for key, value in camera_comment_map.items():
            config_map['camera_config'].yaml_add_eol_comment(comment = value, key = key)
        
        return config_map
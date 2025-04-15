from dataclasses import dataclass, field

@dataclass
class ColorData:
    hsv_min: list = field(default_factory = lambda: [0, 0, 0])
    hsv_max: list = field(default_factory = lambda: [180, 255, 255])
    confidence: float = 0.7
    
    def get_map(self):
        return {
            'hsv_min' : self.hsv_min,
            'hsv_max' : self.hsv_max,
            'confidence' : self.confidence
        }

@dataclass
class ColorRecognitionList:
    # roi的格式 {name : [x1, y1, x2, y2], ...}
    roi = {'default_area' : [170, 90, 470, 390]}
    
    # color的格式 {name ： ColorData, ...}
    color = {'default_color' : ColorData()}
    
    def __init__(self, map = None):
        if map is not None:
            self.roi = map['roi']
            self.color = {name : ColorData(**color_data) for name, color_data in map['color'].items()}
    
    def get_map(self):
        result_map = {
            'roi' : self.roi,
            'color' : self.color
        }
        
        # 解包ColorData
        for color_name, color_data in zip(result_map['color'].keys(), result_map['color'].values()):
            result_map['color'][color_name] = color_data.get_map()
            
        return result_map
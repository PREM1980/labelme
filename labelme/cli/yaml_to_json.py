'''
Created on Jul 8, 2018

@author: prem
'''

import argparse
import json
import os
import warnings
import yaml
from labelme import utils
from labelme import logger

# TODO
# - [high] Determine resolution from yaml files.

    
class YamlToJson(object):
    
    def __init__(self, configs_input_dir, image_name):
        self.resolution = .02
        self.tool_input = {}
        self.shapes = []
        self.shape_item = {}
        self.configs_input_dir = configs_input_dir
        self.image_name = image_name
        self.image_loc = self._get_image_loc()
        self.y, self.x, _ = self._get_image_dimension()
        self.run() 
    
    def _get_image_loc(self):
        return os.path.join(os.path.dirname(os.path.normpath(self.configs_input_dir)),'maps',self.image_name)
    
    def _get_image_dimension(self):
        return utils.get_image_dimensions(self.image_loc)
        
    def run(self):
        for filename in os.listdir(self.configs_input_dir):
            if filename.endswith(".yaml"):             
                with open(os.path.join(self.configs_input_dir, filename)) as stream:
                    try:
                        if filename == 'poses.yaml':
                            pass
                        elif filename == 'aisles.yaml':
                            self._process_aisles(stream)
                            self._generate_output_file(filename)
                        elif filename == 'aisle_definitions.yaml':
                            self._process_aisles_definition(stream)
#                             self._generate_output_file(filename)
                        elif filename == 'meta.yaml':
                            pass                                    
                    except yaml.YAMLError as exc:
                        print(exc)
                        return None
        

    def _process_aisles(self, stream):
        data = yaml.load(stream)
        self.shape_item['points'] = []
        for aisle in data['aisles']:
            if aisle[0:1] == 'A':
                aisle_data = data['aisles'][aisle].split()
                self.shape_item['points'].append(
                    [(float(aisle_data[0])/self.resolution),
                     self.y-(float(aisle_data[1])/self.resolution)
                    ])
                self.shape_item['points'].append(    
                    [(float(aisle_data[3])/self.resolution),
                     self.y-(float(aisle_data[4])/self.resolution)])                                                                                            
                self.shapes.append(self.shape_item)
                self.shape_item['line_color'] = None
                self.shape_item['fill_color'] = None
                self.shape_item['label'] = aisle
                self.shape_item['id'] = None
                self.shape_item['store_location'] = None
                self.shape_item['store_name'] = None
                self.shape_item = {}  
                self.shape_item['points'] = []                                                    
#         self.tool_input['shapes'] = sorted(self.shapes, key=self._sort_point_by_x_y_positions)                 
        self.tool_input['shapes'] = sorted(self.shapes, key=self._sort_by_label)
        self.tool_input['lineColor'] = [0,255,0,128]
        self.tool_input['imagePath'] = self.image_name 
        self.tool_input['flags'] = {}
        self.tool_input['fillColor'] = [255,0,0,128]
        self.tool_input['imageData'] = None
        
    def _sort_points_by_x_y_positions(self, item):        
        return item['points'][0][0], item['points'][0][1]
    
    def _sort_by_label(self, item):        
        return item['label']
    
    def _process_aisles_definition(self, stream):
        data = yaml.load(stream)
        self.shape_item['points'] = []
        for k, v in data.items():            
            self.shape_item['points'].append(v['pts'][0])
            self.shape_item['points'].append(v['pts'][1])
            self.shapes.append(self.shape_item)            
            self.shape_item['fill_color'] = None
            self.shape_item['line_color'] = None
            self.shape_item['label'] = k
            self.shape_item['id'] = v['id']
            self.shape_item['store_location'] = v['store_location']
            self.shape_item['store_name'] = v['store_name']
            self.shape_item = {}  
            self.shape_item['points'] = []
        self.tool_input['shapes'] = sorted(self.shapes, key=lambda y:y['label'])                 
        self.tool_input['lineColor'] = [0,255,0,128]
        self.tool_input['imagePath'] = self.image_name 
        self.tool_input['flags'] = {}
        self.tool_input['fillColor'] = [255,0,0,128]
        self.tool_input['imageData'] = None
    
    def _generate_output_file(self, filename):
        try:
            logger.info('json file generated successfully')        
            with open(os.path.join(os.path.dirname(os.path.normpath(self.configs_input_dir)),'maps',self.image_name.replace('.png','.json')),'w') as f:
                f.write(json.dumps(self.tool_input, indent=4))
        except Exception:
            logger.error('Unable to create config json file. Contact support!')            

# if __name__ == '__main__':
#     warnings.warn("This script converts the config directory\n"
#                   "yaml files to labelme input files.")
# 
#     parser = argparse.ArgumentParser()
#     parser.add_argument('input_dir', help='specify config directory containing yaml files')
#     parser.add_argument('image_name', help='specify the image name corresponding to the config')
#     args = parser.parse_args()
#     input_dir = args.input_dir
#     image_name = args.image_name
#     yaml_to_json = YAMLTOJSON(input_dir, image_name)
#     yaml_to_json.run()
#         
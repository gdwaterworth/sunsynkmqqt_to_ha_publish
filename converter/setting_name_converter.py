from csv import DictReader
from pathlib import Path
import json

class SettingNameConverter:
    def __init__(self, setting_name_map=None):
        if setting_name_map is None:
            setting_name_map = {}

        try:
            with open('/resources/Sunsynk_1phase.json') as options_file:
                setting_name_nmap = json.load(options_file)
                
        except Exception as e:
            print("Error loading xxxx.json. Ensure the file exists and is valid JSON.")
            exit()

    def convert_HAlocation(self, key):
        return self.setting_name_map[key]['HAlocation'] if key in self.setting_name_map else None
    
    def convert_type(self, key):
        return self.setting_name_map[key]['type'] if key in self.setting_name_map else None
    
    
    
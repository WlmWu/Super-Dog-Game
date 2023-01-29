import os
import yaml

class Settings():
    def __init__(self):
        self.getSettings()

    def getSettings(self):
        path = os.path.dirname(os.path.realpath(__file__))
        yamlpath = os.path.join(path, 'settings.yaml')
        imgpath = os.path.join(path, 'src')

        with open(yamlpath, encoding='UTF-8') as f:
            self.config = yaml.safe_load(f)     
        sprites = ['dog', 'meat', 'bomb']
        self.spriteDict = {s: self.config[s] for s in sprites}
        for k, d in self.spriteDict.items():
            self.spriteDict[k]['img'] = [os.path.join(imgpath, i) for i in d['img']]
        
        for k, v in self.config['button'].items():
            v['img'] = os.path.join(imgpath, v['img'])
        
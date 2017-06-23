import yaml
import os

class Config(object):
    ''' Class to store column data about the used dataset (column names and types, which to use as 
        quasi-identifiers etc.. YAML format must be this way:
                columns:
                    -   name: age
                        index: 0
                        is_qi: True
                        is_sensible: False
                        type: number
                    -   name: workclass
                        index: 1
                        is_qi: True
                        is_sensible: False
                        type: category
                    -   name: final_weight
                        index: 2
                        is_qi: False
                        is_sensible: False
                        type: number
    '''
    def __init__(self, data = None, file = None):
        self.data = data
        if file:
            assert(not data), 'Config object need EITHER data stream OR file to read from, not both.'
            self.data = read_yaml(file)
        self.attribute_names, self.qi_indices, self.is_cat, self.sa_index = self.get_anonymize_config()

    def get_anonymize_config(self):
        data = self.data
        if not data:
            return None, None, None, None
        attribute_names = [ att['name'] for att in data['columns'] ]
        qi_indices = []
        is_cat = []
        sa_index = None
        for i in range(len(attribute_names)):
            is_qi = data['columns'][i]['is_qi']
            if is_qi:
                qi_indices.append(data['columns'][i]['index'])
                if data['columns'][i]['type'] == 'category':
                    is_cat.append( True )
                else:
                    is_cat.append(False)
                continue
            is_sensible = data['columns'][i]['is_sensible']
            if is_sensible:
                sa_index = data['columns'][i]['index']
        return attribute_names, qi_indices, is_cat, sa_index


def read_yaml(file):
    with open(file, 'r') as readfile:
        data = yaml.load(readfile)
    return data

def write_yaml(self, data, file=None):
    if not file:
        file = '.yaml'
    with open('output-' + file, 'w') as writefile:
        yaml.dump(data, writefile, default_flow_style=False)

if __name__ == '__main__':
    FILENAME = 'adult.yaml'
    file = FILENAME
    config = Config(file=file)
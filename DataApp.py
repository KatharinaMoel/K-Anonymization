import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import ConfigApp

class Data(object):

    def __init__(self, yaml_file=None, csv_file=None, from_records=False, frame=pd.DataFrame()):
        if not from_records:
            ## TODO 
            # assert(file exists), ''
            self.records = self.load_data(yaml_file, csv_file)
        else:
            assert(not frame.empty), 'Data: if you set from_records = True, you must pass a valid (nonempty DataFrame).'
            self.records = frame
        # convert values of non-numeric columns (i.e. categories) to their number of appearance.
        # to translate back, category_dict contains the valuelist (irredundant) for each category col
        self.category_dict = self.convert_categories()
        print("\n Category DICT : \n %s" % self.category_dict )
        self.column_names = self.records.columns

    def load_config(self, yaml_file):
        config = ConfigApp.Config(file = yaml_file)
        attribute_names = config.attribute_names
        qi_indices = config.qi_indices
        is_cat = config.is_cat 
        sa_index = config.sa_index
        qi_names = [ attribute_names[i] for i in qi_indices ]
        indices_wanted = qi_indices + [sa_index]
        names_wanted = qi_names + [attribute_names[sa_index]]
        return indices_wanted, names_wanted

    def load_data(self, yaml_file, csv_file):
        print('\t Load config.')
        indices_wanted, names_wanted = self.load_config(yaml_file)
        print('\t Load csv...')
        data = pd.read_csv(csv_file, usecols = indices_wanted, names=names_wanted)
        return data
    
    def _replace_func(self, col):
        # do no conversion of all columns with numeric and datetime dtype (and bools)
        ## TODO: is bool here wanted?
        if col.dtype.kind in 'biufcmM':
            return col 
        else: 
            _get_index = lambda x: self.value_list(col.name).index(x)
            return col.map(_get_index)

    def convert_categories(self):
        print('\t Temporary convert categories to numbers.')
        category_dict = { col: self.value_list(col, sort=False) for col in self.records if not self.is_numeric(col) }
        self.records = self.records.apply(self._replace_func)
        return category_dict

    def value_list(self, col, sort=True):
        if not sort:
            return list(self.records[col].unique())
        return sorted( list(self.records[col].unique()) )
    
    def value_lists(self, sort=True):
        value_lists = []
        print( self.column_names )
        for i in range(self.qi_length()):
            value_lists.append( self.value_list(self.column_names[i]) )
            #print('Value Lists[i]: \n %s' % value_lists[i])
            #print('self.value_list: %s' % value_lists[i] )
        #print('\n value lists: %s' % value_lists)
        return value_lists

    def is_numeric(self, col):
        ''' True in case of number, boolean (?) and datetime dtype, othw False.'''
        if self.records[col].dtype.kind in 'biufcmM':
            return True
        return False

    def qi_length(self):
        #print('\n qi_length: %s' % (len(self.records.columns) - 1))
        return len(self.records.columns) - 1

    def column_width(self, col):
        print('\n max: %s \t min: %s' %( self.records[col].max(), self.records[col].min() ))
        print('\n max: %s \t min: %s' %( float(self.records[col].max()), float(self.records[col].min()) ))
        print('\n self.records: %s \n %s' %(col, self.records))
        return float(self.records[col].max()) - float(self.records[col].min())

    def column_widths(self):
        widths = []
        col_names = self.column_names
        for i in range(self.qi_length()):
            widths.append( self.column_width(col_names[i]) )
        print('\n Widths: %s' % widths)
        return widths

    def plot(self, x_col = None, y_col = None):
        # if not columns to plot are specified, use column with index 0 and 1
        if not x_col:
            x_col = self.records.columns[0]
        if not y_col:
            y_col = self.records.columns[1]
        assert(x_col in self.records.columns), 'Data.plot: given column name %s for x_col is not valid. Use one out of %s' %(x_col, self.records.columns)
        assert(y_col in self.records.columns), 'Data.plot: given column name %s for y_col is not valid. Use one out of %s' %(y_col, self.records.columns)
        ## TODO: assert x_col, y_col must contain numeric entries to plot
        try:
            self.records.plot.scatter(x=x_col, y=y_col)
            plt.show()
        except KeyError:
            print('PLOT only of numeric values possible')

if __name__ == '__main__':
    newData = Data('data/adult_klein.yaml', 'data/adult_klein.data')
    newData.plot()
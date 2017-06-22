import numpy as numpy
import pandas as pd


class Partition(object):

    def __init__(self, data, k):
        ''' low/ high: list of indices referring to the lowest/ highest member of every column, 
            index w.r.t the (unique) value_list of a column 
        '''
        self.k = k
        self.member = data.records
        self.qi_length = data.qi_length()
        self.allow = [1] * data.qi_length()
        self.value_lists = data.value_lists()
        self.column_widths = data.column_widths()
        self.column_names = data.column_names
        print('\n partition.allow %s' % self.allow)
        print('\n partition.high %s' % self.high())
        #record = self.member.ix[20, :]
        #print('\n record: %s' % record)
        #self.add_record(record)

    def __len__(self):
        """
        return number of records
        """
        return len(self.member)

    def low(self):
        return self.member.idxmin()

    def high(self):
        return self.member.idxmax()

    def get_norm_width(self, dim):
        """
        return Normalized width of partition
        similar to NCP
        dim: column index, not name
        """
        #d_order = self.data.value_list(col)
        #width = float(d_order[partition.high[index]]) - float(d_order[partition.low[index]])
        #return width * 1.0 / QI_RANGE[index]
        current_width = self.column_widths[dim]
        #print('\n WIDTH: %s' % current_width)
        try:
            norm_width = current_width * 1.0 / self.column_widths[dim]
            print('\n Norm_WIDTH: %s' % norm_width)
            return norm_width
        except ZeroDivisionError:
            return -1


    def choose_dimension(self):
        """
        chooss dim with largest norm_width from all attributes.
        This function can be upgraded with other distance function.
        """
        max_width = -1
        max_dim = -1
        for dim in range(self.qi_length):
            if self.allow[dim] == 0:
                continue
            #print('\n \t MaxWIDTH: %s')
            norm_width = self.get_norm_width(dim)
            print('\n MAXWIDTH: %s \t MAXDIM: %s \t WIDTH: %s \t DIM: %s' %(max_width, max_dim, norm_width, dim))
            if norm_width > max_width:
                max_width = norm_width
                max_dim = dim
        print('\n \t Final MAXDIM: %s' % max_dim)
        return max_dim

    def find_median(self, dim):
        """
        find the middle of the partition, return splitVal
        """
        total = len(self.member.index)
        middle = total / 2
        value_list = self.value_lists[dim]
        if middle < self.k or len(value_list) <= 1:
            return None
        col_name = self.column_names[dim]
        col = self.member[col_name]
        median = col.quantile(interpolation='nearest') #self.member[col_name].median()
        print('\n Median: %s' % median)
        return median

        '''
        index = 0
        split_index = 0
        for i, qi_value in enumerate(value_list):
            index += frequency[qi_value]
            if index >= middle:
                splitVal = qi_value
                split_index = i
                break
        else:
            print("Error: cannot find splitVal")
        try:
            nextVal = value_list[split_index + 1]
        except IndexError:
            # there is a frequency value in partition
            # which can be handle by mid_set
            # e.g.[1, 2, 3, 4, 4, 4, 4]
            nextVal = splitVal
        return (splitVal, nextVal, value_list[0], value_list[-1])
        '''
    def split_frame(self, value, dim):
        '''
        splits data frame in two frames lhs and rhs with lhs containing all values <= value
        '''
        col = self.column_names[dim]
        column = self.member[col]
        lhs = self.member[ column <= value ]
        rhs = self.member[ column > value ]
        return lhs, rhs

#if __name__ == '__main__':

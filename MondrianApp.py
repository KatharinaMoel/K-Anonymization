import numpy as numpy
import pandas as pd

import DataApp
import PartitionApp

class Mondrian(object):

    def __init__(self, yaml_file, csv_file, k=10):
        self.k = k
        print('\n k: %s' % k)
        self.data = DataApp.Data(yaml_file, csv_file)
        print('\n First data: \n %s' % self.data.records['occupation'])
        self.result = []
        partition = PartitionApp.Partition(self.data, self.k)
        self.anonymize(partition)

    def anonymize(self, partition):
        print('\n Partition: \n %s' %partition.member)
        allow_count = sum(partition.allow)
        print('\n ALLOW COUNT: %s ' %allow_count)
        if allow_count == 0:
            self.result.append(partition)
            return
        for index in range(allow_count):
            dim = partition.choose_dimension()
            if dim == -1:
                print("Error: dim=-1")
            median = partition.find_median(dim)
            lhs_frame, rhs_frame = partition.split_frame(median, dim)
            if ( rhs_frame.empty or len(lhs_frame.index) < self.k
                 or len(rhs_frame.index) < self.k ):
                partition.allow[dim] = 0
                continue
            # find low/ high for new partitions lhs, rhs
            lhs_data = DataApp.Data(from_records=True, frame=lhs_frame)
            rhs_data = DataApp.Data(from_records=True, frame=rhs_frame)
            lhs = PartitionApp.Partition(lhs_data, self.k)
            rhs = PartitionApp.Partition(rhs_data, self.k)
            self.anonymize(lhs)
            self.anonymize(lhs)
            return
        self.result.append(partition)
        print('\n \n FINISHED!')

if __name__ == '__main__':
    newMondrian = Mondrian('data/adult_klein.yaml', 'data/adult.data')
    newMondrian.data.plot()

    
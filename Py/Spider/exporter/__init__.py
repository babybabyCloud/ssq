# encoding: utf-8

import csv


class CSV:
    def __init__(self, dest, header, data, **kwargs):
        self.dest = dest
        self.header = header
        self.data = data
        self.ext = kwargs

    def export(self):
        with open(self.dest, 'w') as csv_writer:
            writer = csv.writer(csv_writer, **self.ext)
            writer.writerow(header)
            writer.writerows(self.data)
# encoding: utf-8


class CSV:
    def __init__(self, dest, headers, data, **kwargs):
        self.dest = dest
        self.headers = headers
        self.data = data
        self.ext = kwargs

    def export(self):
        import csv
        with open(self.dest, 'w') as csv_writer:
            writer = csv.writer(csv_writer, **self.ext)
            writer.writerow(self.headers)
            writer.writerows(self.data)

exporterfactory = {'.csv': CSV}
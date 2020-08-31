# coding:utf-8

from collections.abc import Iterable
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By
from typing import Generator


class SSQData:
    __slots__ = ['id', 'date', 'reds', 'blue', 'total', 'pool', 'detail_link']

    def __repr__(self):
        return ', '.join(['{0}: {1}'.format(x, getattr(self, x, None)) for x in self.__slots__])

    def next_attr(self):
        for attr in self.__slots__:
            yield attr


class AbstractExtractor(BaseProcessor):
    pass


class RowDataExtractor(AbstractExtractor):
    def __init__(self, table_box: FirefoxWebElement, tbody: str, colums_slice: slice):
        self.table_box = table_box
        self.tbody = tbody
        self.delete_slice = delete_slice

    def execute(self) -> Generator[SSQData, None, None]:
        rows = self.table_box.find_elements(By.XPATH, self.tbody)
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            yield self.get_data_from_column(columns)

    def get_data_from_column(self, columns: FirefoxWebElement) -> SSQData:
        data = SSQData()
        data_next_attr = data.next_attr()
        #del columns[5:11]
        del columns[self.delete_slice]
        for column in columns:
            span = column.find_elements(By.XPATH, 'span')
            if len(span) > 0 and isinstance(span, Iterable):
                setattr(data, next(data_next_attr), [x.text for x in span])
            elif column is columns[-1]:
                setattr(data, next(data_next_attr), column.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            else:
                setattr(data, next(data_next_attr), column.text)
        return data


def get_detail_data_from_column(columns):
    return tuple([columns[index].text for index in range(len(columns))])




if __name__ == '__main__':
    s = SSQData()
    s.id = 1
    for i in s.__slots__:
        setattr(s, i, s.id + 1)

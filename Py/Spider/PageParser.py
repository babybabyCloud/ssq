# coding:utf-8

from collections.abc import Iterable
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import logging


class PageParser:
    def __init__(self):
        self.logger = logging.getLogger('default')

    def get_row_data(self, table_box: FirefoxWebElement, func, tbody):
        rows = table_box.find_elements_by_xpath(tbody)
        for row in rows:
            columns = row.find_elements_by_tag_name('td')
            yield func(columns)

    @staticmethod
    def get_detail_data_from_column(columns):
        return tuple([columns[index].text for index in range(len(columns))])

    @staticmethod
    def get_data_from_column(columns):
        data = SSQData()
        data_next_attr = data.next_attr()
        del columns[5:11]
        for column in columns:
            span = column.find_elements_by_tag_name('span')
            if len(span) > 0 and isinstance(span, Iterable):
                setattr(data, next(data_next_attr), [x.text for x in span])
            elif column is columns[-1]:
                setattr(data, next(data_next_attr), column.find_element_by_tag_name('a').get_attribute('href'))
            else:
                setattr(data, next(data_next_attr), column.text)
        return data


class SSQData:
    __slots__ = ['id', 'date', 'reds', 'blue', 'total', 'pool', 'detail_link']

    def __repr__(self):
        return ', '.join(['{0}: {1}'.format(x, getattr(self, x, None)) for x in self.__slots__])

    def next_attr(self):
        for attr in self.__slots__:
            yield attr


if __name__ == '__main__':
    s = SSQData()
    s.id = 1
    for i in s.__slots__:
        setattr(s, i, s.id + 1)
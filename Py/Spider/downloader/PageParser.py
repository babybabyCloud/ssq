# coding:utf-8

from collections.abc import Iterable
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By


def get_row_data(table_box: FirefoxWebElement, func, tbody):
    rows = table_box.find_elements(By.XPATH, tbody)
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        yield func(columns)


def get_detail_data_from_column(columns):
    return tuple([columns[index].text for index in range(len(columns))])


def get_data_from_column(columns):
    data = SSQData()
    data_next_attr = data.next_attr()
    del columns[5:11]
    for column in columns:
        span = column.find_elements(By.XPATH, 'span')
        if len(span) > 0 and isinstance(span, Iterable):
            setattr(data, next(data_next_attr), [x.text for x in span])
        elif column is columns[-1]:
            setattr(data, next(data_next_attr), column.find_element(By.TAG_NAME, 'a').get_attribute('href'))
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

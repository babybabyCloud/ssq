# coding:utf-8

from collections import defaultdict
from collections.abc import Iterable
from typing import Any
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By
from . import BaseProcessor


class SSQData:
    __slots__ = ['id', 'date', 'reds', 'blue', 'total', 'pool', 'detail_link']

    def __repr__(self):
        return ', '.join(['{0}: {1}'.format(x, getattr(self, x, None)) for x in self.__slots__])

    def next_attr(self):
        for attr in self.__slots__:
            yield attr


class SSQDetails:
    pass


class RowDataExtractor(BaseProcessor):
    def execute(self):
        rows = self.context_data.request.page.find_elements(By.XPATH, self.context_data.request.tbody)
        self.context_data.response = defaultdict(list)
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            extract_data = self.get_data_from_column(columns)
            if extract_data is Iterable:
                self.context_data.response['data'].extend(extract_data)
            else:
                self.context_data.response['data'].append(extract_data)

    def get_data_from_column(self, **kwargs) -> Any:
        pass


class BasePageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: FirefoxWebElement) -> SSQData:
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


class DetailsPageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: FirefoxWebElement):
        return tuple([columns[index].text for index in range(len(columns))])
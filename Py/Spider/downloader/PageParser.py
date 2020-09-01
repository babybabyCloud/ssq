# coding:utf-8

from collections.abc import Iterable
from dataclass import dataclass
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


@dataclass(repr=True)
class SSQDetails:
    id: int
    link: str
    type: int
    type_num: int
    type_money: int


class RowDataExtractor(BaseProcessor):
    def execute(self) -> None:
        self.context_data.response = dict()
        self.context_data.response.setdefault('data', list())
        element_class = self.context_data.request.get('element_class')
        pages = self.context_data.request.get('pages')
        for page in pages:
            rows = page.find_elements(By.XPATH, element_class)
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, 'td')
                self.get_data_from_column(columns)

    def get_data_from_column(self, **kwargs) -> Any:
        pass


class BasePageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: FirefoxWebElement, **kwargs) -> None:
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
            self.context_data.response.get('data').append(data)


class DetailsPageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: FirefoxWebElement, **kwargs) -> None:
        return tuple([columns[index].text for index in range(len(columns))])

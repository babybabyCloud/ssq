# coding:utf-8

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, List
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By
from . import AwardLevel, BaseProcessor
from .. import logger


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
        if self.context_data.response is None:
            self.context_data.response= dict()
        self.context_data.response.setdefault('data', list())
        element_class = self.context_data.request.get('element_class')
        page = self.context_data.request.get('page')
        rows = page.find_elements(By.XPATH, element_class)
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            self.get_data_from_column(columns, **self.context_data.request)

    def get_data_from_column(self, **kwargs) -> Any:
        '''
            Extract data, the extracted data should be put into context_data.response
        '''
        pass


class BasePageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: FirefoxWebElement, **kwargs) -> None:
        '''
            Extract data from DOM

            :param columns: The DOM where the data is extracted from.
        '''
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
            logger.debug('Retrieve data %s', data)
        self.context_data.response.get('data').append(data)


class DetailsPageDataExtractor(RowDataExtractor):
    def get_data_from_column(self, columns: List[FirefoxWebElement], detail: SSQDetails, **kwargs) -> None:
        '''
            Extract data from DOM

            :param columns: The DOM where the data is extracted from.
            :param detail: The SSQDetails instance contained the id and link information
        '''
        details = SSQDetails(id=int(detail.id), type=AwardLevel.name_to_value(columns[0].text), 
                type_num=int(columns[1].text), type_money=int(columns[2].text), link=None)
        self.context_data.response.get('data').append(details)

# coding:utf-8

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from .. import get_file_name
from .. import logger
from . import BaseProcessor
from .PageParser import SSQDetails, DetailsPageDataExtractor


class HtmlDownloader(BaseProcessor):

    def __init__(self, downloader=None):
        """
            Constructor of HtmlDownloader.
        """
        super().__init__()
        if downloader is None:
            self.__options = Options()
            # self.__options.add_argument('-headless')
            self.browser = Firefox(options=self.__options, executable_path=str(get_file_name(__file__, 'geckodriver')))
            self._wait = WebDriverWait(self.browser, 10)
        else:
            self.browser = downloader.browser
            self._wait = downloader._wait

    def execute(self) -> None:
        logger.debug('Execute in %s with data %s', self.__class__, self.context_data.request)
        self.get_page(**self.context_data.request)

    def get_page(self, url: str, element_class: str, **kwargs) -> WebElement:
        pass


class BasePageDownloader(HtmlDownloader):
    def get_page(self, url: str, element_class: str, max_condition: str, **kwargs) -> WebElement :
        '''
        :param url: Tha page URL need to download
        :param element_class: The inner content of element_class need to return 
        :param max_condition: Some element need click before return the data
        '''
        self.browser.get(url)
        self._wait.until(expected.element_to_be_clickable((By.XPATH, max_condition))).click()
        self.context_data.response = dict(page=self._wait.until(expected.visibility_of_element_located((By.CLASS_NAME,
                element_class))), element_class='//tbody/tr')


class DetailsPageDownloader(HtmlDownloader, DetailsPageDataExtractor):
    def __init__(self, downloader=None):
        super().__init__(downloader)
        
    def get_page(self, details: List[SSQDetails], element_cls: str, **kwargs) -> WebElement :
        self.context_data.response = dict()
        self.context_data.response.setdefault('data', list())
        self.context_data.request['element_class'] = 'table/tbody/tr'
        for item in details:
            self.browser.get(item.link)
            self.context_data.request['page'] = self._wait.until(expected.visibility_of_element_located(
                (By.CLASS_NAME, element_cls)))
            self.context_data.request['detail'] = item
            super(HtmlDownloader, self).execute()
        logger.info(self.context_data.response)
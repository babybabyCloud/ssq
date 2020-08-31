# coding:utf-8

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from .. import get_file_name
from .. import logger
from . import BaseProcessor


class HtmlDownloader(BaseProcessor):

    def __init__(self, downloader=None):
        """
            Constructor of HtmlDownloader.
        """
        if downloader is None:
            self.__options = Options()
            self.__options.add_argument('-headless')
            self.browser = Firefox(options=self.options, executable_path=str(get_file_name(__file__, 'geckodriver')))
            self._wait = WebDriverWait(self.browser, 10)
        else:
            self.browser = downloader.browser
            self._wait = downloader._wait

    def __del__(self):
        logger.info('Close the browser')
        self.browser.quit()

    def execute(self) -> None:
        logger.info('Execute in %s with data %s', self.__class__, self.context_data.request)
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
        self.wait.until(expected.element_to_be_clickable((By.XPATH, max_condition))).click()
        self.context_data.response = dict(page=self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME,
                element_class))), tbody='//tbody/tr')


class DetailsPageDownloader(HtmlDownloader):
    def get_page(self, url: str, element_class: str, **kwargs) -> WebElement :
        self.browser.get(url)
        self.context_data.response = dict(page=self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 
                element_class))), tbody='table/tbody/tr')
# coding:utf-8

from abc import ABC
from Spider import downloader
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from .. import get_file_name
from .. import logger


class HtmlDownloader(ABC):

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

    def get_page(self, url: str, element_class: str, **kwargs) -> WebElement:
        '''
        :param url: Tha page URL need to download
        :param element_class: The inner content of element_class need to return 
        '''
        pass


class BasePageDownloader(HtmlDownloader):
    def get_page(self, url: str, element_class: str, max_condition: str) -> WebElement :
        '''
        :param max_condition: Some element need click before return the data
        '''
        self.browser.get(url)
        self.wait.until(expected.element_to_be_clickable((By.XPATH, max_condition))).click()
        return self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, element_class)))


class DetailsPageDownloader(HtmlDownloader):
    def get_page(self, url: str, element_class: str) -> WebElement :
        self.browser.get(url)
        return self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, element_class)))
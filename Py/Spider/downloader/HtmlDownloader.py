# coding:utf-8

import logging
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger('default')


class HtmlDownloader:

    def __init__(self):
        """
            Constructor of HtmlDownloader.
        """
        self.options = Options()
        self.options.add_argument('-headless')
        self.browser = Firefox(options=self.options, executable_path=str(ConfigFileSearchHelper.get_file_name(__file__, 'geckodriver')))
        self.wait = WebDriverWait(self.browser, 10)

    def __del__(self):
        self.browser.quit()

    def get_page(self, url, table_class, max_condition=None):
        self.browser.get(url)
        if max_condition:
            self.wait.until(expected.element_to_be_clickable((By.XPATH, max_condition))).click()
        return self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, table_class)))


class ConfigFileSearchHelper:

    @staticmethod
    def get_file_name(file_path, target_name):
        import os.path
        from pathlib import PurePath
        directory = os.path.dirname(os.path.abspath(file_path))
        return PurePath(directory, target_name)


if __name__ == "__main__":
    downloader = HtmlDownloader()
    downloader.get_page(r"http://www.cwl.gov.cn/kjxx/ssq/kjgg/")

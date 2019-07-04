# coding:utf-8

import logging
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


logger = logging.getLogger('log_default')


class HtmlDownloader:

    def __init__(self):
        """
            Constructor of HtmlDownloader.
        """
        self.options = Options()
        self.options.add_argument('-headless')
        self.browser = Firefox(options=self.options)
        self.wait = WebDriverWait(self.browser, 10)

    def __del__(self):
        self.browser.quit()

    def get_page(self, url, table_class, max_condition=None):
        self.browser.get(url)
        if max_condition:
            self.wait.until(expected.element_to_be_clickable((By.XPATH, max_condition))).click()
        return self.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, table_class)))


if __name__ == "__main__":
    downloader = HtmlDownloader()
    downloader.get_page(r"http://www.cwl.gov.cn/kjxx/ssq/kjgg/")

# coding:utf-8

from Spider.HtmlDownloader import HtmlDownloader
from Spider.DBHandler import DbHandler
from Spider.PageParser import PageParser
from Spider.AwardLevel import AwardLevel
import configparser
import logging
from logging.config import fileConfig


fileConfig('logging.ini')
logger = logging.getLogger('log_default')


class Manager:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini', encoding='utf-8')
        self.downloader = HtmlDownloader()
        self.db = DbHandler(self.conf)
        self.page_parser = PageParser()

    def start(self, url):
        details_page = []
        table_box = self.downloader.get_page(url, 'bgzt', '//li[@data-xq=100]')
        row_gen = self.page_parser.get_row_data(table_box, PageParser.get_data_from_column, '//tbody/tr')
        for row in row_gen:
            self.db.insert_base(row.id, row.reds, row.blue, row.date[:-3])
            self.db.insert_detail(row.id, row.date[-2:-1], row.total, row.pool, row.detail_link)
            print(row)
            details_page.append((row.id, row.detail_link))

        for page in details_page:
            detail_table = self.downloader.get_page(page[1], 'zjqk')
            for i in self.page_parser.get_row_data(detail_table,
                                                   PageParser.get_detail_data_from_column, 'table/tbody/tr'):
                tp = None
                for name, member in AwardLevel.__members__.items():
                    if name == i[0]:
                        tp = member.value
                        break
                if tp:
                    self.db.insert_details(page[0], tp, i[1], i[2])


def main():
    manager = Manager()
    url = r'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'
    logger.info(url)
    manager.start(url)


if __name__ == '__main__':
    main()

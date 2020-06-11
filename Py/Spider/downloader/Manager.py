#! coding:utf-8

from Spider.downloader.HtmlDownloader import HtmlDownloader, ConfigFileSearchHelper
from Spider.downloader.DBHandler import DbHandler
from Spider.downloader.PageParser import PageParser
from Spider.downloader.AwardLevel import AwardLevel
import logging
from logging.config import dictConfig
import json

with open(str(ConfigFileSearchHelper.get_file_name(__file__, 'logging.json'))) as f:
    config = json.load(f)
    dictConfig(config)

logger = logging.getLogger('default')
START_PAGE = r'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'


class Manager:

    def __init__(self, db_file, query_count):
        self.downloader = HtmlDownloader()
        self.db = DbHandler(db_file)
        self.page_parser = PageParser()
        self._query_count = query_count

    def start(self, url):
        self.db.init_db()
        details_page = []
        table_box = self.downloader.get_page(url, 'bgzt', '//li[@data-xq=%s]' % self._query_count)
        row_gen = self.page_parser.get_row_data(table_box, PageParser.get_data_from_column, '//tbody/tr')
        for row in row_gen:
            self.db.insert_base(row.id, row.reds, row.blue, row.date[:-3])
            self.db.insert_detail(row.id, row.date[-2:-1], row.total, row.pool, row.detail_link)
            details_page.append((row.id, row.detail_link))

        for page in details_page:
            try:
                detail_table = self.downloader.get_page(page[1], 'zjqk')
            except Exception as e:
                logger.error("Error page %s" % page[1])
                continue
            for i in self.page_parser.get_row_data(detail_table,
                    PageParser.get_detail_data_from_column, 'table/tbody/tr'):
                tp = None
                for name, member in AwardLevel.__members__.items():
                    if name == i[0]:
                        tp = member.value
                        break
                if tp:
                    self.db.insert_details(page[0], tp, i[1], i[2])
        logger.info('Pulling completed!')


def main(**kwargs):
    manager = Manager(**kwargs)
    url = START_PAGE
    logger.info(url)
    manager.start(url)


if __name__ == '__main__':
    main()

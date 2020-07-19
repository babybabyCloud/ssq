#! coding:utf-8

from Spider.downloader import get_file_name
from Spider.downloader.HtmlDownloader import HtmlDownloader
from Spider.dboperator.DBHandler import DbHandler
from Spider.downloader.PageParser import PageParser
from Spider.downloader.AwardLevel import AwardLevel
from Spider.dboperator import new_session
import logging
from logging.config import dictConfig
import json
from datetime import datetime

with open(str(get_file_name(__file__, 'logging.json'))) as f:
    config = json.load(f)
    dictConfig(config)

logger = logging.getLogger('default')
START_PAGE = r'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'


class Manager:

    def __init__(self, db_file, query_count):
        self.downloader = HtmlDownloader()
        self.db = DbHandler()
        self.page_parser = PageParser()
        self._query_count = query_count
        self.session = new_session('sqlite:///%s' % db_file)

    def start(self, url):
        details_page = []
        table_box = self.downloader.get_page(url, 'bgzt', '//li[@data-xq=%s]' % self._query_count)
        row_gen = self.page_parser.get_row_data(table_box, PageParser.get_data_from_column, '//tbody/tr')
        for row in row_gen:
            self.db.insert_base(row.id, row.reds, row.blue[0], datetime.strptime(row.date[:-3], '%Y-%m-%d'), self.session)
            self.db.insert_detail(row.id, row.date[-2:-1], row.total, row.pool, row.detail_link, self.session)
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
                    self.db.insert_details(page[0], tp, i[1], i[2], self.session)
        self.session.commit()
        logger.info('Pulling completed!')


def main(**kwargs):
    manager = Manager(**kwargs)
    url = START_PAGE
    logger.info(url)
    manager.start(url)


if __name__ == '__main__':
    main()

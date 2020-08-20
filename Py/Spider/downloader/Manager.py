#! coding:utf-8

from .. import logger
from ..downloader.HtmlDownloader import HtmlDownloader
from ..dboperator.DBHandler import DbHandler
from ..downloader.PageParser import PageParser
from ..downloader import AwardLevel
from ..dboperator import new_session
from datetime import datetime

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
            record_base = RecordBase(id=row.id, red1=row.reds[0], red2=row.reds[1], red3=row.reds[2], red4=row.reds[3], 
                red5=row.reds[4], red6=row.reds[5], blue=row.blue, date_=datetime.strptime(row.date[:-3], '%Y-%m-%d'))
            record_detail = RecordDetail(id=row.id, week=row.date[-2:-1], sales=row.tatal, pool_money=row.pool, 
                detail_link=row.detail_link)
            self.db.insert_base(record_base, self.session)
            self.db.insert_detail(record_detail, self.session)
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
                    record_details = RecordDetails(id=page[0], type=tp, type_num=i[1], type_money=i[2])
                    self.db.insert_details(record_details, self.session)
        self.session.commit()
        logger.info('Pulling completed!')


def main(**kwargs):
    manager = Manager(**kwargs)
    url = START_PAGE
    logger.info('Start pulling from %s' %url)
    manager.start(url)


if __name__ == '__main__':
    main()

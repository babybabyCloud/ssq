#! coding:utf-8

from . import AwardLevel, ProcessContext
from .DataStore import BasePageDataStore
from .HtmlDownloader import BasePageDownloader, DetailsPageDownloader
from .PageParser import BasePageDataExtractor
from .. import logger
from ..dboperator.DBHandler import *
from ..dboperator import new_session
from ..dbmodels import *
from datetime import datetime

START_PAGE = r'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'


class Manager:

    def __init__(self, db_file, query_count):
        self._query_count = query_count
        self._session = new_session('sqlite:///%s' % db_file)
        self._processors_chains = self.init_chain()

    def init_chain(self):
        bd = BasePageDownloader()
        bde = BasePageDataExtractor()
        bpd = BasePageDataStore(self._session)
        dpd = DetailsPageDownloader(bd)
        return (bd, bde, bpd, dpd)

    def start(self, url: str):
        _ctx = ProcessContext(response=dict(url=START_PAGE, \
                element_class='bgzt', max_condition='//li[@data-xq=%s]' %self._query_count), request=None)
        for processor in self._processors_chains:
            processor.context_data.request = _ctx.response
            processor.execute()
            _ctx = processor.context_data

        # details_page = []
        # table_box = self.downloader.get_page(url, 'bgzt', '//li[@data-xq=%s]' % self._query_count)
        # row_gen = get_row_data(table_box, get_data_from_column, '//tbody/tr')
        # for row in row_gen:
        #     record_base = RecordBase(id=row.id, red1=row.reds[0], red2=row.reds[1], red3=row.reds[2], red4=row.reds[3],
        #                              red5=row.reds[4], red6=row.reds[5], blue=row.blue[0], 
        #                              date_=datetime.strptime(row.date[:-3], '%Y-%m-%d')
        #                              )
        #     record_detail = RecordDetail(id=row.id, week=row.date[-2:-1], sales=row.total, pool_money=row.pool)
        #     insert_base(record_base, self.session)
        #     insert_detail(record_detail, self.session)
        #     details_page.append((row.id, row.detail_link))

        # for page in details_page:
        #     try:
        #         detail_table = self.downloader.get_page(page[1], 'zjqk')
        #     except Exception as e:
        #         logger.error("Error page %s" % page[1])
        #         continue
        #     for i in get_row_data(detail_table,
        #             get_detail_data_from_column, 'table/tbody/tr'):
        #         tp = None
        #         for name, member in AwardLevel.__members__.items():
        #             if name == i[0]:
        #                 tp = member.value
        #                 break
        #         if tp:
        #             record_details = RecordDetails(id=page[0], type=tp, type_num=i[1], type_money=i[2])
        #             insert_details(record_details, self.session)
        # self.session.commit()
        # logger.info('Pulling completed!')
        # self.start_compute()
        self._session.rollback()


    def start_compute(self):
        logger.info('Start compute mean')

        from ..analyse.compute import compute_means
        from ..dboperator import get_engine

        compute_means(get_engine(), int(self._query_count))


def main(**kwargs):
    manager = Manager(**kwargs)
    url = START_PAGE
    logger.info('Start pulling from %s' %url)
    manager.start(url)


if __name__ == '__main__':
    main()

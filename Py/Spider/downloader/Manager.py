#! coding:utf-8

from . import ProcessContext
from .DataStore import BasePageDataStore, DetailsPageDataStore
from .HtmlDownloader import BasePageDownloader, DetailsPageDownloader
from .PageParser import BasePageDataExtractor
from ..dboperator.DBHandler import *
from ..dboperator import new_session
from ..dbmodels import *
from Spider.logging import LoggerFactory


START_PAGE = r'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'
logger = LoggerFactory.get_logger(__name__)


class Manager:

    def __init__(self, db_file: str, query_count: str) -> None:
        self._query_count = query_count
        self._session = new_session('sqlite:///%s' % db_file)
        self._processors_chains = self.init_chain()

    def init_chain(self):
        bd = BasePageDownloader()
        bde = BasePageDataExtractor()
        bpd = BasePageDataStore(self._session)
        self.dpd = DetailsPageDownloader(bd)
        dpds = DetailsPageDataStore(self._session)
        return (bd, bde, bpd, self.dpd, dpds)

    def start(self):
        _ctx = ProcessContext(response=dict(url=START_PAGE, \
                element_class='bgzt', max_condition='//li[@data-xq=%s]' %self._query_count), request=None)

        for processor in self._processors_chains:
            processor.context_data.request = _ctx.response
            processor.context_data.response = None
            processor.execute()
            _ctx = processor.context_data

        self._session.commit()
        logger.info('Pulling completed!')
        self.dpd.close()
        self.start_compute()


    def start_compute(self):
        logger.info('Start computing')

        from ..analyse.compute import compute_means
        from ..dboperator import get_engine

        compute_means(get_engine(), int(self._query_count))


def main(*args):
    manager = Manager(*args)
    logger.info('Start pulling from %s' %START_PAGE)
    manager.start()
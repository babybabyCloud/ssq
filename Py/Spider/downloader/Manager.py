#! coding:utf-8

from . import AwardLevel
from .. import run_async, strptime
from ..dboperator.DBHandler import *
from ..dboperator import new_session
from ..dbmodels import *
from ..logging import LoggerFactory
from bs4 import BeautifulSoup
from http import HTTPStatus
from httpx import Client, AsyncClient

import asyncio
import re


logger = LoggerFactory.get_logger(__name__)
_id_extract_reg = re.compile(r'\d+')


class Manager:

    _parser_type = 'html.parser'

    def __init__(self, db_file: str, query_count: str) -> None:
        self._scheme = 'http'
        self._domain = 'www.cwl.gov.cn'
        self._host = f'{self._scheme}://{self._domain}'
        self._refere = f'{self._host}/kjxx/ssq/kjgg/'
        self._query_count = query_count
        self._session = new_session(f'sqlite:///{db_file}')
        self._sub_page = set()

    def start(self) -> None:
        """
        Start
        """
        get_url = f'{self._host}/cwl_admin/kjxx/findDrawNotice'
        with Client() as client:
            param = {'name': 'ssq', 'issueCount': self._query_count}
            header = {'Host': self._domain, 'Referer': self._refere}
            logger.info(f'Start pulling from {get_url} with param {param} and header {header}')
            res = client.get(get_url, params=param, headers=header)
            if res.status_code == HTTPStatus.OK and (data := res.json()).get('message') == '查询成功':
                logger.info(f'Success get data from {get_url}')
                data = res.json()
                self.process_record(data)
            else :
                logger.error(f'Fail to get data from {res.request}, status code is {res.status_code}, message is {res.text}')

    
    def process_record(self, data: dict) -> None:
        """
        Store the base and detail records into DB

        :param data: The data
        """
        details_co = []
        for record in data['result']:
            base_arg_dict = {}
            base_arg_dict['id'] = int(record['code'])
            for index, element in enumerate((red for red in record['red'].split(','))):
                    base_arg_dict[f'red{index+1}'] = int(element)
            base_arg_dict['blue'] = record['blue']
            # record['date'] = 	"2021-03-07(日)"
            base_arg_dict['date_'] = strptime(record['date'][:-3], '%Y-%m-%d')
            record_base = RecordBase(**base_arg_dict)

            detail_arg_dict = {}
            detail_arg_dict['id'] = int(record['code'])
            detail_arg_dict['week'] = record['week']
            detail_arg_dict['sales'] = record['sales']
            detail_arg_dict['pool_money'] = record['poolmoney']
            detail_arg_dict['detail_link'] = record['detailsLink']
            record_detail = RecordDetail(**detail_arg_dict)

            details_co.append(self.process_record_details(record['detailsLink']))

            logger.debug(f'base_arg_dict for RecordBase is {base_arg_dict}.\ndetail_arg_dict for RecordDetail is '\
                    f'{detail_arg_dict}.\nInsert record_base {record_base}.\nInsert record_detail {record_detail}.')
            insert_base(record_base, self._session)
            insert_detail(record_detail, self._session)
        

        asyncio.run(run_async(details_co))
        self._session.commit()

        self.start_compute()


    async def process_record_details(self, path: str) -> None:
        """
        Process the record details

        :param path: The details path
        """
        async with AsyncClient(base_url=self._host, timeout=30.0) as client:
            logger.info(f'Get page from {self._host}{path}')
            res = await client.get(f'{path}')
            if res.status_code == HTTPStatus.OK:
                soup = BeautifulSoup(res.text, self._parser_type)
                table_body = soup.tbody
                details_id = _id_extract_reg.search(soup.h2.text).group(0)
                for row in table_body.find_all('tr'):
                    column_1 = row.find('td')
                    column_2 = column_1.next_sibling.next_sibling
                    column_3 = column_2.next_sibling.next_sibling
                    details_arg_dict = {}
                    details_arg_dict['id'] = details_id
                    details_arg_dict['type'] = AwardLevel.name_to_value(column_1.text)
                    details_arg_dict['type_num'] = int(column_2.text)
                    details_arg_dict['type_money'] = int(column_3.text)

                record_details = RecordDetails(**details_arg_dict)
                logger.debug(f'details_arg_dict for RecordDetails is {details_arg_dict}.\n'\
                        f'Insert record_details {record_details}.')
                insert_details(record_details, self._session)
            else:
                logger.error(f'{res.request}, status: {res.status_code}')


    def start_compute(self):
        logger.info('Start computing')

        from ..analyse import compute
        from ..dboperator import get_engine

        compute(get_engine(), int(self._query_count))




def main(*args):
    logger.info(args)
    manager = Manager(*args)
    manager.start()
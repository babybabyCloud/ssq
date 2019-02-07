# coding:utf-8

from HtmlDownloader import HtmlDownloader
from DBHandler import DbHandler
import configparser
import json


class Manager:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini', encoding='utf-8')
        self.downloader = HtmlDownloader()
        self.db = DbHandler(self.conf)
        self.urls = set()

    def start(self, url):
        self.urls.add(url)
        self.downloader.get_cookie()
        for url in self.urls:
            content = self.downloader.get_content(url)
            result = json.loads(content, encoding='utf-8')['result']
            for item in result:
                self.db.insert_base(item['code'], *(item['red'].split(',')), item['blue'], item['date'][:-3])
                self.db.insert_detail(item['code'], item['week'], item['sales'], item['poolmoney'],
                                      repr(item['detailsLink']))
                for prize in item['prizegrades']:
                    self.db.insert_details(item['code'], prize['type'], prize['typenum'], prize['typemoney'])


if __name__ == '__main__':
    manager = Manager()
    manager.start(r"http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=1")


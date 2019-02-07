# coding:utf-8

import requests


class HtmlDownloader:

    key = '21_qv'
    auth = 'http://www.cwl.gov.cn/cwl_admin/stat/dealer?SiteID=21&CatalogInnerCode=000291000001000001&Type=null&sr=1366x768&cd=24&ce=1&la=zh-CN&cs=UTF-8&vq=1&Referer=http://www.cwl.gov.cn/&Title=%E5%BE%80%E6%9C%9F%E5%BC%80%E5%A5%96_%E4%B8%AD%E5%9B%BD%E7%A6%8F%E5%BD%A9%E7%BD%91&URL=http://www.cwl.gov.cn/kjxx/ssq/kjgg/&Host=www.cwl.gov.cn'

    def __init__(self):
        """
            Constructor of HtmlDownloader.
        """
        self.headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                        "Host": "www.cwl.gov.cn",
                        "Referer": "http://www.cwl.gov.cn/kjxx/ssq/kjgg/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.session = requests.Session()
        self.domain = None
        self.session.headers = self.headers

    def get_cookie(self):
        """
            Accessing base url to get the cookie object
        :return: None
        """
        res = self.session.get(self.auth)
        for co in res.cookies:
            if not self.domain:
                self.domain = co.domain

    def get_content(self, url):
        if not self.session.cookies.get(self.key):
            temp_cookie = requests.cookies.create_cookie(self.key, '1')
            temp_cookie.domain = self.domain
            self.session.cookies.set_cookie(temp_cookie)
        else:
            self.session.cookies.set(self.key, str(int(self.session.cookies.get(self.key)) + 1))

        res = self.session.get(url)
        res.encoding = 'utf-8'
        import pprint
        pprint.pprint(res.text)
        return res.text


if __name__ == "__main__":
    downloader = HtmlDownloader()
    downloader.get_cookie()
    downloader.get_content(r"http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=1")

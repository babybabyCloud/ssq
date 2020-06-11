# encoding: utf-8

from Spider.dboperator import Base
from Spider.downloader import get_file_name
import yaml


class Reader(Base):
    def __init__(self, config, yaml_path):
        super().__init__()
        with open(get_file_name(__file__, yaml_path)) as stream:
            self.sql_templates = yaml.safe_load(stream)

    def select_record_base(self):
        pass
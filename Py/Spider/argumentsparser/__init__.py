# encoding: utf-8

from abc import ABC, abstractmethod
from argparse import Action, ArgumentParser
from .. import SubCommandType
from ..exporter import Export
from ..downloader import Manager, QueryCountEnum


class SubCommand(ABC):
    def __init__(self):
        self._parser = ArgumentParser()
        self._parser.add_argument('--db-file', help='sqlite db file position must be provided', dest='db_file', required=True)

    @abstractmethod
    def execute(self, args):
        pass

    def extract(self, args):
        return self._parser.parse_args(args)


class DownloadSubCommand(SubCommand):
    def __init__(self):
        super().__init__()
        self._parser.add_argument('--query-count', 
            choices=[v.value for v in list(QueryCountEnum)], 
            default=QueryCountEnum.HIGHT.value, 
            dest='query_count')

    def execute(self, args):
        Manager.main(**vars(self.extract(args)))


class ExportSubCommand(SubCommand):
    def __init__(self):
        super().__init__()
        self._parser.add_argument('--before', 
            help='The date before for export: YYYY-MM-DD',
            type=strptime)
        self._parser.add_argument('--after', 
            help='The date afater for export: YYYY-MM-DD',
            type=strptime)
        self._parser.add_argument('--limit',
            help='The max counts for exporting', 
            type=int)
        self._parser.add_argument('--out', 
            help='The output file.', 
            nargs='?',
            default='.')
        self._parser.add_argument('table', 
            help='The names of tables for exporting')

    def execute(self, args):
        Export.main(**vars(self.extract(args)))


class SubCommandAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.__sub_command_mapping = dict(zip([SubCommandType.DOWNLOAD.value, SubCommandType.EXPORT.value], 
            [DownloadSubCommand(), ExportSubCommand()]))

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.__sub_command_mapping[values])

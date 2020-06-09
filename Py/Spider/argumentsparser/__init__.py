# encoding: utf-8

from abc import ABC, abstractmethod
from argparse import Action, ArgumentParser
from Spider import SubCommandType
from Spider.downloader import Manager, QueryCountEnum


class SubCommand(ABC):
    def __init__(self):
        self._parser = ArgumentParser()

    @abstractmethod
    def execute(self, args):
        pass

    def validate(self, args):
        return self._parser.parse_args(args)

class DownloadSubCommand(SubCommand):
    def __init__(self):
        super().__init__()
        self._parser.add_argument('--query-count', 
            choices=QueryCountEnum.__members__.values, 
            default=QueryCountEnum.HIGHT.value, 
            dest='query_count')

    def execute(self, args):
        Manager.main(self.validate(args))


class ExportSubCommand(SubCommand):
    def execute(self, args):
        print('export')


class SubCommandAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.__sub_command_mapping = dict(zip([SubCommandType.DOWNLOAD.value, SubCommandType.EXPORT.value], 
            [DownloadSubCommand(), ExportSubCommand()]))

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.__sub_command_mapping[values])
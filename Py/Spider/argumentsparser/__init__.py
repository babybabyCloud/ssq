# encoding: utf-8

from abc import ABC, abstractmethod
from argparse import Action
from Spider import SubCommandType
from Spider.downloader import Manager


class SubCommand(ABC):
    def __init__(self, validator):
        self.validator_ = validator

    @abstractmethod
    def execute(self, **kwargs):
        pass

class ArgumentValidator(ABC):
    @abstractmethod
    def validate(self, **kwargs):
        pass

class DownloadValidator(ArgumentValidator):
    def validate(self, **kwargs):
        return super().validate(**kwargs)

class DownloadSubCommand(SubCommand):
    def execute(self, **kwargs):
        Manager.main(**kwargs)


class ExportSubCommand(SubCommand):
    def execute(self, **kwargs):
        print('export')


class SubCommandAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
        self.__sub_command_mapping = dict(zip([SubCommandType.DOWNLOAD.value, SubCommandType.EXPORT.value], 
            [DownloadSubCommand(), ExportSubCommand()]))

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.__sub_command_mapping[values])


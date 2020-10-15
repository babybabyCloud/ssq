#! -*- encoding;utf-8 -*-

import click
import Spider.logging


LOG_LEVEL_OPTS = ('NOTSET', 'DEBUG','INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL')
QUERY_COUNT_OPTS = ('30', '50', '100')
DB_FIEL_ARG_NAME = 'db_file'


@click.group()
@click.option('--log-level', 'log_level', 
    type=click.Choice(LOG_LEVEL_OPTS, case_sensitive=False), help='The log level.')
@click.option('--log-path', 'log_path', help='The path of the log.')
@click.option('--log-config', Spider.logging.LOG_CONFIG_PATH_STR, help='The full path of the log json file.')
@click.option('--db-file', DB_FIEL_ARG_NAME, required=True, help='The path of the the SQLite DB file.')
@click.pass_context
def main(ctx, **kwargs):
    if not kwargs.get(Spider.logging.LOG_CONFIG_PATH_STR):
        del kwargs[Spider.logging.LOG_CONFIG_PATH_STR]
    Spider.logging.LoggerFactory.init_log_config(**kwargs)
    ctx.ensure_object(dict)

    ctx.obj[DB_FIEL_ARG_NAME] = kwargs.get(DB_FIEL_ARG_NAME)


@main.command()
@click.option('--query-count', 'query_count', type=click.Choice(QUERY_COUNT_OPTS), required=True, 
    help='The count need to pull.')
@click.pass_context
def download(ctx, query_count):
    from .downloader import Manager
    Manager.main(ctx.obj.get(DB_FIEL_ARG_NAME), query_count)


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('sub_command', action=argumentsparser.SubCommandAction,
#                         choices=[item.value for item in list(SubCommandType)])
#     parser.add_argument('sub_args', nargs=argparse.REMAINDER)
#     return parser.parse_args()
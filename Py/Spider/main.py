#! -*- encoding;utf-8 -*-

import click
import Spider.logging
from  . import _DATE_FORMAT
from datetime import date
from . import strptime


LOG_LEVEL_OPTS = ('NOTSET', 'DEBUG','INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL')
QUERY_COUNT_OPTS = ('30', '50', '100')
DB_FIEL_ARG_NAME = 'db_file'


def validate_date(ctx: click.Context, param: click.Parameter, value: str, format: str = _DATE_FORMAT) -> date:
    """
    Validate the date option value.
    :param ctx: 
    """
    return strptime(value, format) if value else None


@click.group()
@click.option('--log-level', 'log_level', envvar="SSQ_LOG_LEVEL",
    type=click.Choice(LOG_LEVEL_OPTS, case_sensitive=False), help='The log level.')
@click.option('--log-path', 'log_path', help='The path of the log.')
@click.option('--log-config', Spider.logging.LOG_CONFIG_PATH_STR, help='The full path of the log json file.')
@click.option('--db-file', DB_FIEL_ARG_NAME, required=True, help='The path of the the SQLite DB file.')
@click.pass_context
def main(ctx, **kwargs):
    ctx.ensure_object(dict)
    ctx.obj[DB_FIEL_ARG_NAME] = kwargs.pop(DB_FIEL_ARG_NAME)

    if not kwargs.get(Spider.logging.LOG_CONFIG_PATH_STR):
        del kwargs[Spider.logging.LOG_CONFIG_PATH_STR]
    Spider.logging.LoggerFactory.init_log_config(**kwargs)


@main.command()
@click.option('--query-count', 'query_count', default=QUERY_COUNT_OPTS[0], 
    type=click.Choice(QUERY_COUNT_OPTS), required=True, help='The count need to pull.')
@click.pass_context
def download(ctx, query_count: str):
    from .downloader import Manager
    Manager.main(ctx.obj.get(DB_FIEL_ARG_NAME), query_count)


@main.command()
@click.option('--before', callback=validate_date, help='The date before for export: YYYY-MM-DD')
@click.option('--after', callback=validate_date, help='The date after for export: YYYY-MM-DD')
@click.option('--limit', type=int, help='The max counts for exporting')
@click.option('--out', default='.', help='The output file')
@click.argument('table')
@click.pass_context
def export(ctx, **kwargs):
    from .exporter import Export
    Export.main(ctx.obj.get(DB_FIEL_ARG_NAME), **kwargs)

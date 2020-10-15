#! -*- encoding;utf-8 -*-

import click
import Spider.logging

@click.group()
@click.option(
    '--log-level', 
    'log_level',  
    type=click.Choice([
        'NOTSET',
        'DEBUG',
        'INFO',
        'WARN',
        'WARNING',
        'ERROR',
        'FATAL',
        'CRITICAL'
    ], case_sensitive=False))
@click.option(
    '--log-path',
    'log_path'
)
@click.option(
    '--log-config',
    Spider.logging.LOG_CONFIG_PATH_STR
)
def main(**kwargs):
    if not kwargs.get(Spider.logging.LOG_CONFIG_PATH_STR):
        del kwargs[Spider.logging.LOG_CONFIG_PATH_STR]
    Spider.logging.LoggerFactory.init_log_config(**kwargs)


@main.command()
@click.option(
    '--query-count',
    'query_count',
    type=click.Choice((
        '30', 
        '50', 
        '100',
    ))
)
def download(query_count):
    click.echo(query_count)


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('sub_command', action=argumentsparser.SubCommandAction,
#                         choices=[item.value for item in list(SubCommandType)])
#     parser.add_argument('sub_args', nargs=argparse.REMAINDER)
#     return parser.parse_args()
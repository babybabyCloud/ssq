# encoding: utf-8

from ..dboperator import new_session, get_engine
from pandas import read_sql_table


def compute_means(engine: sqlalchemy.engine.Engine):
    read_sql_table(

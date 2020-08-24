# encoding: utf-8

from ..dboperator import new_session, get_engine
from ..dbmodels.model import RecordBase
from pandas import read_sql_table
from sqlalchemy.engine import Engine


def compute_means(engine: Engine):
    df = read_sql_query(RecordBase, engine)

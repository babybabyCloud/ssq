# encoding: utf-8

from ..dboperator import new_session, get_engine
from pandas import read_sql_query
from sqlalchemy.engine import Engine


def compute_means(engine: Engine):
    df = read_sql_query('''
        select * from record_base rb 
        left join records_mean rm on rb.id = rm.id
        order by rb.id;''', engine)